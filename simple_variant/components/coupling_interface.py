# Coupling Interface (3.15)(M) (prt 4) — parametric reconstruction.
#
# Reverse-engineered from components/Coupling Interface (3.15)(M) (prt 4).step
# with `lamad re det all` + `lamad re inspect`. One solid, 28 x 28 x 10.5 mm,
# 3075 mm3. It is a bayonet-style coupling hub: a 26 mm cylindrical body with
# two M3 screw holes (3.15 mm clearance -- the "(3.15)" in the file name, also
# engraved as "3.15mm" on the underside) that bolts onto a servo horn, and a
# 28 mm flange on top carrying a 22.57 mm bore with three 3 mm-wide bayonet
# lugs (120 deg apart) that a tool slides into and twists to lock.
#
# Bottom to top (vendor Z, bottom face at z = -7.40551):
#   * body: 26 mm dia cylinder, 4.5 mm tall, then a 45 deg cone out to 28 mm
#     dia (1 mm tall), then the 28 mm flange (3 mm tall) and the lugs (2 mm).
#   * centre: 8 mm shaft bore with 0.5 x 45 deg openings to 9 mm at both
#     ends; the top end is a 9/11 mm hub ring standing 1 mm proud of a
#     recessed pocket floor; around it a shallow (0.5 mm) conical recess
#     (18.78 -> 20 mm) whose centre is 0.494 mm off the main axis, then the
#     flat ring up to the 22.57 mm bore of the flange, which has a 1 x 45 deg
#     chamfer at the mouth except where the lugs sit.
#   * screw hole A (r = 8 mm, 146.5 deg): 4.5 mm counterbore 2 mm deep, 45 deg
#     countersink, 3.15 mm hole, blind at the body top (z = 4.5 above the
#     bottom face; it does NOT break into the pocket).
#   * screw hole B (r = 10 mm, 326.5 deg = opposite A): same profile, but the
#     profile is also swept radially outward through the rim so the hole is
#     an open U-slot (4.5 mm wide at the counterbore level, 3.15 mm above),
#     with a V-shaped mouth (flanks at +-50.2 deg to the slot axis) at the rim.
#   * "3.15mm" engraved 2.5 mm deep into the bottom face on an arc centred on
#     hole A, reading correctly from below.
#
# What the 100 B-spline faces in the vendor file are (none is design intent):
#   * f6/f249 (348 mm2): the plain 26 mm cylinder of the body. The vendor
#     CAD stored it as a spline surface (sections fit a circle to 0.03 mm).
#   * f4/f248 (35 mm2): the swept U-slot wall and its 45 deg sloped floor at
#     hole B (a sweep of the countersink profile) -- analytic here.
#   * 96 tiny faces (43 mm2) plus ~95 tiny planes: the outlines of the six
#     glyphs of the engraved "3.15mm" text.
#   * the 45 deg body->flange cone is a 58-facet inscribed polygon in the
#     vendor file (facet planes 0.02 mm inside the cone); modelled as a true
#     cone (~1.5 mm3 difference).
# The engraved text is reproduced with build123d's default font (Arial),
# which is not the vendor's font: the glyph outlines only overlap ~30 %, so
# the text accounts for ~16 mm3 of residual (0.5 % of the part) with
# engrave_text=True, or ~12 mm3 of missing volume with it off.
#
# NOTE: `lamad re compare` in solid mode cannot boolean this vendor file (its
# B-spline body and 1e-5-off radii/levels at 0.0085 mm tolerance make OCCT
# return empty/invalid results for every coincident face, even for a plain
# cylinder). The compare artifacts were made in mesh mode against a 0.004 mm
# tessellation of the vendor solid; the IoU was computed with manifold3d
# mesh booleans on the same meshes (see compare_coupling_interface/).
#
# Coordinate frame matches the vendor file: part axis is +Z through
# (-0.0390318, 30.0490949); bottom face at z = -7.40551. Angles are vendor
# XY degrees, atan2(y - axis_y, x - axis_x). The script builds in a local
# frame (axis = Z, bottom face = z 0) and moves the result at the end.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

