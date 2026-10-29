# Slot Holder — parametric reconstruction.
#
# Reverse-engineered from components/Slot Holder.stl (watertight mesh, 4440
# triangles) by listing its coplanar facet groups with trimesh and fitting
# circles to the curved vertex rings. The part is a 3D-printed U-shaped
# holder / cradle:
#
#   * a 95 x 104.8 mm U plate, 15 mm thick (Y), whose bottom corners are
#     30 mm radii. A 81 mm wide slot opens from the top; the slot walls are
#     7 mm thick, the floor is 4 mm thick, and the slot's bottom corners are
#     tangent arcs of radius 25.53 that meet the flat floor at an angle.
#   * every edge of that U is rounded r = 2, EXCEPT the slot contour on the
#     front face (y = 58.017), which is left sharp because the retaining
#     lips sit there.
#   * three 2 mm thick retaining lips on the front face, projecting into the
#     slot: one 6.9 mm wide strip down each wall (z = -12 .. 40) and a 31 mm
#     wide, 6 mm tall strip on the floor. Each side lip carries a screw
#     hole: 2.4 mm through the lip with a 4.8 mm x 1.4 mm deep counterbore
#     opening into the slot (an M2 fastener from inside the slot).
#   * a 6 mm through-hole across each side wall (axis X), 7 mm behind the
#     front face.
#
# Clean (typed) numbers recovered: 95, 104.8, 15, 7, 4, 2, 30, 81, 31, 6,
# 52, 2.4/4.8 dia, 0.6/1.4 cbore split, hole y = front + 7, hole dia 6.
# Derived / fitted (not clean): the slot arc (r 25.5302, leaving the wall
# 28.408 above the bottom), the side-lip width 6.9117 (= 7 - 0.0883), the
# bottom lip being 0.0883 off the body centre, the lip z range and the
# hole / counterbore heights. Those are kept as measured.
#
# Modelling note: OCCT cannot fillet this part directly. The floor is 4 mm
# with r = 2 rounds on both faces (zero flat left on the back) and the slot
# arcs meet the floor at a 17 deg corner, so BRepFilletAPI aborts. The r = 2
# rounds are therefore built as 3D Minkowski offsets of inset cores
# (`offset(..., kind=Kind.ARC)`) and the body is the intersection of a
# fully-rounded plain plate with a slab whose slot contour is rounded on the
# back face only; the two back inner-top corners get an explicit r = 2 sphere.
# Where the two floor rounds overlap (wall thinner than 4 mm near the slot
# arc/floor junction) this gives the intersection of the two fillets, within
# ~0.02 mm of any CAD kernel's result.
#
# Coordinate frame matches the STL exactly: X across the part (body centre
# x = 0.1607), Y through the thickness (front face y = 58.017, back face
# 73.017), Z up (top of walls z = 44.021, bottom z = -60.779). Units mm.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

# ---- STL frame -----------------------------------------------------------
x0 = 0.16066            # body centre (X)
y_front = 58.01723      # front face (Y); the lips are on this face
z_top = 44.02082        # top of the walls (Z)

# ---- U plate -------------------------------------------------------------
width = 95.0            # overall X
height = 104.8          # overall Z
thick = 15.0            # overall Y
corner_r = 30.0         # outer bottom corners
wall = 7.0              # slot wall thickness (X)
floor_t = 4.0           # slot floor thickness (Z)
slot_arc_r = 25.5302    # slot bottom-corner arc, tangent to the wall ...
slot_arc_h = 28.4084    # ... leaving the wall this far above the bottom
edge_r = 2.0            # fillet on every U edge except the front slot contour

# ---- side-wall through-hole (axis X) -------------------------------------
wall_hole_r = 3.0
wall_hole_y = 7.0       # behind the front face
wall_hole_z = 4.5863    # STL Z

# ---- retaining lips (front face) -----------------------------------------
lip_t = 2.0             # lip thickness (Y)
lip_w = 6.9117          # side lip width (X, from the slot wall inward)
lip_z0 = 11.99782       # side lips run from z = -lip_z0 ...
lip_z1 = 40.00218       # ... to z = +lip_z1   (52 mm)
bot_lip_w = 31.0        # floor lip width (X)
bot_lip_h = 6.0         # floor lip height above the slot floor
bot_lip_cx = 0.0723     # floor lip centre (X); 0.088 left of the body centre

# ---- screw holes in the side lips (axis Y) -------------------------------
screw_r = 1.2           # 2.4 mm clearance through the front skin
screw_cbore_r = 2.4     # 4.8 mm counterbore opening into the slot
screw_skin = 0.6        # skin left at the front face
screw_x = 37.7617       # hole centre from the body centre (|X|)
screw_z = 14.24163      # STL Z

include_lips = True

# ========================================================================
import math

