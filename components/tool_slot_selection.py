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
#     lead-in funnel on the front and a 5 x 2.5 slope on the back;
#   * the back half (y 10..20) of the window is 4.6 mm wider, with an extra
#     7 mm wide widening at y 10..14 whose floor slopes 68 deg;
#   * two cantilever snap tabs (3.0 x 16 x 1.17 mm) hanging in pockets in
#     the side walls at y 6.5..10 with a shallow R4.4 detent bump;
#   * a 1.5 mm front recess over the side walls below z = -0.6 (R5.5 round
#     into the front face) and a 45 deg chamfer under the wall bottoms, both
#     sparing a 63 mm wide central lobe;
#   * a 2.7 mm deep trough with R14.3 sides in the cavity floor, open to
#     the back face, with a 23 deg front wall;
#   * one 3.8 mm x 7 mm deep blind hole in each outer side face (heat-set
#     insert / pin) at y 5, z 4.6;
#   * R2 fillets on the top/side edges of both faces, R1 on the hull edges
#     (except the lobe's share of the front side-arc edge, left sharp).
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

# ---- STL frame -----------------------------------------------------------
x_center = 0.1605       # x of the symmetry plane in the STL
y_front = 60.017        # front face (y) in the STL

# ---- outer body ----------------------------------------------------------
width = 80.0
thick = 20.0            # Y thickness
z_top = 43.752
top_corner_r = 2.0      # rounds on the two top corners of the XZ outline
kink_depth = 30.227     # straight sides end at z = -30.227 (sharp kink)
side_arc_r = 80.46      # hull side arcs (not tangent to the sides)
junction_x = 27.5865    # where the side arcs meet the bottom arc (sharp)
junction_depth = 50.77
bottom_depth = 56.579   # lowest point of the bottom arc (z = -56.579)
fillet_top = 2.0        # edges of the front/back faces above the kink
fillet_hull = 1.0       # edges of the front/back faces on the hull arcs

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
bar_front_y = 5.0
bar_back_y = 7.492
bar_half_front = 26.285 # window half-width at the bar front face
bar_half_back = 25.9955
funnel_run = 5.0        # 45 deg lead-in: width grows by this at y = 0
back_slope_run = 5.0    # back slope widens by this between bar_back_y..split_y
split_y = 10.0          # front/back cavity profiles change here
widen_half = 35.296     # extra widening y split_y..widen_y1 (70.59 wide)
widen_y1 = 14.0
widen_floor_z0 = 2.753  # widening floor z at y = split_y ...
widen_floor_z1 = 12.783 # ... and at y = widen_y1 (68 deg slope)

# ---- front recess / chamfer (spare the central lobe) ---------------------
recess_depth = 1.5
recess_top_depth = 0.604   # recess ends at z = -0.604 ...
recess_round_r = 5.5       # ... with an R5.5 round out to the front face
lobe_half = 31.5           # un-recessed central lobe |x| < 31.5
lobe_top_depth = 21.987    # lobe begins at z = -21.987
chamfer_depth0 = 32.227    # 45 deg plane y + z = -32.227 under the walls

# ---- snap tabs in the side walls -----------------------------------------
tab_inset = 1.0         # tab inner face is 1.0 mm outboard of cav_half
tab_w = 3.008
tab_gap = 0.3           # side clearance in the pocket
tab_gap_bot = 0.4       # bottom clearance
tab_t = 1.167           # tab thickness (y)
pocket_back_y = 6.5     # pocket spans y 6.5..split_y
tab_z0 = 10.6
tab_z1 = 26.6           # tab roots into the pocket ceiling here
bump_r = 4.4            # detent bump on the tab's cavity face
bump_protrude = 0.416
bump_z = 12.462

# ---- side holes ----------------------------------------------------------
hole_d = 3.8
hole_depth = 7.0
hole_y = 5.0
hole_z = 4.586

# ---- floor trough (open to the back face) --------------------------------
trough_depth = 50.887   # trough floor z = -50.887 (2.7 below the cavity floor)
trough_flat_half = 9.7
trough_r = 14.3         # sides blend into the cavity floor at floor_half
trough_y0 = 12.704      # front wall meets the cavity floor here ...
trough_y1 = 13.849      # ... and the trough floor here (23 deg wall)

# ========================================================================
import math

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
    Line(P(-hw, -kink_depth), P(-hw, z_top - top_corner_r)),
    ThreePointArc(P(-hw, z_top - top_corner_r),
                  P(-hw + top_corner_r * (1 - math.cos(math.pi / 4)),
                    z_top - top_corner_r * (1 - math.sin(math.pi / 4))),
                  P(-hw + top_corner_r, z_top)),
    Line(P(-hw + top_corner_r, z_top), P(hw - top_corner_r, z_top)),
    ThreePointArc(P(hw - top_corner_r, z_top),
                  P(hw - top_corner_r * (1 - math.cos(math.pi / 4)),
                    z_top - top_corner_r * (1 - math.sin(math.pi / 4))),
                  P(hw, z_top - top_corner_r)),
    Line(P(hw, z_top - top_corner_r), K),
    radius_arc(K, J, side_arc_r, P(0, 0)),
    ThreePointArc(J, B, mirror_x(J)),
    radius_arc(mirror_x(J), mirror_x(K), side_arc_r, P(0, 0)),
]
body = prism_y(face_xz(outline), 0, thick)

