# Igus DryLin T TS-04-15 rail — parametric reconstruction (BOM: TS-04-15-600).
#
# Reverse-engineered from
#   components/Vendor/Igus drylin T TS-04-15 rail (100mm).step
# (vendor-authoritative, igus-cad.com) with `lamad re det all` +
# `lamad re inspect`. One solid, 49 faces (29 planes + 20 cylinders).
#
# Cross-section (XZ, symmetric about x = 0, read from the y = -50 end loop;
# all numbers typed in the vendor file, nothing solver-derived):
#   * top flange 17.0 wide, underside at z = 6.2 (4.6 thick), 0.4 x 45 deg
#     chamfers on both outer corners, 8.0-wide / 0.5-deep 45 deg-sided groove
#     down the middle of the top face (7.0 at the floor, z = 10.3);
#   * web 5.5 wide, r0.7 fillets into the top flange underside, r1.0 fillets
#     into the lower flange;
#   * lower flange 15.0 wide, 1.3 tall at its outer edge; its upper (carriage
#     running) faces slope 15 deg up toward the web, r0.2 fillets on both
#     outer corners;
#   * bottom face has a 5.5-wide / 0.3-deep 45 deg-sided recess (4.9 at the
#     floor) down the middle.
#
# Mounting holes (axis Z, on the centreline): 3.4 through, 6.0 counterbore
# sunk 3.2 below the top-groove floor (counterbore floor at z = 7.1).
# The 100 mm vendor rail has holes at y = -40, 0, +40, i.e. pitch 40 with
# 10 mm from each end.
#
# HOLE RULE: igus cut rails carry the hole pattern CENTRED on the rail
# ("Bohrbild mittig"): n = floor((length - 2 * hole_end_min) / hole_pitch) + 1
# holes at pitch 40, the pattern centred on y = 0, so both end distances are
# equal and >= hole_end_min (10 mm, the end distance seen on the 100 mm
# rail). Set `holes_centered = False` for the alternative "first hole a fixed
# hole_end_min from the -Y end, march at pitch while the far end distance
# stays >= hole_end_min" rule. Both rules reproduce the 100 mm vendor file.
#
# Coordinate frame matches the vendor file: rail runs along Y and is centred
# on the origin (y = -length/2 .. +length/2), x = -8.5 .. 8.5, bottom face at
# z = 0, top face at z = 10.8. Units mm.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

# ---- length / holes -----------------------------------------------------
length = 100.0          # 100 reproduces the vendor file; BOM part is 600
hole_pitch = 40.0
hole_end_min = 10.0     # minimum (and, for the 100 mm rail, actual) end distance
holes_centered = True   # igus rule; False = fixed offset from the -Y end
hole_r = 1.7            # 3.4 through (M3 clearance)
cbore_r = 3.0           # 6.0 counterbore
cbore_depth = 3.2       # measured down from the top-groove floor

# ---- cross-section ---------------------------------------------------------
width = 17.0            # X, overall (top flange)
height = 10.8           # Z, overall
top_flange_t = 4.6      # top flange thickness (underside at height - this)
top_chamfer = 0.4       # 45 deg, both outer corners of the top flange
top_groove_w = 8.0      # width at the top face
top_groove_d = 0.5      # depth, 45 deg sides (floor is 1.0 narrower)
web_w = 5.5
web_top_fillet = 0.7    # web -> top flange underside
web_bot_fillet = 1.0    # web -> lower flange running face
low_flange_w = 15.0
low_flange_h = 1.3      # outer-edge height of the lower flange
run_angle = 15.0        # running-face slope, deg from horizontal
low_corner_fillet = 0.2 # both outer corners of the lower flange
bot_recess_w = 5.5      # width at the bottom face
bot_recess_d = 0.3      # depth, 45 deg sides (floor is 0.6 narrower)

# ========================================================================
import math

half_w = width / 2
half_lw = low_flange_w / 2
half_web = web_w / 2
under = height - top_flange_t
tg_half = top_groove_w / 2
tg_floor_half = tg_half - top_groove_d          # 45 deg sides
br_half = bot_recess_w / 2
br_floor_half = br_half - bot_recess_d           # 45 deg sides
# running face: z = low_flange_h at x = half_lw, rising at run_angle inward
web_corner_z = low_flange_h + (half_lw - half_web) * math.tan(
    math.radians(run_angle))

# sharp (pre-fillet) half profile, CCW from the bottom centre, mirrored
right = [
    (br_floor_half, bot_recess_d),
    (br_half, 0.0),
    (half_lw, 0.0),
    (half_lw, low_flange_h),
    (half_web, web_corner_z),
    (half_web, under),
    (half_w - top_chamfer, under),
    (half_w, under + top_chamfer),
    (half_w, height - top_chamfer),
    (half_w - top_chamfer, height),
    (tg_half, height),
    (tg_floor_half, height - top_groove_d),
]
pts = right + [(-x, z) for (x, z) in reversed(right)]
profile = Plane.XZ * Polygon(*pts, align=None)
rail = extrude(profile, amount=length / 2, both=True)


def y_edges_at(shape, x, z, tol=1e-4):
    """Edges parallel to Y whose section point is at (+-x, z)."""
    return [
        e for e in shape.edges().filter_by(Axis.Y)
        if abs(abs(e.center().X) - x) < tol and abs(e.center().Z - z) < tol
    ]


rail = fillet(y_edges_at(rail, half_web, web_corner_z), web_bot_fillet)
rail = fillet(y_edges_at(rail, half_web, under), web_top_fillet)
rail = fillet(
    y_edges_at(rail, half_lw, 0.0) + y_edges_at(rail, half_lw, low_flange_h),
    low_corner_fillet)

# ---- mounting holes --------------------------------------------------------
if holes_centered:
    n = int(math.floor((length - 2 * hole_end_min) / hole_pitch + 1e-9)) + 1
    span = (n - 1) * hole_pitch
    hole_ys = [-span / 2 + i * hole_pitch for i in range(n)]
else:
    hole_ys = []
    y = -length / 2 + hole_end_min
    while y <= length / 2 - hole_end_min + 1e-9:
        hole_ys.append(y)
        y += hole_pitch

cb_floor = height - top_groove_d - cbore_depth
for y in hole_ys:
    rail -= Pos(0, y, height / 2) * Cylinder(hole_r, height + 2)
    rail -= Pos(0, y, (cb_floor + height + 1) / 2) * Cylinder(
        cbore_r, height + 1 - cb_floor)

show_object(rail, name="igus_rail_TS-04-15", color="silver")
