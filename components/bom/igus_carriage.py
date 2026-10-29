# Igus DryLin T TW-04-15 carriage — parametric reconstruction.
#
# Reverse-engineered from components/Vendor/Igus drylin T TW-04-15 carriage.step
# (vendor-authoritative STEP from igus-cad.com) with `lamad re det all` +
# `lamad re inspect`. Three solids in the vendor file:
#
#   * p1:s1  the aluminium carriage body, 32 x 42 x 13.2 mm, 201 faces.
#     A 27 mm wide core block (full 42 mm length) with two 30 mm long
#     mounting wings on the sides that bring the width to 32 mm. The wing
#     tops are raised 0.3 mm pads (z = 7.5 vs 7.2 for the core) joined by
#     a 45 deg step, and the wings' lower outer corner is a 45 deg chamfer.
#     Underneath, a full-length channel for the rail: two R4 bores on
#     x = +-6.2 joined by a 7.9 mm wide ceiling at z = 3.3, with a 7.5 mm
#     wide bottom slot whose edges are thin lips (r0.3 / r0.4 rounds) and
#     15 deg lead-in slopes. Four M3 threaded through-holes (modelled at
#     the minor diameter 2.459 with 45 deg chamfers to 3.0 at both ends)
#     at x = +-12.5, y = 11 / 31 (25 x 20 mm pattern) with 6 mm x 2 mm
#     counterbores from below. All external edges have r0.5 rounds.
#   * p2:s1 / p2:s2  two identical mirror-image plastic (iglidur) liners
#     that sit in the R4 bores, 41 mm long (y 0.5 .. 41.5). Each is a C
#     section: R4 outside spanning +-120 deg, flat tab at x = +-4.2, and
#     a rectangular 4.6 mm tall bore that wraps the 17 mm wide rail flange
#     (x = +-8.5, z = +-2.3, r0.2 inside corners, 0.2 mm 45 deg lead-ins).
#     A 6 mm long notch in the middle (y 18 .. 24) relieves the outside of
#     the liner to x = +-9.5 / z = +-3.3 (r1.7 corners, 30 deg ramps).
#
# Simplifications (together 0.013 % of the volume, IoU 0.99987 against
# the STEP): the raised "igus" lettering inside the 5 x 10 x 0.3 mm logo
# pocket on top is omitted (pocket kept; 1.31 mm^3 missing); the vendor's
# odd r0.5 round on the bottom edge of the end faces (centre 0.3 mm above
# the bottom, so only a 0.04 mm sliver is removed) is left sharp
# (0.08 mm^3 extra); the corner blends where the r0.5 rounds meet at the
# top of the core's vertical corners are OCC's rather than the vendor's
# (0.03 mm^3). Everything else is analytic and reproduced.
#
# Coordinate frame matches the vendor file: rail runs along Y, carriage
# spans y 0 .. 42, x +-16, z -5.7 .. 7.5; the two rail-bore axes are
# (+-6.2, *, 0) and the mounting face is z = 7.5. Units mm.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.
# (Negative literals are not picked up as params, so values below z = 0
# are given as positive magnitudes and negated where used.)

# ---- body envelope -------------------------------------------------------
body_len = 42.0          # Y, 0 .. body_len
core_w = 27.0            # X width of the full-length core block
wing_w = 32.0            # X width across the mounting wings
wing_len = 30.0          # wings are centred on the length (y 6 .. 36)
top_z = 7.2              # core top
pad_z = 7.5              # wing mounting pads
pad_inner_x = 8.0        # pads start here; 45 deg step down to top_z inboard
bottom_z = 5.7           # bottom face at z = -bottom_z
wing_wall_z = 2.7        # wing outer wall ends at z = -wing_wall_z, then
                         # a 45 deg chamfer tangent to the r0.5 rounds
edge_r = 0.5             # every external r0.5 round

# ---- rail channel (XZ profile, runs along Y) -----------------------------
bore_r = 4.0
bore_x = 6.2             # bore axes at x = +-bore_x, z = 0
ceiling_z = 3.3          # flat between the bores
lip_z = 3.4              # bottom lips top at z = -lip_z
slot_half_w = 3.75       # bottom slot x = +-slot_half_w
lip_r = 0.3              # round lip / slot wall
slope_deg = 15.0         # lead-in slope from the slot wall to the bottom
slope_x = 6.25           # slope meets the bottom face at x = +-slope_x
slope_r = 0.4            # round slot wall / slope

