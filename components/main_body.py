# Main body — parametric reconstruction.
#
# Reverse-engineered from components/Main body.step with `lamad re det all`
# + `lamad re inspect`. One solid, 60 faces (38 planes + 22 cylinders):
#
#   * a 100 x 130 x 5 mm plate (X x Z x Y) with R20 corners at the +Z end,
#     R33 corners at the -Z end, a 5 mm deep notch along each long side,
#     four 2.9 mm corner holes and two 3.4 mm holes on the Z axis;
#   * a full-length T-slot / dovetail groove on the +Y face running along Z:
#     15.3 mm wide floor at y = 2.35, undercut lips whose undersides slope
#     15 deg down to a 7.20 mm opening at y = 5, r0.35 fillets at the four
#     wall corners, and a 0.3 mm tall 45 deg-chamfered ridge up the middle
#     of the floor (the two Z-axis holes break through its top);
#   * a bayonet hub on the -Y face: r23.513 x 2.1375 hub, r21.891 neck down
#     to y = -5.13, then a 3.965 mm thick lobed disc (base r21.589, three
#     lobes to r23.085 spanning 65 / 51.6 / 51.7 deg). It is the mating
#     half of the lugged ring in components/bayonet_casing.py.
#
# Typed (clean) dimensions are used as the knobs; the few ugly numbers in
# the STEP (hub/neck radii, disc bottom, notch end 40.002, corner hole
# positions) are solver outputs and are kept verbatim. The three lobe
# angles are all exactly 0.0026118 deg below their typed values (sketch
# seam at 117.0 deg) — reproduced via `lobe_rot`.
#
# Coordinate frame matches the vendor file: plate occupies x -50..50,
# y 0..5, z -65..65; hub axis is -Y through the origin; groove runs along Z
# on the y = 5 face. Lobe angles are vendor XZ degrees, atan2(z, x). Units mm.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.
# (Negative literals are not picked up as params, so the -Z / -Y values
# are given as positive magnitudes and negated where used.)

# ---- plate envelope ------------------------------------------------------
plate_w = 100.0         # X
plate_t = 5.0           # Y, y = 0 .. plate_t
plate_l = 130.0         # Z
top_corner_r = 20.0     # corners at +Z
bot_corner_r = 33.0     # corners at -Z
notch_depth = 5.0       # side notches, both long edges
notch_z_lo = 31.8       # notch from z = -notch_z_lo ...
notch_z_hi = 40.002     # ... to z = +notch_z_hi

# ---- holes (all along Y) -------------------------------------------------
corner_hole_r = 1.45
corner_hole_x = 44.2892138
corner_hole_z_hi = 45.2456934   # z = +corner_hole_z_hi
corner_hole_z_lo = 37.0436934   # z = -corner_hole_z_lo
end_hole_r = 1.7
end_hole_z = 60.0               # z = +-end_hole_z, x = 0

# ---- groove on the +Y face (profile in XY, runs along Z) -----------------
groove_floor = 2.35        # floor height (y)
groove_half_w = 7.65       # floor / wall half width
lip_half_w = 3.601095      # opening half width at y = plate_t
lip_angle = 15.0           # lip underside slope, deg from the XZ plane
groove_fillet = 0.35       # all four wall corners
ridge_h = 0.3              # centre ridge above the floor
ridge_top_half_w = 2.387868
ridge_chamfer = 0.3        # 45 deg sides on the ridge

# ---- bayonet hub on the -Y face ------------------------------------------
hub_r = 23.5129275
hub_h = 2.1375             # y = 0 .. -hub_h
neck_r = 21.8909925
neck_bottom = 5.13         # y = -neck_bottom (lobed disc top)
disc_r = 21.58875          # lobed disc base radius
lobe_r = 23.085            # lobe outer radius
disc_bottom = 9.094635     # y = -disc_bottom
lobe1_start = 41.2         # vendor XZ deg, lobe grows CCW (atan2(z, x))
lobe1_span = 65.0
lobe2_start = 165.5
lobe2_span = 51.6
lobe3_start = 284.5
lobe3_span = 51.7
lobe_rot = 0.0026118       # subtracted from every lobe angle (vendor quirk)

include_hub = True

# ========================================================================
import math

