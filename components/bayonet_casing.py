# Bayonet casing v10 — parametric reconstruction.
#
# Reverse-engineered from components/Bayonet casing v10.step with
# `lamad re det all` + `lamad re inspect`. Two solids in the vendor file:
#
#   * a 75 mm x 5 mm mounting disc (1 mm 45 deg chamfer both faces, two
#     countersunk through-holes on the X axis), and
#   * a bayonet ring sitting on the disc: 7.35 mm tall tube with a 1.4 mm
#     deep counterbore lip at the mouth and three internal lugs. Each lug
#     has a 1.0 mm-wide locating tooth that hangs down toward the disc, a
#     flat clamping land, and a 23 deg planar ramp that thins the lug
#     from 1.9 mm to 1.3 mm at its free end.
#
# Every linear dimension of the ring divides by 1.00056 into a round number
# (OD 56, ID 46.6, lug ID 44.1, height 7.35, ...), so the ring was clearly
# scaled uniformly by that factor for fit; the disc is unscaled. `ring_scale`
# reproduces that. The three lugs are NOT an exact 120 deg polar pattern in
# the vendor file (ends at 32.95 / 151.97 / 270 deg, third lug 0.5 mm longer);
# the measured end angles are kept so the reconstruction matches the STEP.
#
# Coordinate frame matches the vendor file: ring axis is +Y through
# (13.2557, *, 92.0822); the disc spans y = -62.988 .. -57.988 and the ring
# grows toward +Y from the disc's top face. Units mm. Angles below are
# measured in the vendor XZ plane as atan2(z - cz, x - cx) in degrees.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

# ---- vendor frame ---------------------------------------------------------
axis_x = 13.2556572     # ring axis position (vendor X)
axis_z = 92.0822317     # ring axis position (vendor Z)
disc_y0 = -62.988375    # disc bottom face (vendor Y)

# ---- mounting disc -------------------------------------------------------
disc_r = 37.5
disc_h = 5.0
disc_chamfer = 1.0        # 45 deg, both faces
hole_pitch = 63.0         # two holes on the X axis, +-31.5
hole_r = 3.25             # 6.5 mm through-hole
csk_r = 6.0               # 90 deg countersink, 12 mm at the ring-side face
csk_depth = 2.75          # == csk_r - hole_r for a 90 deg countersink

# ---- bayonet ring (nominal, pre-scale) -----------------------------------
ring_scale = 1.00056      # uniform scale applied to every ring length
ring_r_out = 28.0
ring_r_in = 23.3          # bore below the lip
lip_r = 23.875            # counterbore at the mouth
lip_depth = 1.4
ring_h = 7.35
lug_r_in = 22.05          # lug inner radius
lug_thick = 1.9           # lug thickness at the flat land
lug_tip_thick = 1.2989    # thickness at the end of the ramp
tooth_h = 1.45            # tooth bottom above the disc face

# ---- lug layout ----------------------------------------------------------
# The vendor file dimensions each lug as an ARC LENGTH on the ring bore
# (21.0 mm, with the third lug 21.5 mm); the odd-looking angles in the STEP
# (51.64 / 52.87 deg) are just those arcs divided by ring_r_in. Tooth and
# ramp are angular. The flat land is whatever is left over.
lug_arc = 21.0            # lugs 1 and 2: span as arc length at ring_r_in
lug3_arc = 21.5           # lug 3 is 0.5 mm longer (keying)
tooth_deg = 2.46          # locating tooth, ~1.0 mm at the bore
ramp_deg = 23.0           # ramp arc, measured from the lug's free end
lug1_end = 32.9523166     # free (ramp) end of each lug, vendor XZ degrees
lug2_end = 151.9657761
lug3_end = 270.0          # (= -90 deg; kept positive so --param can see it)

include_disc = True
include_ring = True

# ========================================================================
import math

big = 100.0  # generous cutter length


