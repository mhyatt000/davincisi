# Left side (microcont) — parametric reconstruction.
#
# Reverse-engineered from components/Left side (microcont).step with
# `lamad re det all` + `lamad re inspect` + x-plane slices. One solid:
#
#   * a 5 mm side-wall plate (vendor x = -50..-45) that runs straight for
#     y = -25.4 .. 21 and then continues as an S-curved panel to y = 58.0
#     (two degree-5 B-spline faces); the panel thickens from 5 mm to 13.9 mm
#     at its end face, which carries a 2.4 mm tapped hole (M2.5 minor) and a
#     small r0.5 bead / r2 fillet lip on its inner edge;
#   * two mirror-image mounting tabs (3 mm thick, y = 5..8) hanging past the
#     plate's top and bottom edges, each with a countersunk 2.9 mm hole;
#   * on the back (vendor -x) a 12.5 mm tall microcontroller enclosure frame:
#     30.4 x 71.8 outer, 2.5 mm walls with r2 corners, a 25.4 x 56 cavity,
#     thick end bars with four 1.8 mm self-tap holes on a 20.5 x 61.5 grid
#     (r2.75 half bosses, 1 mm r1.4 counterbore at the top, 45 deg cone),
#     a 3 mm board ledge, a 1.5 mm lid rim, an 8 mm wide connector (USB)
#     window through the +z bar and a 12 x 3.5 x 2.5 pocket in the -z bar.
#     Every edge of the frame's base face is 0.5 mm x 45 deg chamfered,
#     which is why the cavity and the hole bottoms flare out at the plate.
#
# Coordinate frame: the vendor STEP frame, built directly (no mirror: OCCT
# reflections break later booleans). All x knobs are given as positive
# "x-prime" depths, x' = -x_vendor, and negated by X() when placed: plate
# back face at vendor x = -50 (x' = 50), tabs toward +x (smaller x'), frame
# toward -x (larger x'), part centred on z = 4.101. Units mm.
#
# Findings: the frame's design numbers are clean (30.4, 71.8, 25.4, 56,
# 20.5, 61.5, 2.5, ...) but the STEP has the whole frame scaled by
# 0.999975748 about the plate face (every radius: 1 -> 0.999975748,
# 2 -> 1.999951495, 12.5 -> 12.499696845); `frame_scale` reproduces that
# exactly so the faces coincide for booleans. The plate/tab/panel numbers
# (40.002, 58.0172..., 39.3835..., 23.2984...) are solver-derived and kept
# at full precision. The vendor chamfer on the frame's outer base edge stops
# short for y = -8.9 .. 3.0 at both z ends (two tiny r2.5 cone slivers,
# 0.7 mm^2 each); here the chamfer runs the full loop (~3.7 mm^3 difference).
#
# Compare note: the vendor solid is not a valid OCCT boolean argument
# (BRepAlgoAPI_Check: BOPAlgo_SelfIntersect — the vertex where that partial
# chamfer ends, (-50, -8.8607, 40.002), lies on the plate's back-top edge
# without splitting it), so `lamad re compare` against the raw STEP returns
# an empty intersection. compare_left_side/repair_reference.py splits that
# edge (geometry untouched) and writes vendor_repaired_ref.step; against it
# the script scores IoU 0.99993 (missing 3.7 mm^3 = the chamfer gap above,
# extra 0).
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

# ---- plate ---------------------------------------------------------------
plate_back_x = 50.0       # x' of the plate's back (frame-side) face
plate_t = 5.0             # plate thickness (front face at x' = 45)
plate_y_back = 25.399     # plate starts at y = -plate_y_back
plate_z_top = 40.002      # top face
plate_h = 71.802          # height; bottom face at plate_z_top - plate_h

