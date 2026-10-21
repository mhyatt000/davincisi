# Tool holder. Copied from ../../components/tool_slot_selection.py on
# 2026-10-19 for the simple variant;
# edit freely here, the original is left untouched.
#
# Simple-variant changes (names: bottom = the 80 x 100.3 face nearest the
# mount, i.e. the y_front face; front = the curved hull of the U; sides =
# the two arms; back = the open end of the U, with the top bar):
#   * no fillets or rounds on the outline: the R2 / R1 edge fillets and the
#     R2 top corners of the original are gone, all outer edges are sharp.
#   * flat bottom, for printing bottom-down: the original's 1.5 mm side-wall
#     recess (with its R5.5 round) and 45 deg under-wall chamfer are gone, and
#     the top bar at the back reaches the bottom face (no 45 deg lead-in
#     funnel under it, so no 52 mm bridge). The bottom face is one plane with
#     only the through-window in it.
#   * no side holes: the two 3.8 mm blind holes in the outer side faces are
#     gone.
#   * two dovetail pins on the tower's dovetail-pin line, from the tower's
#     own pin out to the mount, each joined to the holder by a 6 mm x 8 mm
#     strap; see "dovetail pins" (construction lines named in
#     ../sketches/tool_dovetail.py).
#   * the snap-tab pockets run down through the bottom face (the original
#     pockets stopped at y = 6.5), so nothing is left under either tab; the
#     tabs themselves are unchanged.
#
# Tool slot selection — parametric reconstruction from an STL mesh.
#
# Reverse-engineered from components/Tool slot selection.stl (2924 tris,
# watertight) with trimesh: coplanar-facet listing + plane sections + circle
# fits. `lamad re det/inspect/measure` are STEP-only, so every number below
# comes from the mesh (planes are exact in a Fusion STL export; arcs were
# least-squares fitted to the facet vertices).
#
# WHAT IT IS: a 3D-printed tool-holder frame, 80 x 20 x 100.3 mm. A flat
# plate (20 mm thick in Y) with a large through-window: 61 mm wide at the
# top, a V-shaped lower cavity (two tangent arcs + a 25 deg flank) ending in
# a 36 mm flat floor. The outer outline is a rectangle with a rounded
# "boat hull" bottom (two arcs with a kink at the junction). Features:
#   * a 2.5 mm top bar bridging the window at y 5.0..7.5 with a 45 deg
#     lead-in funnel on the front and a 5 x 2.5 slope on the back (this copy:
#     bar runs y 0..7.5, no funnel);
#   * the back half (y 10..20) of the window is 4.6 mm wider, with an extra
#     7 mm wide widening at y 10..14 whose floor slopes 68 deg;
#   * two cantilever snap tabs (3.0 x 16 x 1.17 mm) hanging in pockets in
#     the side walls at y 6.5..10 with a shallow R4.4 detent bump;
#   * a 1.5 mm front recess over the side walls below z = -0.6 (R5.5 round
#     into the front face) and a 45 deg chamfer under the wall bottoms, both
#     sparing a 63 mm wide central lobe (removed in this copy);
#   * a 2.7 mm deep trough with R14.3 sides in the cavity floor, open to
#     the back face, with a 23 deg front wall;
#   * one 3.8 mm x 7 mm deep blind hole in each outer side face (heat-set
#     insert / pin) at y 5, z 4.6 (removed in this copy);
#   * (original only) R2 fillets on the top/side edges of both faces, R1 on
#     the hull edges -- removed in this copy, see above.
#
# Mesh-mode compare (lamad re compare, 20k samples): mean 0.005 mm, p95
# 0.033 mm both ways; max 0.15 mm script->STL. The 0.64 mm STL->script max
# is a degenerate 2 um thick sheet in the STL at the trough wall (x' = +-9.7)
# and not a feature. B-rep volume 38636 vs 38640 mm^3.
#
# COORDINATE FRAME matches the STL exactly: X across the width (centre at
# x = 0.1605), Y through the thickness (front face y = 60.017, back face
# y = 80.017), Z up (top z = 43.752, bottom z = -56.579). The script builds
# in a local frame (x' = x - 0.1605, y' = y - 60.017, z unchanged) and
# translates at the end. Depth-type knobs are given as positive numbers
# (z = -depth) because negative literals are not picked up as --param.
#
# Clean typed numbers found: 80, 20, 2.0/1.0 fillets, 1.5 recess, 5.5
# round, 5.0/7.5 bar, 45 deg funnel, 10.0 wall split, 14.0, 16 x 3 tab,
# 0.3/0.4 gaps, 2.7 trough depth, 3.8 x 7 hole, 1.0 tab inset. Everything
# else (cavity widths 60.967 / 65.559 / 70.592, arc radii 80.5 / 68.4 /
# 22.97 / 9.84 / 14.3, odd z levels) is as-measured and presumably driven
# by the tool the slot was designed around.

