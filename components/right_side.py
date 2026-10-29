# Right side wall — parametric reconstruction.
#
# Reverse-engineered from components/Right side.step (one Fusion solid,
# 28 faces) with `lamad re det all` + `lamad re inspect`. The part is the
# right-hand side wall of the tool housing:
#
#   * a 5 mm plate (x 45..50, y -25.399..21) that is a constant profile
#     extruded 71.802 mm along Z (z -31.8..40.002);
#   * above y = 21 both faces of the plate sweep inward (-X) along S-shaped
#     splines into a 13.9 mm wide "hood" whose flat top sits at y = 58.017.
#     The hood carries a 2.4 mm x 11.34 mm blind hole from the top face
#     (x 37.92, z 14.24) and a 1 mm wide, 0.5 mm tall full-round lip on
#     its outer (+X) top corner, blended in with an R2 fillet;
#   * two mirror-image 3 mm mounting tabs (y 5..8) that stick out of the
#     plate's inner (x = 45) face at each Z end: a flat x = 39.38 face,
#     a convex R23.3 outer arc, an R5.03 round where the tab meets the
#     plate, and a 2.9 mm through-hole with a 90 deg countersink (5.5 mm
#     at the y = 8 face).
#
# The two spline faces are degree-5 B-splines with 10 poles on uniform
# knots (Fusion fit-point splines through 6 points). No analytic curve
# (two-arc ogee, Hermite, cosine) reproduces them closer than ~0.1 mm,
# so the vendor poles are kept, normalised by each curve's (dx, dy), and
# re-scaled to whatever endpoints the knobs below give. Both curves share
# the same X pole pattern; their Y poles differ slightly, so each has its
# own table (S_LEFT / S_RIGHT below).
#
# Many hood/tab numbers are solver-derived (58.0172302, 33.7489637, ...);
# clean 'typed' values are 5 / 3 / 21 / 54 / 11.34 / 1.2 / 1.45 / 2.75 /
# 0.5 / 2.0 / 5.0. The measured values are kept so the reconstruction
# matches the STEP. The tab's outer arc meets the plate end at x = 49.9994
# rather than 50.0 in the vendor file; that falls out of the arc centre and
# radius here as well (the slab is a box clipped by the arc cylinder).
#
# Coordinate frame matches the vendor file exactly: plate thickness along X,
# plate height along Y (hood toward +Y), plate length along Z. Units mm.
# Negative frame values (y0 = -25.399, z0 = -31.8) are derived from positive
# knobs because lamad does not pick up negative literals as parameters.
#
# Verification (see components/compare_right_side/): face coverage matches
# all 28 vendor faces both ways at 0.01 mm, the solid volume agrees to
# 1e-4 mm^3, and a mesh-mode compare against a 5 um tessellation of the
# vendor STEP gives mean / p95 / max surface distances of 0.0006 / 0.004 /
# 0.012 mm (chordal noise). A boolean-free IoU from classifying a jittered
# 0.35 mm point grid (3.37 M points) against both solids is 0.99999 (0
# reference-only points, 10 reconstruction-only, all classifier glitches
# on the vendor's B-spline faces). The solid-mode (IoU) compare cannot run
# on this part: OCCT booleans fail on the coincident B-spline faces -- the
# vendor STEP cannot even be booleaned against a second import of itself.
# Sub-micron details matter for the remaining booleans, which is why the
# vendor's 45.0000007 / 21.0000002 / 54.0000007 values are kept verbatim.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

# ---- plate ---------------------------------------------------------------
plate_x0 = 45.0000006705523  # inner (tab-side) face (vendor: 0.67 um off 45)
plate_x1 = 50.0              # outer face (plate is 5 mm thick)
bend_y = 21.0000001937151    # both faces start their S-curve here
plate_y_len = 46.3990001937151  # straight plate below bend_y (bottom y = -25.399)
plate_z1 = 40.002        # +Z end face
plate_z_len = 71.802     # -Z end face at plate_z1 - plate_z_len = -31.8