# ---- curved panel (continuation of the plate toward +y) ------------------
panel_y0 = 21.0           # straight part ends / splines start
panel_y_end = 58.017230247  # panel end face
panel_out_x = 33.4276444790818  # x' of the outer (front) face at the end
panel_in_x = 47.3393404064634   # x' of the inner (back) face at the end
panel_out_straight = 4.017  # outer face is straight for this much before the end
panel_in_straight = 4.506   # inner face likewise
lip_bead_r = 0.5          # bead on the inner edge of the end face
lip_fillet_r = 2.0        # fillet blending the bead into the end face
end_hole_r = 1.2          # tapped hole in the panel end face (M2.5 minor)
end_hole_x = 37.601013062 # x' of that hole
end_hole_z = 14.241632466
end_hole_depth = 11.34

# ---- mounting tabs (mirror pair about the plate's z centre) --------------
tab_y0 = 5.0              # tab lies on y = tab_y0 .. tab_y0 + tab_t
tab_t = 3.0
tab_edge_x = 39.3834924427726  # x' of the tab's free edge (toward the front)
tab_gusset_h = 5.0        # gusset arc climbs this far up the plate face
tab_arc_r = 23.298414798  # big corner arc, free edge -> plate bottom face
tab_arc_cx = 26.945161238 # x' of that arc's centre
tab_arc_cz = 3.364295902  # arc centre this far inboard of the plate edge
tab_hole_x = 44.2892130801077
tab_hole_drop = 5.2436933606308  # hole centre past the plate edge
tab_hole_r = 1.45         # 2.9 mm clearance (M2.5)
tab_csk_r = 2.75          # 90 deg countersink on the outer (y = 8) face

# ---- microcontroller frame (on the plate back, nominal numbers) ----------
frame_scale = 0.999975748 # vendor scale on every frame length (see above)
frame_zc = 4.102827528    # frame centre line (vendor)
frame_y_front = 5.000306436  # frame's +y outer face (vendor)
frame_h = 12.5            # x' = plate_back_x .. plate_back_x + frame_h
frame_w = 30.4            # y extent
frame_len = 71.8          # z extent
frame_corner_r = 2.0
wall = 2.5
rim_h = 1.5               # lid rim: only the 2.5 walls remain this far down
ledge_h = 3.0             # board ledge: full end bars this far up the floor
cavity_len = 56.0         # cavity z extent (bars tangent to the bosses)
cavity_r = 1.0
base_chamfer = 0.5        # 45 deg chamfer on every edge of the base face
hole_dy = 20.5            # mounting hole grid
hole_dz = 61.5
hole_r = 0.9              # 1.8 mm self-tap
hole_cb_r = 1.4           # counterbore at the bar top, 45 deg cone below
hole_cb_depth = 1.0
boss_r = 2.75
usb_w = 8.0               # connector window through the +z bar
usb_depth = 4.0           # measured from the rim top
usb_r = 1.0
pocket_w = 12.0           # blind pocket in the -z bar's outer face
pocket_depth = 3.5        # measured from the rim top
pocket_z = 2.5
pocket_r = 2.0
rim_round_r = 1.0         # rounds where the window/pocket meet the rim

# ========================================================================
import math
from OCP.Geom import Geom_BSplineCurve
from OCP.collections import Array1_gp_Pnt, Array1_double, Array1_int
from OCP.gp import gp_Pnt
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge

big = 200.0


def X(xp):
    """local x' (positive depth) -> vendor x"""
    return -xp


plate_front_x = plate_back_x - plate_t
plate_z0 = plate_z_top - plate_h
zc = plate_z_top - plate_h / 2          # plate centre: tabs mirror about it

# Vendor spline poles (degree 5, uniform clamped knots), in local x'. They
# are normalised to the vendor end points and re-mapped to the knobs above,
# so moving the ends stretches the curve affinely.
_OUTER_POLES = [
    (45.0, 21.0),
    (45.0, 22.4563878081016),
    (44.7636891577788, 25.2995411651542),
    (43.7010244314877, 29.3556206942441),
    (41.1464934574065, 34.4285521322549),
    (37.2811510216754, 40.5716781151933),
    (34.7266200475942, 45.6446095532036),
    (33.663955321303, 49.7006890822929),
    (33.4276444790818, 52.5438424393454),
    (33.4276444790818, 54.000230247447)]