# ---- dovetail pins (this copy) -------------------------------------------
# Same frame as ../components/tower.py (both are the original assembly's
# frame), so the tower's pin numbers carry over: the pins run along Z at
# x = 0 with the nominal dovetail.py profile, wide face at y = pin_tip_y and
# narrow face 10 mm higher. They start at the tower's pin (|z| =
# tower_pin_half) and end at the mount, trimmed by a lofted surface: its
# bottom edge is half of the mount's circle (radius mount_r about the mount
# axis x = 0, z = 0) at the pins' tip, its top edge is the holder's OUTER edge
# on its base -- the curved hull at the front, the flat back edge at the back
# -- so the pin ends lean out along the mount_outer construction lines. A
# strap joins each pin to the holder: the loft's side surface thickened
# strap_t inward, kept only within a strap_w wide box (centred on the pin)
# from the dovetail's narrow top face upward. strap_w matches the tower's
# baseplate channel so the straps pass through it. Body, straps and pins are
# fused into one part.
include_pins = True
strap_t = 6.0           # strap thickness, inward from the loft surface (= tower.py end_cut_inset)
strap_w = 8.0           # strap width; tower.py block_gap (its baseplate channel)
pin_tip_y = 4.508       # tower.py: baseplate_y0 - rib_d - dovetail_height
tower_pin_half = 18.715 # tower.py: base_gap/2 + window_z0 - jst_chamfer
mount_r = 37.5          # dovetail_mount.py: disc_r

# ---- STL frame -----------------------------------------------------------
x_center = 0.1605       # x of the symmetry plane in the STL
y_front = 60.017        # front face (y) in the STL

# ---- outer body ----------------------------------------------------------
width = 80.0
thick = 20.0            # Y thickness
z_top = 43.752
kink_depth = 30.227     # straight sides end at z = -30.227 (sharp kink)
side_arc_r = 80.46      # hull side arcs (not tangent to the sides)
junction_x = 27.5865    # where the side arcs meet the bottom arc (sharp)
junction_depth = 50.77
bottom_depth = 56.579   # lowest point of the bottom arc (z = -56.579)

# ---- through-window (cavity) ---------------------------------------------
cav_half = 30.4835      # upper window half-width, y 0..10 (60.967 wide)
cav_top = 36.458        # window ceiling under the top bar
step_depth = 1.83       # window starts widening at z = -1.83 ...
step_half = 32.7795     # ... to this half-width (also y 10..20 width)
step_bot = 9.514        # widening slope ends at z = -9.514
wall_bot = 14.232       # vertical wall ends at z = -14.232
bump_mid_x = 33.0035    # small R2.3 convex bump below the wall (3 points)
bump_mid_depth = 15.125
bump_end_x = 33.2485
bump_end_depth = 15.518
inner_arc_cx = 10.444   # upper cavity arc (R22.97), centre (10.444, -12.719)
inner_arc_cdepth = 12.719
inner_arc_r = 22.97
corner_cx = 11.71       # lower corner arc (R9.84), centre (11.71, -40.68)
corner_cdepth = 40.68
corner_r = 9.84
floor_half = 18.07      # flat cavity floor, 36.14 wide
floor_depth = 48.187    # cavity floor z = -48.187