# fillets on the front/back faces: R2 above the kink, R1 on the hull arcs.
raw_body = body


def yface_edges(solid, y, zlo, zhi):
    return [e for e in solid.edges()
            if abs(e.center().Y - y) < 1e-3 and zlo < e.center().Z < zhi]


try:
    body = fillet(yface_edges(body, 0, -kink_depth + 1e-3, BIG)
                  + yface_edges(body, thick, -kink_depth + 1e-3, BIG), fillet_top)
    body = fillet(yface_edges(body, 0, -BIG, -kink_depth - 1e-3)
                  + yface_edges(body, thick, -BIG, -kink_depth - 1e-3), fillet_hull)
    fillet_mode = "chained"
except Exception:
    # fall back: split at the kink, fillet the two pieces, re-join (leaves a
    # small step where R2 meets R1 instead of the CAD blend)
    upper_part = body & box(-BIG, BIG, -1, thick + 1, -kink_depth, BIG)
    lower_part = body & box(-BIG, BIG, -1, thick + 1, -BIG, -kink_depth)
    upper_part = fillet(yface_edges(upper_part, 0, -kink_depth + 1e-3, BIG)
                        + yface_edges(upper_part, thick, -kink_depth + 1e-3, BIG),
                        fillet_top)
    lower_part = fillet(yface_edges(lower_part, 0, -BIG, -kink_depth - 1e-3)
                        + yface_edges(lower_part, thick, -BIG, -kink_depth - 1e-3),
                        fillet_hull)
    body = upper_part + lower_part
    fillet_mode = "split"

# The STL has NO fillet on the front face along the side arcs: outside the
# central lobe the recess removes that edge, and inside the lobe the edge was
# simply left sharp (only the bottom arc is filleted there). OCCT propagates
# the hull fillet along the whole front chain, so put that sliver back.
for s in (1, -1):
    body += raw_body & box(min(s * junction_x, s * lobe_half),
                           max(s * junction_x, s * lobe_half),
                           -1, fillet_hull + 0.01, -BIG, -lobe_top_depth)

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

# ---- top bar: front funnel and back slope (z above the window ceiling) --
z_hi = z_top + 5
funnel = Polygon((-bar_half_front - funnel_run - 1, -1),
                 (bar_half_front + funnel_run + 1, -1),
                 (bar_half_front, bar_front_y),
                 (-bar_half_front, bar_front_y), align=None)
body -= Pos(0, 0, cav_top) * extrude(funnel, amount=z_hi - cav_top)
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

# ---- front recess + under-wall chamfer, sparing the central lobe ---------
lobe = box(-lobe_half, lobe_half, -1, thick + 1, -BIG, -lobe_top_depth)
recess = box(-BIG, BIG, -1, recess_depth, -BIG, -recess_top_depth)
recess += cyl_x(recess_round_r, -BIG, BIG, recess_depth - recess_round_r,
                -recess_top_depth)
cham = Plane.YZ * Polygon((-1, -chamfer_depth0 + 1), (thick + 1, -chamfer_depth0 - thick - 1),
                          (thick + 1, -BIG), (-1, -BIG), align=None)
cutter = recess + extrude(cham, amount=BIG, both=True)
body -= cutter - lobe

# ---- snap tabs -----------------------------------------------------------
for s in (1, -1):
    xi = cav_half + tab_inset            # tab inner face
    xo = xi + tab_w                      # tab outer face
    pocket = box(min(s * (xi - tab_gap), s * (xo + tab_gap)),
                 max(s * (xi - tab_gap), s * (xo + tab_gap)),
                 pocket_back_y, split_y + 0.5, tab_z0 - tab_gap_bot, tab_z1)
    body -= pocket
    tab = box(min(s * xi, s * xo), max(s * xi, s * xo),
              split_y - tab_t, split_y, tab_z0, tab_z1)
    bump = cyl_x(bump_r, min(s * xi, s * xo), max(s * xi, s * xo),
                 split_y + bump_protrude - bump_r, bump_z)
    bump &= box(-BIG, BIG, split_y, split_y + 1, -BIG, BIG)
    body += tab + bump

# ---- side holes ----------------------------------------------------------
for s in (1, -1):
    x_in, x_out = hw - hole_depth, hw + 1
    body -= cyl_x(hole_d / 2, min(s * x_in, s * x_out), max(s * x_in, s * x_out),
                  hole_y, hole_z)

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
show_object(body, name="tool_slot_selection", color="burlywood")