_INNER_POLES = [
    (50.0, 21.0),
    (50.0, 22.3079115214089),
    (49.9456685626124, 24.9199250003161),
    (49.7013458667181, 28.8265283607768),
    (49.1140205524478, 34.0169928869225),
    (48.2253198540169, 40.494237360526),
    (47.637994539746, 45.6847018866711),
    (47.3936718438511, 49.591305247131),
    (47.3393404064634, 52.2033187260382),
    (47.3393404064634, 53.511230247447)]


def vendor_spline(poles, x0, x1, y0, y1, z):
    """Degree-5 B-spline edge through re-mapped vendor poles at height z."""
    px0, py0 = poles[0]
    px1, py1 = poles[-1]
    n = len(poles)
    deg = 5
    arr = Array1_gp_Pnt(1, n)
    for i, (px, py) in enumerate(poles, 1):
        x = x0 + (x1 - x0) * (px - px0) / (px1 - px0)
        y = y0 + (y1 - y0) * (py - py0) / (py1 - py0)
        arr.SetValue(i, gp_Pnt(X(x), y, z))
    nseg = n - deg
    knots = Array1_double(1, nseg + 1)
    mults = Array1_int(1, nseg + 1)
    for i in range(nseg + 1):
        knots.SetValue(i + 1, i / nseg)
        mults.SetValue(i + 1, deg + 1 if i in (0, nseg) else 1)
    curve = Geom_BSplineCurve(arr, knots, mults, deg)
    return Edge(BRepBuilderAPI_MakeEdge(curve).Edge())


def wire_of(items):
    """Wire from a mix of edges and Polyline wires."""
    edges = []
    for it in items:
        edges.extend(it.edges() if isinstance(it, Wire) else [it])
    return Wire(edges)


def arc_mid(c, r, a, b):
    """Point on the minor arc of circle (c, r) halfway between a and b."""
    ux, uy = a[0] - c[0] + b[0] - c[0], a[1] - c[1] + b[1] - c[1]
    L = math.hypot(ux, uy)
    return (c[0] + r * ux / L, c[1] + r * uy / L)


# ---- plate + panel: one profile in the XY plane, extruded in z ----------
z = plate_z0
panel_out_y_str = panel_y_end - panel_out_straight
panel_in_y_str = panel_y_end - panel_in_straight
A = (plate_front_x, -plate_y_back)
B = (plate_front_x, panel_y0)
C = (panel_out_x, panel_out_y_str)
D = (panel_out_x, panel_y_end)
# lip: bead centred on the end-face line at the inner corner, fillet
# tangent to the end face and to the bead.
c_bead = (panel_in_x - lip_bead_r, panel_y_end)
dx = math.sqrt((lip_fillet_r + lip_bead_r) ** 2 - lip_fillet_r ** 2)
c_fil = (c_bead[0] - dx, panel_y_end + lip_fillet_r)
E = (c_fil[0], panel_y_end)
k = lip_fillet_r / (lip_fillet_r + lip_bead_r)
T = (c_fil[0] + k * (c_bead[0] - c_fil[0]), c_fil[1] + k * (c_bead[1] - c_fil[1]))
F = (panel_in_x, panel_y_end)
G = (panel_in_x, panel_in_y_str)
H = (plate_back_x, panel_y0)
I = (plate_back_x, -plate_y_back)


def P(p):
    return (X(p[0]), p[1], z)


profile = [
    Polyline(P(A), P(B)),
    vendor_spline(_OUTER_POLES, plate_front_x, panel_out_x,
                  panel_y0, panel_out_y_str, z),
    Polyline(P(C), P(D), P(E)),
    ThreePointArc(P(E), P(arc_mid(c_fil, lip_fillet_r, E, T)), P(T)),
    ThreePointArc(P(T), P(arc_mid(c_bead, lip_bead_r, T, F)), P(F)),
    Polyline(P(F), P(G)),
    vendor_spline(_INNER_POLES, plate_back_x, panel_in_x,
                  panel_y0, panel_in_y_str, z),
    Polyline(P(H), P(I), P(A)),
]
plate = extrude(make_face(wire_of(profile)), amount=plate_h, dir=(0, 0, 1))