# ---- top bar / funnel (z above cav_top) ----------------------------------
bar_back_y = 7.492      # top bar spans y 0..bar_back_y (from the bottom face)
bar_half_back = 25.9955
back_slope_run = 5.0    # back slope widens by this between bar_back_y..split_y
split_y = 10.0          # front/back cavity profiles change here
widen_half = 35.296     # extra widening y split_y..widen_y1 (70.59 wide)
widen_y1 = 14.0
widen_floor_z0 = 2.753  # widening floor z at y = split_y ...
widen_floor_z1 = 12.783 # ... and at y = widen_y1 (68 deg slope)

# ---- snap tabs in the side walls -----------------------------------------
tab_inset = 1.0         # tab inner face is 1.0 mm outboard of cav_half
tab_w = 3.008
tab_gap = 0.3           # side clearance in the pocket
tab_gap_bot = 0.4       # bottom clearance
tab_t = 1.167           # tab thickness (y)
tab_z0 = 10.6
tab_z1 = 26.6           # tab roots into the pocket ceiling here
bump_r = 4.4            # detent bump on the tab's cavity face
bump_protrude = 0.416
bump_z = 12.462

# ---- floor trough (open to the back face) --------------------------------
trough_depth = 50.887   # trough floor z = -50.887 (2.7 below the cavity floor)
trough_flat_half = 9.7
trough_r = 14.3         # sides blend into the cavity floor at floor_half
trough_y0 = 12.704      # front wall meets the cavity floor here ...
trough_y1 = 13.849      # ... and the trough floor here (23 deg wall)

# ========================================================================
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dovetail import dovetail_height, dovetail_sketch  # noqa: E402

BIG = 60.0


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(
        x1 - x0, y1 - y0, z1 - z0)


def cyl_x(r, x0, x1, y, z):
    """Cylinder with its axis along X from x0 to x1 at (y, z)."""
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def P(x, z):
    return Vector(x, 0, z)


def arc_on(c, r, a, b):
    """ThreePointArc from a to b along the circle (centre c, radius r),
    taking the shorter way round (points in the XZ plane)."""
    a0 = math.atan2(a.Z - c.Z, a.X - c.X)
    a1 = math.atan2(b.Z - c.Z, b.X - c.X)
    d = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    am = a0 + d / 2
    return ThreePointArc(a, P(c.X + r * math.cos(am), c.Z + r * math.sin(am)), b)


def radius_arc(a, b, r, hint):
    """Arc a->b of radius r whose centre is the candidate closer to hint."""
    mx, mz = (a.X + b.X) / 2, (a.Z + b.Z) / 2
    cx, cz = b.X - a.X, b.Z - a.Z
    L = math.hypot(cx, cz)
    h = math.sqrt(max(r * r - (L / 2) ** 2, 0.0))
    nx, nz = -cz / L, cx / L
    cands = [P(mx + h * nx, mz + h * nz), P(mx - h * nx, mz - h * nz)]
    c = min(cands, key=lambda q: math.hypot(q.X - hint.X, q.Z - hint.Z))
    return arc_on(c, r, a, b)


def face_xz(edges):
    return make_face(edges)


def prism_y(face, y0, y1):
    """Extrude an XZ-plane face along +Y from y0 to y1."""
    return Pos(0, y0, 0) * extrude(face, amount=y1 - y0, dir=(0, 1, 0))


def prism_x(face, x0, x1):
    return Pos(x0, 0, 0) * extrude(face, amount=x1 - x0, dir=(1, 0, 0))