# ---- mounting holes (M3, 25 x 20 pattern) --------------------------------
hole_x = 12.5
hole_pitch_y = 20.0      # centred on the length: y = 11 and 31
thread_minor_r = 1.2295  # M3 minor diameter 2.459
thread_major_r = 1.5     # 45 deg chamfers open to 3.0 at both faces
pad_bottom_z = 3.7       # underside of the wing pad at z = -pad_bottom_z
cbore_r = 3.0            # 6 mm counterbore from below ...
cbore_depth = 2.0        # ... up to the pad underside

# ---- logo pocket on top --------------------------------------------------
pocket_w = 5.0           # X
pocket_l = 10.0          # Y, centred on the length
pocket_depth = 0.3

# ---- liners --------------------------------------------------------------
liner_len = 41.0         # y 0.5 .. 41.5, centred on the body
liner_span_deg = 120.0   # outer R4 arc +-liner_span_deg about the bore axis
rail_half_w = 8.5        # liner bore x = +-rail_half_w (rail flange 17 wide)
flange_half_t = 2.3      # liner bore z = +-flange_half_t
bore_corner_r = 0.2
bore_lead_in = 0.2       # 45 deg chamfer at the bore mouth
notch_len = 6.0          # centre notch, y 18 .. 24
notch_x = 9.5            # notch relieves the outside to x = +-notch_x ...
notch_z = 3.3            # ... and z = +-notch_z
notch_r = 1.7
notch_ramp_deg = 30.0    # ramp from the z = notch_z flat down to the tab
notch_wall_x = 4.7       # tab wall inside the notch
notch_ramp_run = 1.0     # ramp spans x = notch_wall_x .. notch_wall_x + run

include_body = True
include_liners = True

# ========================================================================
import math

big = 3 * body_len


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(
        x1 - x0, y1 - y0, z1 - z0)


def prism(sketch_xz, y0, y1):
    """Extrude an XZ sketch (local u = x, v = z) along Y from y0 to y1.
    extrude() follows the face normal, which flips with polygon winding,
    so extrude both ways and clip to the slab."""
    solid = extrude(Plane.XZ * sketch_xz, amount=big, both=True)
    return solid & box(-big, big, y0, y1, -big, big)


def cyl_z(r, z0, z1, x=0.0, y=0.0):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def verts_near(shape, pts, tol=1e-3):
    """2D vertices of a sketch near any of the (u, v) points."""
    out = []
    for v in shape.vertices():
        for (u, w) in pts:
            if abs(v.X - u) < tol and abs(v.Y - w) < tol:
                out.append(v)
                break
    if len(out) != len(pts):
        raise ValueError(f"expected {len(pts)} vertices, found {len(out)}")
    return out


def y_edges_at(solid, pts, tol=1e-3):
    """Edges of a solid parallel to Y whose (x, z) matches one of pts."""
    out = []
    for e in solid.edges():
        d = e @ 1 - e @ 0
        if d.length < 1e-9 or abs(d.normalized().Y) < 0.999:
            continue
        c = e.center()
        if any(abs(c.X - u) < tol and abs(c.Z - w) < tol for (u, w) in pts):
            out.append(e)
    if len(out) != len(pts):
        raise ValueError(f"expected {len(pts)} edges, found {len(out)}")
    return out


zb = -bottom_z
core_hw = core_w / 2
wing_hw = wing_w / 2
y_mid = body_len / 2
wing_y0, wing_y1 = y_mid - wing_len / 2, y_mid + wing_len / 2

# ---- body: full-length core ---------------------------------------------
# Built sharp, then its four vertical corners are rounded while the
# bottom edges are still square (OCC propagates a fillet along tangent
# edge chains, so rounding the verticals after the bottom round would
# also round the bottom edge of the end faces, which the vendor leaves
# sharp). The bottom corner round (centre (13, -5.2)) is then cut with an
# explicit cutter along the full length; it is the same circle that
# rounds the wings' chamfer/bottom edge, so the surface is continuous.
core = box(-core_hw, core_hw, 0, body_len, zb, top_z)