# panel end hole (along -y from the end face). The extra Rot(0, 0, 90)
# turns the cylinder about its own axis: with the default seam position
# the seam lands exactly on the vendor hole's seam and OCCT's cut against
# the vendor solid fails (compare reports an invalid result).
plate -= (Pos(X(end_hole_x), panel_y_end - end_hole_depth / 2, end_hole_z)
          * Rot(-90, 0, 0) * Rot(0, 0, 90) * Cylinder(end_hole_r, end_hole_depth))


# ---- tabs ----------------------------------------------------------------
def make_tab(sgn):
    """Tab hanging off the bottom (sgn = -1) or top (sgn = +1) plate edge;
    profile in the plane y = tab_y0, extruded +y."""
    y = tab_y0
    zb = zc + sgn * plate_h / 2            # plate edge the tab hangs from
    P1 = (plate_front_x, zb - sgn * tab_gusset_h)
    P2 = (tab_edge_x, zb)
    # gusset arc: through P1, tangent to the vertical free edge at P2
    cx = ((tab_edge_x ** 2 - plate_front_x ** 2 - tab_gusset_h ** 2)
          / (2 * (tab_edge_x - plate_front_x)))
    cg = (cx, zb)
    rg = cx - tab_edge_x
    # big arc: centre inboard of the plate edge, from the free edge down
    # to where it meets the plate's bottom/top face
    cb = (tab_arc_cx, zb - sgn * tab_arc_cz)
    P3 = (tab_edge_x,
          cb[1] + sgn * math.sqrt(tab_arc_r ** 2 - (tab_edge_x - cb[0]) ** 2))
    P4 = (cb[0] + math.sqrt(tab_arc_r ** 2 - tab_arc_cz ** 2), zb)
    P5 = (plate_front_x, zb)

    def Q(p):
        return (X(p[0]), y, p[1])

    w = wire_of([
        ThreePointArc(Q(P1), Q(arc_mid(cg, rg, P1, P2)), Q(P2)),
        Polyline(Q(P2), Q(P3)),
        ThreePointArc(Q(P3), Q(arc_mid(cb, tab_arc_r, P3, P4)), Q(P4)),
        Polyline(Q(P4), Q(P5), Q(P1)),
    ])
    tab = extrude(make_face(w), amount=tab_t, dir=(0, 1, 0))
    # countersunk hole, countersink opening on the outer (y = tab_y0 + t) face
    hz = zb + sgn * tab_hole_drop
    csk_d = tab_csk_r - tab_hole_r
    cut = Cylinder(tab_hole_r, big)
    cut += Pos(0, 0, tab_t - csk_d / 2) * Cone(tab_hole_r, tab_csk_r, csk_d)
    cut += Pos(0, 0, tab_t + big / 2) * Cylinder(tab_csk_r, big)
    # local z -> +y, local origin at y = tab_y0
    tab -= Pos(X(tab_hole_x), tab_y0, hz) * Rot(-90, 0, 0) * cut
    return tab


tab_bot = make_tab(-1)
tab_top = make_tab(+1)

# ---- frame ---------------------------------------------------------------
# Every frame length is multiplied by frame_scale (S); x' levels are
# plate_back_x + S * nominal depth.
S = frame_scale
x0 = plate_back_x


def fx(d):
    return x0 + S * d


x_top = fx(frame_h)
x_rim = fx(frame_h - rim_h)
x_ledge = fx(ledge_h)
fw, fl, wl = frame_w * S, frame_len * S, wall * S
cav_w = fw - 2 * wl
yc = frame_y_front - fw / 2
hole_ys = (yc - hole_dy * S / 2, yc + hole_dy * S / 2)
hole_zs = (frame_zc - hole_dz * S / 2, frame_zc + hole_dz * S / 2)
z_top, z_bot = frame_zc + fl / 2, frame_zc - fl / 2


def yz_plane(x):
    """Sketch plane at x' = x: u -> y, v -> -z, normal +x' (vendor -x)."""
    return Plane(origin=(X(x), yc, frame_zc), x_dir=(0, 1, 0), z_dir=(-1, 0, 0))