# ---- hood ----------------------------------------------------------------
hood_x_l = 33.7489636661551  # hood inner face (end of the left S-curve)
hood_x_r = 47.6606595935366  # hood outer face (end of the right S-curve)
hood_top = 58.017230247447   # hood top face
hood_l_y = 54.0000006854534  # left S-curve ends here, then straight up
hood_r_y = 53.5112204550036  # right S-curve ends here, then straight up
lip_r = 0.5              # full-round lip on the outer top corner
lip_fillet_r = 2.0       # fillet blending the lip into the top face
hood_hole_x = 37.922332248671
hood_hole_z = 14.2416324662293
hood_hole_r = 1.2
hood_hole_depth = 11.34  # blind, from the top face

# ---- mounting tabs (both Z ends, mirror images) --------------------------
tab_y0 = 5.0
tab_t = 3.0              # y 5..8
tab_x = 39.3834931133248     # flat face of the tab
tab_len = 16.3360606666852   # how far the tab reaches past the plate end
tab_round_h = 5.0        # the plate/tab round meets the x=45 face this far
#                          inside the plate's Z span; its radius follows from
#                          being tangent to the tab face with its centre
#                          on the plate end plane.
tab_arc_r = 23.2984147977892   # convex outer arc of the tab
tab_arc_cx = 26.9451619090121  # ... centre x
tab_arc_dz = 3.3642959022113   # ... centre z, measured into the plate from its end
tab_hole_x = 44.2892137506599
tab_hole_dz = 5.2436933606308  # hole centre, measured outward from the plate end
tab_hole_r = 1.45        # 2.9 mm through-hole
tab_csk_r = 2.75         # 90 deg countersink, 5.5 mm at the y = 8 face

include_tabs = True
include_hood_hole = True

# ========================================================================
import math

# Normalised poles of the vendor S-curves: (gx, gy) in [0, 1] from the
# plate end (bend_y) to the hood end of each curve. Degree 5, knots
# 0, .2, .4, .6, .8, 1 with multiplicities 6,1,1,1,1,6.
S_GX = (0.0, 0.0, 0.020420288834, 0.112248156062, 0.332992408989,
        0.667007591010, 0.887751843938, 0.979579711166, 1.0, 1.0)
S_LEFT_GY = (0.0, 0.044205061044, 0.130468469104, 0.253430107555,
             0.407044275264, 0.592955724736, 0.746569892445,
             0.869531530896, 0.955794938956, 1.0)
S_RIGHT_GY = (0.0, 0.046544562277, 0.136292640532, 0.260901997467,
              0.410963383810, 0.589036616190, 0.739098002533,
              0.863707359468, 0.953455437723, 1.0)

x0 = plate_x0
x1 = plate_x1
y0 = bend_y - plate_y_len
z1 = plate_z1
z0 = plate_z1 - plate_z_len


def s_curve(p0, p1, gy, z):
    """Degree-5 B-spline from p0 to p1 (XY, at height z) with the vendor
    pole pattern scaled to the endpoints. Vertical tangents at both ends."""
    poles = [(p0[0] + gx * (p1[0] - p0[0]), p0[1] + g * (p1[1] - p0[1]), z)
             for gx, g in zip(S_GX, gy)]
    spans = len(poles) - 5
    knots = [0.0] * 6 + [i / spans for i in range(1, spans)] + [1.0] * 6
    return Edge.make_bspline(poles, knots, 5)


def cyl_y(r, ya, yb, x, z):
    """Cylinder of radius r along +Y from ya to yb through (x, *, z)."""
    return Pos(x, (ya + yb) / 2, z) * Rot(90, 0, 0) * Cylinder(r, yb - ya)