# ---- vendor frame ---------------------------------------------------------
axis_x = -0.0390318      # part axis (vendor X)
axis_y = 30.0490949      # part axis (vendor Y)
bottom_depth = 7.40551   # bottom face is this far below vendor z = 0

# ---- body / flange -------------------------------------------------------
body_r = 13.0            # 26 mm body
body_h = 4.5             # body top (also the blind ceiling of the holes)
cone_h = 1.0             # 45 deg cone from body_r to flange_r
flange_r = 14.0          # 28 mm flange
flange_h = 3.0           # flange thickness above the cone
bore_r = 11.2872         # flange bore (tool interface), 22.574 mm dia
bore_chamfer = 1.0       # 45 deg chamfer at the bore mouth

# ---- bayonet lugs --------------------------------------------------------
lug_count = 3
lug_w = 3.0              # parallel-sided, 3 mm wide
lug_h = 2.0              # stands above the flange top
lug_deg = 86.5           # first lug centre; the others at +120 deg

# ---- centre pocket / hub -------------------------------------------------
floor_z = 5.0            # pocket floor (0.5 below the flange underside)
recess_r_floor = 9.3901  # conical recess radius at the floor ...
recess_r_top = 10.0      # ... and where it meets the flat ring at z 5.5
recess_offset = 0.4941   # recess centre is off-axis by this much ...
recess_offset_deg = 56.5 # ... in this direction (hole_deg + 90)
hub_r = 5.5              # hub ring outer radius
hub_top = 6.0            # hub ring top
shaft_r = 4.0            # 8 mm shaft bore
shaft_cbore_r = 4.5      # 9 mm openings at both ends (45 deg steps)
shaft_cbore_h = 2.0      # depth of the bottom 9 mm opening

# ---- screw holes (M3 clearance) ------------------------------------------
hole_r = 1.575           # 3.15 mm clearance hole
head_r = 2.25            # 4.5 mm counterbore for the screw head
head_h = 2.0             # counterbore depth from the bottom face
csk_deg = 45.0           # countersink cone between head_r and hole_r
hole_a_r = 8.0           # hole A distance from the axis
hole_deg = 326.5         # hole B (and slot) direction; hole A is opposite
hole_b_r = 10.0          # hole B distance from the axis
slot_len = 2.15          # straight slot beyond hole B before the mouth
mouth_deg = 50.2         # mouth flank angle measured from the slot axis

# ---- engraved text on the bottom face ------------------------------------
engrave_text = True
text_str = "3.15mm"
text_size = 2.7          # font size (glyph height ~2 mm)
text_r = 11.4            # arc radius of the glyph centre line
text_depth = 2.5         # cut depth into the bottom face
text_deg = 146.5         # arc centred on hole A (bbox centre of the string)

# ========================================================================
import math

big = 60.0


def cyl_z(r, z0, z1, x=0.0, y=0.0):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def cone_z(r0, r1, z0, z1, x=0.0, y=0.0):
    return Pos(x, y, (z0 + z1) / 2) * Cone(r0, r1, z1 - z0)


def revolved(points):
    """Revolve an (r, z) polygon about the Z axis."""
    return revolve(Plane.XZ * Polygon(*points, align=None), Axis.Z, 360)


# ---- body ----------------------------------------------------------------
z_cone = body_h + cone_h            # flange underside
z_flange = z_cone + flange_h        # flange top
z_lug = z_flange + lug_h            # lug top

body = cyl_z(body_r, 0, body_h)
body += cone_z(body_r, flange_r, body_h, z_cone)
body += cyl_z(flange_r, z_cone, z_lug)