def along_x(xc, yy, zz):
    """Place a z-up primitive with local +z along +x' at x' = xc."""
    return Pos(X(xc), yy, zz) * Rot(0, -90, 0)


def box(x0_, x1_, y0_, y1_, z0_, z1_):
    return Pos(X((x0_ + x1_) / 2), (y0_ + y1_) / 2, (z0_ + z1_) / 2) * Box(
        x1_ - x0_, y1_ - y0_, z1_ - z0_)


frame = extrude(yz_plane(x0) * RectangleRounded(fw, fl, frame_corner_r * S),
                amount=x_top - x0)
# cavity (open at the base, up to the rim)
frame -= extrude(yz_plane(x0 - 1) * RectangleRounded(cav_w, cavity_len * S, cavity_r * S),
                 amount=x_rim - x0 + 1)
# lid rim: only the 2.5 walls remain for the last rim_h
frame -= extrude(yz_plane(x_rim) * Rectangle(cav_w, fl - 2 * wl),
                 amount=x_top - x_rim + 1)
# end bars relieved between the half bosses, above the board ledge
for zb_, sgn in ((hole_zs[0], 1), (hole_zs[1], -1)):
    zin = zb_ + sgn * boss_r * S        # bar face tangent to the bosses
    rel = box(x_ledge, x_rim + 1, hole_ys[0], hole_ys[1], min(zb_, zin), max(zb_, zin))
    for yh in hole_ys:
        rel -= along_x((x_ledge + x_rim) / 2, yh, zb_) * Cylinder(boss_r * S, x_rim - x_ledge + 4)
    frame -= rel
# mounting holes: r hole_r to the counterbore, 45 deg cone, counterbore
cone_h = (hole_cb_r - hole_r) * S
x_cb = fx(frame_h - rim_h - hole_cb_depth)
for yh in hole_ys:
    for zh in hole_zs:
        frame -= along_x((x0 - 1 + x_cb) / 2, yh, zh) * Cylinder(hole_r * S, x_cb - x0 + 1)
        frame -= along_x(x_cb - cone_h / 2, yh, zh) * Cone(hole_r * S, hole_cb_r * S, cone_h)
        frame -= along_x(x_cb + 1, yh, zh) * Cylinder(hole_cb_r * S, 2)
# connector window through the +z bar (rounded end at its floor)
usb_x0 = fx(frame_h - usb_depth)
win = Plane(origin=(X(usb_x0 + big / 2), yc, hole_zs[1]), x_dir=(-1, 0, 0),
            z_dir=(0, 0, 1)) * RectangleRounded(big, usb_w * S, usb_r * S)
frame -= extrude(win, amount=big)
# blind pocket in the -z bar's outer face
pk_x0 = fx(frame_h - pocket_depth)
pk = Plane(origin=(X(pk_x0 + big / 2), yc, z_bot - 1), x_dir=(-1, 0, 0),
           z_dir=(0, 0, 1)) * RectangleRounded(big, pocket_w * S, pocket_r * S)
frame -= extrude(pk, amount=pocket_z * S + 1)
# r1 rounds on the four rim corners cut by the window / pocket
for half_w, z_face, zdir in ((usb_w * S / 2, z_top - wl, 1),
                             (pocket_w * S / 2, z_bot + wl, -1)):
    for side in (-1, 1):
        y_edge = yc + side * half_w
        y_in = y_edge + side * rim_round_r * S
        z_in = z_face + zdir * rim_round_r * S
        corner = box(x_rim, x_top + 1, min(y_edge, y_in), max(y_edge, y_in),
                     min(z_face, z_in), max(z_face, z_in))
        corner -= along_x(x_rim + 1, y_in, z_in) * Cylinder(rim_round_r * S, 6)
        frame -= corner
# 45 deg chamfer on every edge of the base face
base_edges = frame.edges().filter_by(lambda e: abs(e.center().X - X(x0)) < 1e-6)
frame = chamfer(base_edges, base_chamfer * S)

# ---- assemble ------------------------------------------------------------
part = plate + tab_bot + tab_top + frame

show_object(part, name="left_side", color="steelblue")