def is_vertical_at(e, x, ys):
    if e.geom_type != GeomType.LINE:
        return False
    c = e.center()
    d = (e @ 1 - e @ 0).normalized()
    return abs(d.Z) > 0.999 and abs(abs(c.X) - x) < 1e-4 and any(
        abs(c.Y - y) < 1e-4 for y in ys)


core = fillet([e for e in core.edges() if is_vertical_at(e, core_hw, (0, body_len))],
              edge_r)
for sx in (-1, 1):
    cx = sx * (core_hw - edge_r)
    corner = box(min(cx, sx * core_hw), max(cx, sx * core_hw), -1, body_len + 1,
                 zb, zb + edge_r)
    core -= corner - Pos(cx, y_mid, zb + edge_r) * Rot(90, 0, 0) * Cylinder(
        edge_r, body_len + 4)
body = core

# ---- body: mounting wings ------------------------------------------------
# The 45 deg lower chamfer is the common tangent of two r0.5 rounds: the
# one ending the x = 16 wall at z = -2.7 and the one at the bottom corner
# of the core (x = 13.5, z = -5.7). That is why the vendor's chamfer plane
# sits at x - z = 18.907 rather than a round number.
chamfer_c = (wing_hw - edge_r) + wing_wall_z + edge_r * math.sqrt(2)
chamfer_z_top = wing_hw - chamfer_c            # on the x = 16 wall
chamfer_x_bot = chamfer_c + zb                 # on the bottom face
pad_step_x = pad_inner_x - (pad_z - top_z)     # 45 deg step starts here
wing_prof = Polygon(
    (pad_step_x, top_z), (pad_inner_x, pad_z), (wing_hw, pad_z),
    (wing_hw, chamfer_z_top), (chamfer_x_bot, zb), (pad_step_x, zb),
    align=None)
wing_prof = fillet(verts_near(wing_prof, [(chamfer_x_bot, zb)]), edge_r)
wing = prism(wing_prof, wing_y0, wing_y1)
body = body + wing + mirror(wing, about=Plane.YZ)


# r0.5 rounds on the remaining sharp outer edges, done as ONE fillet so
# OCC blends the corners where they meet: wing top edges, wing wall /
# chamfer edges, core top edges at the ends, the top edges of the two end
# faces, and the four vertical wing corners.
def is_outer_edge(e):
    if e.geom_type != GeomType.LINE:
        return False
    c = e.center()
    d = (e @ 1 - e @ 0).normalized()
    t = 1e-4
    at_wing_x = abs(abs(c.X) - wing_hw) < t
    at_core_x = abs(abs(c.X) - core_hw) < t
    at_end_y = abs(c.Y) < t or abs(c.Y - body_len) < t
    at_wing_y = abs(c.Y - wing_y0) < t or abs(c.Y - wing_y1) < t
    if abs(d.Z) > 0.999:                       # vertical wing corners
        return at_wing_x and at_wing_y
    if abs(d.X) > 0.999:                       # end-face top edges
        return abs(c.Z - top_z) < t and at_end_y
    if abs(d.Y) > 0.999:                       # edges along the rail
        if at_wing_x:
            return abs(c.Z - pad_z) < t or abs(c.Z - chamfer_z_top) < t
        if at_core_x:
            return abs(c.Z - top_z) < t
    return False


body = fillet([e for e in body.edges() if is_outer_edge(e)], edge_r)

# ---- body: rail channel --------------------------------------------------
slope_t = math.tan(math.radians(slope_deg))
slot_z_wall = zb + (slope_x - slot_half_w) * slope_t   # slope meets the wall
x_far = slope_x + 3
z_far = zb - (x_far - slope_x) * slope_t
chan = Pos(bore_x, 0) * Circle(bore_r) + Pos(-bore_x, 0) * Circle(bore_r)
chan += Pos(0, (ceiling_z - lip_z) / 2) * Rectangle(2 * bore_x, ceiling_z + lip_z)
chan += Polygon(
    (-slot_half_w, -lip_z + 0.5), (slot_half_w, -lip_z + 0.5),
    (slot_half_w, slot_z_wall), (slope_x, zb), (x_far, z_far),
    (x_far, zb - 3), (-x_far, zb - 3), (-x_far, z_far), (-slope_x, zb),
    (-slot_half_w, slot_z_wall), align=None)
