# Grippers — "Gripper (2) v10": two Gripper 1 jaws stacked along Z.
#
# Reverse-engineered from components/Grippers.step (assembly of Slider:1 =
# four slider blocks, Plate:1 and Plate 2:1 = plate + tab each) with
# `lamad re inspect` / `lamad re det all`.  The upper jaw is exactly
# components/Gripper 1.step (plate z = 27.8485..65.8485, tab above); the
# lower jaw is the SAME geometry mirrored in Z about the mid-plane between
# the two plates (its truss triangles hang from the top, its tab points
# down to z = -41.149), so the two tabs face away from each other.  The
# vendor gap between the facing plate faces is 8.996 mm (9 - 0.004).
#
# The parametric body below is a verbatim copy of components/gripper.py
# (lamad executes a single script file); see that file for the derivation.
# Coordinate frame matches the vendor file.  Units mm.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

# ---- stacking ---------------------------------------------------------------
stack_gap = 8.996        # distance between the two plates' facing faces
include_upper = True
include_lower = True

# ---- vendor frame ---------------------------------------------------------
plate_cx = 15.851        # vendor X of the part centre line
plate_z0 = 27.8485       # vendor Z of the plate bottom

# ---- back plate -----------------------------------------------------------
plate_w = 56.0           # X
plate_h = 38.0           # Z
plate_t = 2.0            # Y (y = -plate_t .. 0)
screw_r = 1.5            # countersunk through holes, 4x
screw_dx = 12.5          # +- from the centre line
screw_z1 = 7.0           # below the plate top
screw_z2 = 27.0
csk_r = 2.75             # 90 deg countersink radius at the +Y face
window_w = 6.015         # window at each side edge of each block, X
window_z0 = 15.22        # above the plate bottom
window_z1 = 25.75

# ---- slider blocks --------------------------------------------------------
block_w = 24.0           # X
block_d = 27.1           # Y (y = 0 .. block_d)
block_gap = 8.0          # between the two blocks
wall_t = 1.0             # side (truss) walls
floor_t = 2.0
front_t = 2.0            # wall fused to the plate (y = 0 .. 2)
back_t = 2.0
slot_w = 12.0            # back-wall slot, centred, floor top .. open top
circle_r = 8.3           # back-wall circular cut-out, centred in X
circle_z = 11.502        # above the block bottom
pin_r = 1.0              # 4 pin holes through the back wall
pin_dx = 8.0             # +- from the block centre
pin_dz = 15.0            # +- from the block mid-height

# ---- tab ------------------------------------------------------------------
tab_w = 14.0             # X, centred on plate_cx
tab_t = 4.0              # Y (y = -2 .. 2 at the base)
tab_h = 22.0             # above the plate top
tab_bend_z = 4.0         # start of the jog (sharp-corner sketch) above base
tab_tip_y = 7.2          # tip front face at y = -tab_tip_y
tab_tip_z = 13.0         # end of the jog (sharp-corner sketch) above base
tab_r_in = 3.0           # fillet on the front (concave) bend corner
tab_r_out = 6.0          # fillet on the back (convex) bend corner
tab_r_tip = 3.35         # fillet on the back corner at the top of the jog
tab_end_r = 6.5          # corner radius of the rounded end
tab_hole_r = 1.5
tab_hole_z = 17.5        # above the plate top
tab_cbore_r = 2.7
tab_cbore_d = 2.0        # from the +Y (block-side) face of the tip

include_tab = True

# ========================================================================
import math

big = 200.0
MIN = (Align.MIN, Align.MIN, Align.MIN)

# Side-wall truss cut-outs, block-local (y, z) mm with y = 0 at the plate's
# back face and z = 0 at the block bottom.  All four walls are identical.
TRUSS_CUTOUTS = [
    # V-notch at the open top, spanning front wall to back wall
    [(2.0, 38.0), (15.258, 28.0687), (25.1, 38.0), (25.1, 40.0), (2.0, 40.0)],
    # trapezoid against the front wall
    [(2.0, 3.5159), (12.9923, 11.556), (12.9923, 25.1854), (2.0, 33.4195)],
    # triangle sitting on the floor
    [(6.1372, 2.0), (20.1936, 2.0), (14.6532, 8.2289)],
    # lower cut-out against the back wall
    [(25.1, 2.0), (25.1, 13.3228), (16.7373, 13.3228), (16.7373, 11.4019)],
    # upper triangle against the back wall
    [(25.1, 24.6456), (25.1, 33.0116), (16.7373, 24.6456)],
]


def box_min(x0, y0, z0, dx, dy, dz):
    return Pos(x0, y0, z0) * Box(dx, dy, dz, align=MIN)


def cyl_y(r, y0, y1, x, z):
    """Cylinder along Y from y0 to y1 at (x, z)."""
    return Pos(x, (y0 + y1) / 2, z) * Rot(-90, 0, 0) * Cylinder(r, y1 - y0)