big = 60.0                          # half-size of the helper slab
z_bot = z_top - height
y_back = y_front + thick
half_w = width / 2
slot_half = half_w - wall
z_floor = z_bot + floor_t
z_arc = z_bot + slot_arc_h          # the slot arc leaves the wall here
arc_cx = slot_half - slot_arc_r     # arc centre, |X| from the body centre
# the arc meets the flat floor (not tangent) at |x| = x_junc
theta = math.asin((z_arc - z_floor) / slot_arc_r)
x_junc = arc_cx + slot_arc_r * math.cos(theta)


def box(xa, xb, ya, yb, za, zb):
    """Axis-aligned box between two corners (either order)."""
    return Pos((xa + xb) / 2, (ya + yb) / 2, (za + zb) / 2) * Box(
        abs(xb - xa), abs(yb - ya), abs(zb - za))


def cyl_y(r, x, z, ya, yb):
    return Pos(x, (ya + yb) / 2, z) * Rot(90, 0, 0) * Cylinder(r, yb - ya)


def cyl_x(r, y, z, xa, xb):
    return Pos((xa + xb) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, xb - xa)


def plain_plate(inset, ya, yb):
    """Outer outline (r=30 bottom corners) shrunk by `inset`, y = ya..yb."""
    p = box(x0 - half_w + inset, x0 + half_w - inset, ya, yb,
            z_bot + inset, z_top - inset)
    low = p.edges().filter_by(Axis.Y).filter_by(
        lambda e: e.center().Z < z_bot + inset + 1)
    return fillet(low, corner_r - inset)


def slot_void(grow, ya, yb):
    """The slot (open at the top), dilated outward by `grow` >= 0."""
    s = box(x0 - slot_half - grow, x0 + slot_half + grow, ya, yb,
            z_arc, z_top + 5)
    s += box(x0 - x_junc, x0 + x_junc, ya, yb, z_floor - grow, z_arc + 1)
    clip = box(x0 - big, x0 + big, ya - 1, yb + 1, z_floor - grow, z_top + 6)
    for sg in (-1, 1):
        s += cyl_y(slot_arc_r + grow, x0 + sg * arc_cx, z_arc, ya, yb) & clip
        if grow > 0:   # rolling-ball round at the arc/floor junction
            s += cyl_y(grow, x0 + sg * x_junc, z_floor, ya, yb)
    return s


r = edge_r
# A: the plain plate with every edge rounded (Minkowski: inset core + ball)
plate_round = offset(plain_plate(r, y_front + r, y_back - r), amount=r,
                     kind=Kind.ARC)

# B: a large slab minus the slot, with the slot contour rounded on the back
# face only (the Minkowski result is rounded at both ends; the sharp slot is
# restored for y <= y_back - r).
core_b = box(x0 - big + r, x0 + big - r, y_front + r, y_back - r,
             z_bot - 10 + r, z_top + 10 - r) - slot_void(r, y_front, y_back)
slab_b = offset(core_b, amount=r, kind=Kind.ARC)
slab_b += (box(x0 - big, x0 + big, y_front - 1, y_back - r, z_bot - 10, z_top + 10)
           - slot_void(0, y_front - 2, y_back))

# C: the U outline with its four top corners rounded (the Y-direction rounds
# at the top of each wall), sharp elsewhere.
u_prism = plain_plate(0, y_front - 1, y_back + 1) - slot_void(0, y_front - 2, y_back + 2)
u_prism = fillet(u_prism.edges().filter_by(Axis.Y).filter_by(
    lambda e: e.center().Z > z_top - 1e-3), r)

body = plate_round & slab_b & u_prism

# The two back inner-top corners are where three rounds meet: replace the
# three-cylinder corner with the proper r=2 sphere.
for sg in (-1, 1):
    cx = x0 + sg * (slot_half + r)
    corner = box(cx, cx - sg * (r + 1), y_back - r, y_back + 1,
                 z_top - r, z_top + 1)
    body -= corner - Pos(cx, y_back - r, z_top - r) * Sphere(r)

# ---- side-wall through-hole -----------------------------------------------
body -= cyl_x(wall_hole_r, y_front + wall_hole_y, wall_hole_z,
              x0 - big, x0 + big)

# ---- retaining lips (sharp-edged, on the front face) ----------------------
if include_lips:
    y_lip = y_front + lip_t
    for sg in (-1, 1):
        lip = box(x0 + sg * (slot_half - lip_w), x0 + sg * slot_half,
                  y_front, y_lip, 0 - lip_z0, lip_z1)
        lip -= cyl_y(screw_r, x0 + sg * screw_x, screw_z, y_front - 1, y_lip + 1)
        lip -= cyl_y(screw_cbore_r, x0 + sg * screw_x, screw_z,
                     y_front + screw_skin, y_lip + 1)
        body += lip
    body += box(bot_lip_cx - bot_lip_w / 2, bot_lip_cx + bot_lip_w / 2,
                y_front, y_lip, z_floor, z_floor + bot_lip_h)

show_object(body, name="slot_holder", color="burlywood")