# lugs: parallel-sided blocks kept when the flange top is cut back, and
# excluded from the bore mouth chamfer so they stay full height inside
lug_blk = Pos((bore_r + flange_r) / 2, 0, (z_flange - bore_chamfer + z_lug + 1) / 2) * Box(
    flange_r - bore_r + 4, lug_w, z_lug + 1 - (z_flange - bore_chamfer))
lug_keep = Rot(0, 0, lug_deg) * lug_blk
for k in range(1, lug_count):
    lug_keep += Rot(0, 0, lug_deg + k * 360.0 / lug_count) * lug_blk
body -= cyl_z(flange_r + 1, z_flange, z_lug + 1) - lug_keep
body -= cone_z(bore_r, bore_r + big, z_flange - bore_chamfer,
               z_flange - bore_chamfer + big) - lug_keep

# flange bore, pocket floor and eccentric conical recess
body -= cyl_z(bore_r, z_cone, big)
oa = math.radians(recess_offset_deg)
recess = cone_z(recess_r_floor, recess_r_top, floor_z, z_cone,
                recess_offset * math.cos(oa), recess_offset * math.sin(oa))
body -= recess

# hub ring and the stepped shaft bore
body += cyl_z(hub_r, floor_z, hub_top)
step = shaft_cbore_r - shaft_r
body -= revolved([
    (0, -1), (shaft_cbore_r, -1), (shaft_cbore_r, shaft_cbore_h),
    (shaft_r, shaft_cbore_h + step), (shaft_r, floor_z - step),
    (shaft_cbore_r, floor_z), (shaft_cbore_r, big), (0, big)])

# ---- screw holes ---------------------------------------------------------
csk_h = (head_r - hole_r) / math.tan(math.radians(csk_deg))
z_csk = head_h + csk_h
hole_profile = [(0, -1), (head_r, -1), (head_r, head_h), (hole_r, z_csk),
                (hole_r, body_h), (0, body_h)]

hole_a = revolved(hole_profile)
body -= Rot(0, 0, hole_deg + 180) * Pos(hole_a_r, 0, 0) * hole_a

# hole B: the same profile swept radially outward (+X in the hole frame)
sweep_profile = Plane.YZ * Polygon(
    (-head_r, -1), (head_r, -1), (head_r, head_h), (hole_r, z_csk),
    (hole_r, body_h), (-hole_r, body_h), (-hole_r, z_csk), (-head_r, head_h),
    align=None)
swept = extrude(sweep_profile, amount=body_r)
if swept.bounding_box().max.X < 1:      # extrude went the other way
    swept = extrude(sweep_profile, amount=-body_r)
m = math.tan(math.radians(mouth_deg))
mouth = extrude(Pos(0, 0, -1) * Polygon(
    (slot_len, -hole_r), (slot_len + big, -hole_r - m * big),
    (slot_len + big, hole_r + m * big), (slot_len, hole_r), align=None),
    amount=body_h + 1)
hole_b = revolved(hole_profile) + swept + mouth
body -= Rot(0, 0, hole_deg) * Pos(hole_b_r, 0, 0) * hole_b

# ---- engraved text -------------------------------------------------------
if engrave_text:
    arc = Edge.make_circle(text_r, start_angle=0, end_angle=180)
    txt = Text(text_str, font_size=text_size, path=arc)
    c = txt.bounding_box().center()
    # centre the string on text_deg, then mirror across that radial plane
    # so it reads left-to-right when viewed from below
    txt = Rot(0, 0, text_deg - math.degrees(math.atan2(c.Y, c.X))) * txt
    d = math.radians(text_deg)
    txt = mirror(txt, about=Plane(origin=(0, 0, 0),
                                  x_dir=(math.cos(d), math.sin(d), 0),
                                  z_dir=(-math.sin(d), math.cos(d), 0)))
    glyphs = extrude(Pos(0, 0, -1) * txt, amount=text_depth + 1)
    body -= glyphs

# ---- place in the vendor frame -------------------------------------------
body = Pos(axis_x, axis_y, -bottom_depth) * body
show_object(body, name="coupling_interface", color="steelblue")