# ---- plate + hood profile (XY at z = z0), extruded along +Z ---------------
# lip geometry: full round of radius lip_r centred on the top face at the
# outer corner; the R lip_fillet_r fillet is tangent to the top face and
# externally tangent to that round.
lip_cx = hood_x_r - lip_r
fil_cx = lip_cx - math.sqrt((lip_fillet_r + lip_r) ** 2 - lip_fillet_r ** 2)
fil_cy = hood_top + lip_fillet_r
k = lip_fillet_r / (lip_fillet_r + lip_r)
tangent = (fil_cx + k * (lip_cx - fil_cx), fil_cy + k * (hood_top - fil_cy))
a_mid = (math.atan2(hood_top - fil_cy, lip_cx - fil_cx) - math.pi / 2) / 2
fil_mid = (fil_cx + lip_fillet_r * math.cos(a_mid),
           fil_cy + lip_fillet_r * math.sin(a_mid))


def P(x, y):
    return (x, y, z0)


profile = [
    Line(P(x1, y0), P(x0, y0)),
    Line(P(x0, y0), P(x0, bend_y)),
    s_curve((x0, bend_y), (hood_x_l, hood_l_y), S_LEFT_GY, z0),
    Line(P(hood_x_l, hood_l_y), P(hood_x_l, hood_top)),
    Line(P(hood_x_l, hood_top), P(fil_cx, hood_top)),
    ThreePointArc(P(fil_cx, hood_top), P(*fil_mid), P(*tangent)),
    ThreePointArc(P(*tangent), P(lip_cx, hood_top + lip_r), P(hood_x_r, hood_top)),
    Line(P(hood_x_r, hood_top), P(hood_x_r, hood_r_y)),
    s_curve((x1, bend_y), (hood_x_r, hood_r_y), S_RIGHT_GY, z0),
    Line(P(x1, bend_y), P(x1, y0)),
]
face = Face(Wire(profile))
wall = extrude(face, amount=plate_z_len, dir=(0, 0, 1))

if include_hood_hole:
    wall -= cyl_y(hood_hole_r, hood_top - hood_hole_depth, hood_top + 1,
                  hood_hole_x, hood_hole_z)


# ---- mounting tabs -------------------------------------------------------
def make_tab(z_end, sgn):
    """Tab at plate end z_end, reaching sgn*tab_len beyond it (sgn = -1 for
    the -Z end, +1 for the +Z end)."""
    ya, yb = tab_y0, tab_y0 + tab_t
    ym = (ya + yb) / 2
    # flat-faced slab clipped by the convex outer arc
    zc = (z_end + sgn * tab_len + z_end) / 2
    slab = Pos((tab_x + x1) / 2, ym, zc) * Box(x1 - tab_x, tab_t, tab_len)
    slab &= cyl_y(tab_arc_r, ya - 1, yb + 1, tab_arc_cx, z_end - sgn * tab_arc_dz)
    # round between the tab face and the plate: tangent to x = tab_x, centre
    # on the plate end plane, passing through (x0, z_end - sgn*tab_round_h),
    # i.e. it lies inside the plate's Z span, on the plate's x = x0 face
    w = x0 - tab_x
    r_round = (w * w + tab_round_h ** 2) / (2 * w)
    rnd = cyl_y(r_round, ya, yb, tab_x + r_round, z_end)
    clip = Pos((tab_x + x1) / 2, ym, z_end - sgn * (r_round + 1) / 2) * \
        Box(x1 - tab_x, tab_t + 2, r_round + 1)
    tab = slab + (rnd & clip)
    # countersunk through-hole, countersink opening on the y = yb face
    hz = z_end + sgn * tab_hole_dz
    tab -= cyl_y(tab_hole_r, ya - 1, yb + 1, tab_hole_x, hz)
    csk_d = tab_csk_r - tab_hole_r          # 90 deg countersink
    cone = (Pos(tab_hole_x, yb - csk_d / 2, hz) * Rot(-90, 0, 0)
            * Cone(tab_hole_r, tab_csk_r, csk_d))
    tab -= cone
    tab -= cyl_y(tab_csk_r, yb, yb + 1, tab_hole_x, hz)
    return tab


if include_tabs:
    wall += make_tab(z0, -1)
    wall += make_tab(z1, +1)

show_object(wall, name="right_side", color="steelblue")