def cyl_z(r, z0, z1, x=0.0, y=0.0):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def sector(r0, r1, a0, a1, z0, z1):
    """Annular sector r0..r1, angles a0..a1 (deg, CCW from +X), z0..z1."""
    ring = cyl_z(r1, z0, z1) - cyl_z(r0, z0, z1)
    span = a1 - a0
    # keep a wedge: half-space cuts along the two bounding radial planes
    wedge = cyl_z(r1 + 1, z0 - 1, z1 + 1)
    for a, side in ((a0, -1), (a1, 1)):
        cut = Pos(0, side * big / 2, 0) * Box(2 * big, big, 4 * big)
        wedge -= Rot(0, 0, a) * cut
    if span > 180:
        raise ValueError("sector span must be <= 180 deg")
    return ring & wedge


# ---- disc ----------------------------------------------------------------
# Built in a local frame: axis +Z, disc bottom at z = 0, then moved onto
# the vendor frame at the end.
disc = cyl_z(disc_r, 0, disc_h)
disc = chamfer(disc.edges().filter_by(GeomType.CIRCLE), disc_chamfer)
for sx in (-1, 1):
    x = sx * hole_pitch / 2
    disc -= cyl_z(hole_r, -big, big, x)
    # 90 deg countersink opening on the top (ring-side) face
    cone = Pos(x, 0, disc_h - csk_depth / 2) * Cone(hole_r, csk_r, csk_depth)
    disc -= cone
    disc -= cyl_z(csk_r, disc_h, big, x)

# ---- ring body -----------------------------------------------------------
S = ring_scale
R_out, R_in, R_lip, R_lug = (ring_r_out * S, ring_r_in * S,
                             lip_r * S, lug_r_in * S)
H = ring_h * S
lug_top = H - lip_depth * S
flat_z = lug_top - lug_thick * S
tip_z = lug_top - lug_tip_thick * S
tooth_z = tooth_h * S

ring = cyl_z(R_out, 0, H) - cyl_z(R_in, -1, H + 1)
ring -= cyl_z(R_lip, lug_top, H + 1)


def make_lug(end_deg_vendor, arc_mm):
    """One lug in the local frame. Local angle = -vendor angle (the local
    Z-up frame is rotated -90 deg about X to land on the vendor +Y axis)."""
    span = math.degrees(arc_mm / ring_r_in)   # scale-free: arc and radius
    # canonical lug: free end on the +X radial plane, lug grows CCW (+Y)
    body = sector(R_lug, R_in, 0, span - tooth_deg, flat_z, lug_top)
    tooth = sector(R_lug, R_in, span - tooth_deg, span, tooth_z, lug_top)
    # planar ramp: level lines parallel to the end plane (X), dropping
    # from tip_z at y = 0 to flat_z at the ramp/flat boundary
    run = R_lug * math.sin(math.radians(ramp_deg))
    slope = (tip_z - flat_z) / run
    y_far = run * 1.5
    prism = Plane.YZ * Polygon(
        (-1, tip_z + slope), (y_far, tip_z - slope * y_far),
        (y_far, flat_z - 1), (-1, flat_z - 1), align=None)
    wedge = extrude(prism, amount=R_in + 2, both=True)
    lug = (body - wedge) + tooth
    return Rot(0, 0, -end_deg_vendor) * lug


for end, arc in ((lug1_end, lug_arc), (lug2_end, lug_arc),
                 (lug3_end, lug3_arc)):
    ring += make_lug(end, arc)

# ---- place both solids in the vendor frame -------------------------------
# local (x, y, z) -> vendor (x, z, -y) + (axis_x, disc_y0, axis_z)
to_vendor = Pos(axis_x, disc_y0, axis_z) * Rot(-90, 0, 0)
disc = to_vendor * disc
ring = to_vendor * Pos(0, 0, disc_h) * ring

if include_disc:
    show_object(disc, name="mount_disc", color="dimgray")
if include_ring:
    show_object(ring, name="bayonet_ring", color="steelblue")