def mirror_x(p):
    return P(-p.X, p.Z)


# ---- outer outline (XZ) --------------------------------------------------
hw = width / 2
K = P(hw, -kink_depth)
J = P(junction_x, -junction_depth)
B = P(0, -bottom_depth)
outline = [
    Line(P(-hw, -kink_depth), P(-hw, z_top)),
    Line(P(-hw, z_top), P(hw, z_top)),
    Line(P(hw, z_top), K),
    radius_arc(K, J, side_arc_r, P(0, 0)),
    ThreePointArc(J, B, mirror_x(J)),
    radius_arc(mirror_x(J), mirror_x(K), side_arc_r, P(0, 0)),
]
body = prism_y(face_xz(outline), 0, thick)

# ---- cavity profiles (XZ) ------------------------------------------------
C1 = P(inner_arc_cx, -inner_arc_cdepth)
C2 = P(corner_cx, -corner_cdepth)
# external tangent of the two arcs on the +x side: unit normal n with
# n.(C1 - C2) = r2 - r1
dx, dz = C1.X - C2.X, C1.Z - C2.Z
L = math.hypot(dx, dz)
phi = math.atan2(dz, dx)
ang = phi - math.acos((corner_r - inner_arc_r) / L)
n = (math.cos(ang), math.sin(ang))
if n[0] < 0:
    ang = phi + math.acos((corner_r - inner_arc_r) / L)
    n = (math.cos(ang), math.sin(ang))
T1 = P(C1.X + inner_arc_r * n[0], C1.Z + inner_arc_r * n[1])
T2 = P(C2.X + corner_r * n[0], C2.Z + corner_r * n[1])
P_wall = P(step_half, -wall_bot)
P_bmid = P(bump_mid_x, -bump_mid_depth)
P_bend = P(bump_end_x, -bump_end_depth)
P_floor = P(floor_half, -floor_depth)


def lower_cavity_edges():
    """Right side top-down from P_wall to the floor, then the mirror."""
    right = [
        ThreePointArc(P_wall, P_bmid, P_bend),
        arc_on(C1, inner_arc_r, P_bend, T1),
        Line(T1, T2),
        arc_on(C2, corner_r, T2, P_floor),
        Line(P_floor, mirror_x(P_floor)),
    ]
    C1m, C2m = mirror_x(C1), mirror_x(C2)
    left = [
        arc_on(C2m, corner_r, mirror_x(P_floor), mirror_x(T2)),
        Line(mirror_x(T2), mirror_x(T1)),
        arc_on(C1m, inner_arc_r, mirror_x(T1), mirror_x(P_bend)),
        ThreePointArc(mirror_x(P_bend), mirror_x(P_bmid), mirror_x(P_wall)),
    ]
    return right + left


front_profile = [
    Line(P(-cav_half, cav_top), P(cav_half, cav_top)),
    Line(P(cav_half, cav_top), P(cav_half, -step_depth)),
    Line(P(cav_half, -step_depth), P(step_half, -step_bot)),
    Line(P(step_half, -step_bot), P_wall),
    *lower_cavity_edges(),
    Line(mirror_x(P_wall), P(-step_half, -step_bot)),
    Line(P(-step_half, -step_bot), P(-cav_half, -step_depth)),
    Line(P(-cav_half, -step_depth), P(-cav_half, cav_top)),
]
back_profile = [
    Line(P(-step_half, z_top + 5), P(step_half, z_top + 5)),
    Line(P(step_half, z_top + 5), P_wall),
    *lower_cavity_edges(),
    Line(mirror_x(P_wall), P(-step_half, z_top + 5)),
]
body -= prism_y(face_xz(front_profile), -1, split_y)
body -= prism_y(face_xz(back_profile), split_y, thick + 1)