def cone_y(r0, r1, y0, y1, x, z):
    """Cone along +Y: radius r0 at y0, r1 at y1."""
    return Pos(x, (y0 + y1) / 2, z) * Rot(-90, 0, 0) * Cone(r0, r1, y1 - y0)


def fillet_vertex(face, y, z, r):
    v = face.vertices().filter_by(
        lambda v: abs(v.Y - y) < 1e-6 and abs(v.Z - z) < 1e-6)
    return fillet(v, r)


# ---- one slider block (local: x 0..block_w, y 0..block_d, z 0..plate_h) --
def make_block():
    blk = Box(block_w, block_d, plate_h, align=MIN)
    blk -= box_min(wall_t, front_t, floor_t,
                   block_w - 2 * wall_t, block_d - front_t - back_t, big)
    for pts in TRUSS_CUTOUTS:
        cutter = extrude(Plane.YZ * Polygon(*pts, align=None),
                         block_w / 2 + 1, both=True)
        blk -= Pos(block_w / 2, 0, 0) * cutter
    cx, cz = block_w / 2, plate_h / 2
    blk -= box_min(cx - slot_w / 2, block_d - back_t - 1, floor_t,
                   slot_w, back_t + 2, big)
    blk -= cyl_y(circle_r, block_d - back_t - 1, block_d + 1, cx, circle_z)
    for sx in (-1, 1):
        for sz in (-1, 1):
            blk -= cyl_y(pin_r, block_d - back_t - 1, block_d + 1,
                         cx + sx * pin_dx, cz + sz * pin_dz)
    return blk


def make_gripper():
    """One jaw in a local frame: plate bottom at z = 0, vendor X/Y."""
    # ---- plate + blocks ------------------------------------------------------
    x0 = plate_cx - plate_w / 2
    body = box_min(x0, -plate_t, 0, plate_w, plate_t, plate_h)
    block = make_block()
    block_x0s = (x0, x0 + block_w + block_gap)
    for bx in block_x0s:
        body += Pos(bx, 0, 0) * block

    # windows through plate + front wall at both side edges of each block
    for bx in block_x0s:
        for wx in (bx, bx + block_w - window_w):
            body -= box_min(wx, -plate_t - 1, window_z0,
                            window_w, plate_t + front_t + 2, window_z1 - window_z0)

    # countersunk screw holes (csk opens on the +Y face of the front wall)
    csk_depth = csk_r - screw_r
    for sx in (-1, 1):
        for dz in (screw_z1, screw_z2):
            hx, hz = plate_cx + sx * screw_dx, plate_h - dz
            body -= cyl_y(screw_r, -plate_t - 1, front_t + 1, hx, hz)
            body -= cone_y(screw_r, csk_r + 1, front_t - csk_depth, front_t + 1,
                           hx, hz)

    # ---- tab -------------------------------------------------------------------
    if include_tab:
        h = tab_t / 2
        yt = -tab_tip_y
        prof = Polygon((-h, 0), (-h, tab_bend_z), (yt, tab_tip_z), (yt, tab_h),
                       (yt + tab_t, tab_h), (yt + tab_t, tab_tip_z),
                       (h, tab_bend_z), (h, 0), align=None)
        prof = Plane.YZ * prof
        prof = fillet_vertex(prof, -h, tab_bend_z, tab_r_in)
        prof = fillet_vertex(prof, h, tab_bend_z, tab_r_out)
        prof = fillet_vertex(prof, yt + tab_t, tab_tip_z, tab_r_tip)
        tab = extrude(prof, tab_w / 2, both=True)   # both: fillet may flip normal
        # rounded end: 14 x tab_h outline in XZ with the top corners filleted
        outline = Rectangle(tab_w, tab_h, align=(Align.CENTER, Align.MIN))
        outline = fillet(outline.vertices().filter_by(
            lambda v: v.Y > tab_h - 1e-6), tab_end_r)
        outline = Plane.XZ * outline
        tab &= extrude(outline, big, both=True)
        # through hole + counterbore from the block-side face of the tip
        tab -= cyl_y(tab_hole_r, yt - 1, big, 0, tab_hole_z)
        tab -= cyl_y(tab_cbore_r, yt + tab_t - tab_cbore_d, big, 0, tab_hole_z)
        body += Pos(plate_cx, 0, plate_h) * tab
    return body


# ---- place the two jaws ------------------------------------------------------
jaw = make_gripper()
upper = Pos(0, 0, plate_z0) * jaw
mid_z = plate_z0 - stack_gap / 2            # mirror plane between the plates
lower = mirror(upper, about=Plane.XY.offset(mid_z))
if include_upper:
    show_object(upper, name="gripper_upper", color="steelblue")
if include_lower:
    show_object(lower, name="gripper_lower", color="darkorange")