channel = prism(chan, -1, body_len + 1)
channel = fillet(y_edges_at(channel, [(slot_half_w, -lip_z),
                                      (-slot_half_w, -lip_z)]), lip_r)
channel = fillet(y_edges_at(channel, [(slot_half_w, slot_z_wall),
                                      (-slot_half_w, slot_z_wall)]), slope_r)
body -= channel

# ---- body: M3 holes with chamfers and counterbores -----------------------
zpb = -pad_bottom_z
ch = thread_major_r - thread_minor_r          # 45 deg chamfer depth
for sx in (-1, 1):
    for sy in (-1, 1):
        x, y = sx * hole_x, y_mid + sy * hole_pitch_y / 2
        body -= cyl_z(thread_minor_r, zpb - 1, pad_z + 1, x, y)
        body -= Pos(x, y, pad_z - ch / 2) * Cone(thread_minor_r, thread_major_r, ch)
        body -= cyl_z(thread_major_r, pad_z, pad_z + 1, x, y)
        body -= Pos(x, y, zpb + ch / 2) * Cone(thread_major_r, thread_minor_r, ch)
        body -= cyl_z(cbore_r, zpb - cbore_depth - 1, zpb, x, y)

# ---- body: logo pocket ---------------------------------------------------
body -= box(-pocket_w / 2, pocket_w / 2, y_mid - pocket_l / 2,
            y_mid + pocket_l / 2, top_z - pocket_depth, top_z + 1)

# ---- liners --------------------------------------------------------------
# Right-hand liner built around the bore at (+bore_x, 0), then mirrored.
tab_x = bore_x + bore_r * math.cos(math.radians(liner_span_deg))   # 4.2
lin = Pos(bore_x, 0) * Circle(bore_r)
lin -= Pos(tab_x - big / 2, 0) * Rectangle(big, big)               # flat tab
lin -= Pos((tab_x - big + rail_half_w) / 2, 0) * Rectangle(
    rail_half_w - tab_x + big, 2 * flange_half_t)                   # bore
liner_y0 = y_mid - liner_len / 2
liner = prism(lin, liner_y0, liner_y0 + liner_len)
liner = fillet(y_edges_at(liner, [(rail_half_w, flange_half_t),
                                  (rail_half_w, -flange_half_t)]),
               bore_corner_r)
liner = chamfer(y_edges_at(liner, [(tab_x, flange_half_t),
                                   (tab_x, -flange_half_t)]), bore_lead_in)

# centre notch: outside relieved to a rounded rectangle with 30 deg ramps
ramp_z = notch_z - notch_ramp_run * math.tan(math.radians(notch_ramp_deg))
notch_prof = Polygon(
    (notch_wall_x, flange_half_t), (notch_wall_x, ramp_z),
    (notch_wall_x + notch_ramp_run, notch_z), (notch_x, notch_z),
    (notch_x, -notch_z), (notch_wall_x + notch_ramp_run, -notch_z),
    (notch_wall_x, -ramp_z), (notch_wall_x, -flange_half_t),
    (rail_half_w, -flange_half_t), (rail_half_w, flange_half_t),
    align=None)
ny0, ny1 = y_mid - notch_len / 2, y_mid + notch_len / 2
keep = prism(notch_prof, ny0 - 1, ny1 + 1)
keep = fillet(y_edges_at(keep, [(notch_x, notch_z), (notch_x, -notch_z)]),
              notch_r)
keep = fillet(y_edges_at(keep, [(rail_half_w, flange_half_t),
                                (rail_half_w, -flange_half_t)]),
              bore_corner_r)
liner -= box(0, big, ny0, ny1, -big, big) - keep
liner_l = mirror(liner, about=Plane.YZ)

if include_body:
    show_object(body, name="carriage_body", color="silver")
if include_liners:
    show_object(liner, name="liner_right", color="darkorange")
    show_object(liner_l, name="liner_left", color="darkorange")