# ---- top bar: back slope (z above the window ceiling) --------------------
z_hi = z_top + 5
slope = Polygon((-bar_half_back, bar_back_y), (bar_half_back, bar_back_y),
                (bar_half_back + back_slope_run, split_y),
                (bar_half_back + back_slope_run, split_y + 0.5),
                (-bar_half_back - back_slope_run, split_y + 0.5),
                (-bar_half_back - back_slope_run, split_y), align=None)
body -= Pos(0, 0, cav_top) * extrude(slope, amount=z_hi - cav_top)

# ---- extra widening at y split_y..widen_y1 with a sloped floor -----------
widen = Plane.YZ * Polygon((split_y, widen_floor_z0), (widen_y1, widen_floor_z1),
                           (widen_y1, z_hi), (split_y, z_hi), align=None)
body -= extrude(widen, amount=widen_half, both=True)

# ---- snap tabs -----------------------------------------------------------
for s in (1, -1):
    xi = cav_half + tab_inset            # tab inner face
    xo = xi + tab_w                      # tab outer face
    # pocket open through the bottom face (y = 0), nothing under the tab
    pocket = box(min(s * (xi - tab_gap), s * (xo + tab_gap)),
                 max(s * (xi - tab_gap), s * (xo + tab_gap)),
                 -1, split_y + 0.5, tab_z0 - tab_gap_bot, tab_z1)
    body -= pocket
    tab = box(min(s * xi, s * xo), max(s * xi, s * xo),
              split_y - tab_t, split_y, tab_z0, tab_z1)
    bump = cyl_x(bump_r, min(s * xi, s * xo), max(s * xi, s * xo),
                 split_y + bump_protrude - bump_r, bump_z)
    bump &= box(-BIG, BIG, split_y, split_y + 1, -BIG, BIG)
    body += tab + bump

# ---- floor trough --------------------------------------------------------
Ct = P(trough_flat_half, -trough_depth + trough_r)
Pf = P(floor_half, -floor_depth)
Pt = P(trough_flat_half, -trough_depth)
trough_xz = [
    Line(mirror_x(Pf), P(-floor_half, -floor_depth + 10)),
    Line(P(-floor_half, -floor_depth + 10), P(floor_half, -floor_depth + 10)),
    Line(P(floor_half, -floor_depth + 10), Pf),
    arc_on(Ct, trough_r, Pf, Pt),
    Line(Pt, mirror_x(Pt)),
    arc_on(mirror_x(Ct), trough_r, mirror_x(Pt), mirror_x(Pf)),
]
trough = prism_y(face_xz(trough_xz), trough_y0 - 1, thick + 1)
trough_yz = Plane.YZ * Polygon((trough_y0, -floor_depth + 10), (trough_y0, -floor_depth),
                               (trough_y1, -trough_depth), (trough_y1, -BIG),
                               (thick + 1, -BIG), (thick + 1, -floor_depth + 10), align=None)
trough &= extrude(trough_yz, amount=BIG, both=True)
body -= trough
# ---- into the STL frame ---------------------------------------------------
body = Pos(x_center, y_front, 0) * body

# ---- dovetail pins (STL frame; not fused to the body) --------------------
def circle_arc(r, a0, a1):
    """Arc of the mount circle in the XZ plane (y = 0), angles in degrees from
    +X; the front (-Z) is at +90, the back (+Z) at +270."""
    def pt(a):
        a = math.radians(a)
        return Vector(r * math.cos(a), 0, -r * math.sin(a))
    return ThreePointArc(pt(a0), pt((a0 + a1) / 2), pt(a1))