big = 3 * plate_l  # generous cutter size (derived, so not a --param knob)


def cyl_y(r, y0, y1, x=0.0, z=0.0):
    """Cylinder with its axis along Y spanning y0..y1 at (x, z)."""
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def sector_y(r, y0, y1, a0, a1):
    """Disc sector about the Y axis between vendor XZ angles a0..a1 (deg,
    CCW as seen with atan2(z, x); span <= 180)."""
    if a1 - a0 > 180:
        raise ValueError("sector span must be <= 180 deg")
    # Rot(0, -t, 0) carries +X to angle t. Half-space z >= 0 is 0..180 deg.
    half = Pos(0, 0, big / 2) * Box(2 * big, 2 * big, big)
    w0 = Rot(0, -a0, 0) * half              # angles a0 .. a0 + 180
    w1 = Rot(0, -(a1 - 180), 0) * half      # angles a1 - 180 .. a1
    return cyl_y(r, y0, y1) & w0 & w1


# ---- plate ---------------------------------------------------------------
plate = Pos(0, plate_t / 2, 0) * Box(plate_w, plate_t, plate_l)
hx, hz = plate_w / 2, plate_l / 2

# rounded corners: square cutter minus the corner cylinder
for sx in (-1, 1):
    for sz, r in ((1, top_corner_r), (-1, bot_corner_r)):
        cx, cz = sx * (hx - r), sz * (hz - r)        # arc centre
        sq = Pos(sx * (hx - r / 2), plate_t / 2, sz * (hz - r / 2)) * Box(
            r, plate_t + 2, r)
        plate -= sq - cyl_y(r, -2, plate_t + 2, cx, cz)
    # side notch
    nz0, nz1 = -notch_z_lo, notch_z_hi
    plate -= Pos(sx * (hx - notch_depth / 2), plate_t / 2, (nz0 + nz1) / 2) * Box(
        notch_depth, plate_t + 2, nz1 - nz0)

# ---- groove (cutter profile in the XY plane, extruded along Z) -----------
lip_y_wall = plate_t - (groove_half_w - lip_half_w) * math.tan(
    math.radians(lip_angle))
ridge_base_half_w = ridge_top_half_w + ridge_chamfer
ridge_top = groove_floor + ridge_h
profile = Polygon(
    (-groove_half_w, groove_floor),
    (-ridge_base_half_w, groove_floor),
    (-ridge_top_half_w, ridge_top),
    (ridge_top_half_w, ridge_top),
    (ridge_base_half_w, groove_floor),
    (groove_half_w, groove_floor),
    (groove_half_w, lip_y_wall),
    (lip_half_w, plate_t),
    (lip_half_w, plate_t + 2),
    (-lip_half_w, plate_t + 2),
    (-lip_half_w, plate_t),
    (-groove_half_w, lip_y_wall),
    align=None,
)
cutter = extrude(profile, amount=hz + 5, both=True)
wall_edges = [
    e for e in cutter.edges().filter_by(Axis.Z)
    if abs(abs(e.center().X) - groove_half_w) < 1e-6
]
cutter = fillet(wall_edges, groove_fillet)
plate -= cutter

# ---- holes ---------------------------------------------------------------
for sx in (-1, 1):
    for z in (corner_hole_z_hi, -corner_hole_z_lo):
        plate -= cyl_y(corner_hole_r, -2, plate_t + 2, sx * corner_hole_x, z)
for sz in (-1, 1):
    plate -= cyl_y(end_hole_r, -2, plate_t + 2, 0, sz * end_hole_z)

# ---- bayonet hub ---------------------------------------------------------
body = plate
if include_hub:
    hub = cyl_y(hub_r, -hub_h, 0)
    hub += cyl_y(neck_r, -neck_bottom, -hub_h)
    hub += cyl_y(disc_r, -disc_bottom, -neck_bottom)
    for start, span in ((lobe1_start, lobe1_span), (lobe2_start, lobe2_span),
                        (lobe3_start, lobe3_span)):
        a0 = start - lobe_rot
        hub += sector_y(lobe_r, -disc_bottom, -neck_bottom, a0, a0 + span)
    body = plate + hub

show_object(body, name="main_body", color="seagreen")