def pin_end_sections(front):
    """Matching edge lists (bottom, top) for the pin-end loft, placed in the
    STL frame, without the closing z = 0 lines. Bottom: half the mount circle
    at the pins' tip, split at the angles of the holder outline's corners so
    each arc lofts to its matching outline edge. Top: the holder's outer
    outline on its base (curved hull at the front, flat back edge at the back)."""
    if front:
        a_k = math.degrees(math.atan2(kink_depth, hw))            # side straight | side arc
        a_j = math.degrees(math.atan2(junction_depth, junction_x))  # side arc | hull arc
        cuts = [180, 180 - a_k, 180 - a_j, a_j, a_k, 0]
        top = [Line(P(-hw, 0), mirror_x(K)),
               radius_arc(mirror_x(K), mirror_x(J), side_arc_r, P(0, 0)),
               ThreePointArc(mirror_x(J), B, J),
               radius_arc(J, K, side_arc_r, P(0, 0)),
               Line(K, P(hw, 0))]
    else:
        a_c = math.degrees(math.atan2(z_top, hw))                 # back corners
        cuts = [180, 180 + a_c, 360 - a_c, 360]
        top = [Line(P(-hw, 0), P(-hw, z_top)),
               Line(P(-hw, z_top), P(hw, z_top)),                  # flat back edge
               Line(P(hw, z_top), P(hw, 0))]
    bottom = [Pos(0, pin_tip_y, 0) * circle_arc(mount_r, a0, a1) for a0, a1 in zip(cuts, cuts[1:])]
    top = [Pos(x_center, y_front, 0) * e for e in top]
    return bottom, top


def pin_end_keep(front):
    """Solid lofted between the pin-end sections, closed along z = 0; a pin
    is trimmed to the inside of it."""
    bottom, top = pin_end_sections(front)
    close = lambda edges: Line(edges[-1] @ 1, edges[0] @ 0)
    return loft([Face(Wire(bottom + [close(bottom)])), Face(Wire(top + [close(top)]))],
                ruled=True)


def loft_wall(front, samples=40):
    """The loft's side surface thickened strap_t inward (open at top, bottom
    and z = 0): pin_end_keep minus an inner loft. Each ruling of the loft
    (matching points on a bottom/top edge pair) is moved strap_t along the
    surface normal and cut back to the two planes; the inner loft runs
    through the moved rulings."""
    bottom, top = pin_end_sections(front)
    inner_lo, inner_hi = [], []
    for eb, et in zip(bottom, top):
        for i in range(samples + (eb is bottom[-1])):
            u = i / samples
            pb, pt = eb @ u, et @ u
            g = pt - pb
            n = (eb % u).cross(g).normalized()
            if n.dot(Vector(-pb.X, 0, -pb.Z)) < 0:     # point toward the mount axis
                n = -n
            qb, qt = pb + n * strap_t, pt + n * strap_t
            at = lambda y: qb + (qt - qb) * ((y - qb.Y) / (qt.Y - qb.Y))
            inner_lo.append(at(pin_tip_y))
            inner_hi.append(at(y_front))
    for pts in (inner_lo, inner_hi):                  # ends back onto the z = 0 plane
        for j in (0, -1):
            pts[j] = Vector(pts[j].X, pts[j].Y, 0)
    inner = loft([Face(Polyline(*inner_lo, close=True)), Face(Polyline(*inner_hi, close=True))],
                 ruled=True)
    return pin_end_keep(front) - inner


def strap(front):
    """The part of loft_wall in line with the pin: a strap_w x full-length
    rectangle on the dovetail's narrow top face, extruded 0.5 m upward."""
    y0 = pin_tip_y + dovetail_height                  # the dovetail's narrow top face
    column = Pos(0, y0 + 250, 0) * Box(strap_w, 500, 4 * BIG)
    return loft_wall(front) & column


if include_pins:
    profile = Pos(0, pin_tip_y, 0) * dovetail_sketch(clearance=0)
    for front, z0, z1 in ((True, -bottom_depth, -tower_pin_half),
                          (False, tower_pin_half, z_top)):
        pin = Pos(0, 0, z0) * extrude(profile, amount=z1 - z0)
        body += (pin & pin_end_keep(front)) + strap(front)

show_object(body, name="body", color="burlywood")
