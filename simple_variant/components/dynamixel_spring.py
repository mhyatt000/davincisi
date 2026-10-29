# "Dynamixel Spring (15.5mm)(M)" — ORTHOPLANAR SPRING, parametric reconstruction.
#
# SIMPLE VARIANT (differs from the vendor part described below):
#   * the horn-side flange is its own part, lower_cap.py (no keyed stud, a
#     dimple for the horn screw); this script keeps the tube from the flange
#     top (y 8.0) up, plus the spring disc;
#   * `mirror`: the tube + disc are mirrored about y = y_mirror (14.7), so a
#     second spring disc sits at the bottom with its hub ring on the lower
#     cap's top face (y 8.0). The top disc is unchanged, so the upper cap
#     (coupling_interface.py) mates as before. Shown as shaft / disc /
#     disc_lower; only the top disc carries the "15.5mm" engraving.
#
# Reverse-engineered from components/Dynamixel Spring (15.5mm)(M) (prt 4).step
# (same part as components/Orthoplanar Spring.stl) with `lamad re det all`,
# `lamad re inspect` and build123d sections. Two vendor solids:
#
#   * HUB (s2, y = -0.1 .. 17.4): a horn-side flange (r 8, 5.1 thick) with
#     4 x r1 through-holes on a 12 mm bolt circle (the XL/XC-330 horn pattern)
#     and a keyed r1.2 locating stud underneath; a r5 tube rises from the
#     flange with a stepped blind bore (r3.25 -> 0.2 chamfer -> r2.8, floor at
#     y 4.3). A 0.1 mm deep ring groove with a round (r0.5) ceiling sits in the
#     flange underside (r 4.0 .. 4.3) - a modelling artefact, kept for fidelity.
#   * SPRING DISC (s1, y = 17.4 .. 21.4): a r14 x 3 mm plate with three 3 mm
#     wide rim notches, a central hub ring (r5, counterbore r4 x 1 mm on top,
#     bore r3.25) joined to the plate by three 20.8 deg spokes, and three
#     identical through-slots (exact 120 deg polar copies) that carve each
#     spoke into a folded (hairpin) flexure beam running along the sides of a
#     triangle around the hub. "15.5mm" is engraved 0.5 mm deep in the
#     underside near the rim.
#
# All 96 B-spline faces of the vendor file are the glyph walls of that
# engraved "15.5mm" text; the flexure arm walls are planes with r0.4 fillets.
# The slot outline is kept as a measured corner table (vendor XZ plane, one
# slot) because the sketch is hand-drawn: only its fillet radius (0.4), the
# notch width (3.0), one wall length (13.33) and the 0.55 step are 'typed'
# numbers; everything else is solver-derived. The pattern is rotated 26.47 deg
# from the vendor X axis (`pattern_rot`); the rim notches sit on the triangle
# vertex directions (pattern_rot + 180 + k*120).
#
# Coordinate frame matches the vendor STEP: spring axis is +Y through the
# origin, stud at the -Y end, disc at the +Y end. Units mm. The name's
# "15.5mm" = distance from the stud tip (y -0.1) to y 15.4, where the vendor
# hub cylinder is split into three leftover faces - i.e. probably the hub
# height of an earlier revision; nothing in the current geometry is 15.5.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.
# `only="shaft"` / `"disc"` / `"disc_lower"` shows one part.

# ---- shaft: tube + bore (flange split off into lower_cap.py) -------------
tube_y0 = 8.0              # lower_cap.py's flange top
tube_r = 5.0
tube_y1 = 17.4             # tube top == disc underside
bore_r = 3.25              # main bore (also the disc bore)

# ---- symmetry --------------------------------------------------------------
mirror = True              # second disc at the bottom, mirrored about y_mirror
y_mirror = 14.7            # maps the top boss (y 21.4) onto tube_y0 (8.0)

# ---- spring disc -----------------------------------------------------------
disc_r = 14.0
disc_t = 3.0               # disc_y0 = tube_y1, disc_y1 = tube_y1 + disc_t
boss_h = 1.0               # hub ring standing above the disc (y 20.4 .. 21.4)
boss_r = 5.0
cbore_r = 4.0              # counterbore in the boss top
notch_w = 3.0
notch_floor_r = 11.1       # vendor floor is an r11.74 arc off-centre by 0.65; within 0.01 mm
notch_chamfer = 0.2        # 45 deg chamfer on the bottom edge of each notch floor
pattern_rot = 26.47        # deg, triangle side normal vs vendor +X (measured)
slot_fillet = 0.4          # fillet radius on the flexure slot corners
n_arms = 3                 # polar count of slots/notches (the slot table is drawn for 3)

# ---- engraved label --------------------------------------------------------
engrave = True
text_str = "15.5mm"
text_depth = 0.5
text_size = 2.7            # font size; vendor cap height ~1.9 mm (font differs)
text_r = 13.68             # polar position of the string's bottom-left corner
text_angle = 267.0         # deg
text_rot = 14.0            # deg, baseline rotation in the XZ plane

only = "all"               # "all" | "shaft" | "disc" | "disc_lower"

# ========================================================================
import math

R = slot_fillet
# One flexure slot, vendor XZ plane: (x, z, fillet radius). The first and
# last corners are re-projected onto the hub circle (tube_r) along their
# adjoining walls, and the outline closes with an arc on the hub circle.
SLOT = [
    (-4.72530, 1.63445, 0),       # end of hub arc
    (-7.46612, 2.97708, 0),       # spoke wall, r5 -> r8
    (-7.74114, 2.50073, 0),       # 0.55 step
    (-1.62247, -9.79051, R),      # 13.33 wall (triangle side, 5.81 from centre)
    (-3.97553, -10.96189, R),     # turn-around, 1.83 end wall
    (-10.00662, 1.15344, R),      # hairpin 1 (0.47 wide)
    (-10.42941, 0.94297, R),
    (-4.11482, -11.74185, 0),     # sharp corner at the triangle vertex
    (2.33799, -9.99647, R),
    (10.02221, 1.59744, R),       # hairpin 2 (0.50 wide)
    (9.60466, 1.87419, R),
    (2.14027, -9.38806, R),       # 0.4 fillet into the horizontal
    (-0.85980, -9.38806, R),      # horizontal z = -9.388
    (-0.85980, -4.92551, 0),      # vertical x = -0.8598 (spoke wall) up to hub
]

_show = show_object
def show_object(obj, name, **kw):
    if only in ("all", name):
        _show(obj, name=name, **kw)

disc_y0 = tube_y1
disc_y1 = tube_y1 + disc_t
boss_y1 = disc_y1 + boss_h

# ---- helpers (everything is built along the vendor +Y axis) ---------------
def cyl_y(r, y0, y1, x=0.0, z=0.0):
    return Pos(x, (y0 + y1) / 2, z) * (Plane.XZ * Cylinder(r, y1 - y0))

def prism_y(face_xz, y0, y1):
    """Extrude a face lying in Plane.XZ (local u=x, v=z) from y0 up to y1
    (symmetric extrude, so the wire's winding direction does not matter)."""
    return extrude(Pos(0, (y0 + y1) / 2, 0) * face_xz, (y1 - y0) / 2, both=True)

def ray_circle(p, q, r):
    """Point on the ray p->q at distance r from the origin (nearest beyond p)."""
    d = (q - p).normalized()
    b = p.dot(d)
    c = p.dot(p) - r * r
    roots = [-b - math.sqrt(b * b - c), -b + math.sqrt(b * b - c)]
    s = min(t for t in roots if t > 1e-9)
    return p + d * s

def rounded_outline(verts, close_r=None, close_long=False):
    """Face in the XY sketch plane from (u, v, fillet_r) corners joined by
    lines; the last->first segment is a straight line, or an arc of radius
    close_r about the origin if close_r is given (short way, or long way if
    close_long). Fillets whose tangent points overrun each other (slot
    width < 2r, the vendor's hairpins) are trimmed to their intersection."""
    P = [Vector(u, v, 0) for u, v, _ in verts]
    n = len(P)
    fil = [None] * n
    for i, (u, v, r) in enumerate(verts):
        if r <= 0 or i == 0 or i == n - 1:
            continue
        a = (P[i - 1] - P[i]).normalized()
        b = (P[i + 1] - P[i]).normalized()
        th = math.acos(max(-1.0, min(1.0, a.dot(b))))
        t = r / math.tan(th / 2)
        bis = (a + b).normalized()
        fil[i] = [P[i] + a * t, P[i] + b * t, P[i] + bis * (r / math.sin(th / 2)), r]
    # overlapping fillets -> circle/circle intersection nearest the end wall
    for i in range(n - 1):
        j = i + 1
        if fil[i] and fil[j]:
            seg = P[j] - P[i]
            if (fil[j][0] - fil[i][1]).dot(seg) < 0:
                c1, c2, r = fil[i][2], fil[j][2], fil[i][3]
                mid = (c1 + c2) / 2
                d = (c2 - c1).length
                h = math.sqrt(max(r * r - (d / 2) ** 2, 0.0))
                perp = Vector(-(c2 - c1).Y, (c2 - c1).X, 0).normalized()
                wall = (P[i] + P[j]) / 2
                cands = [mid + perp * h, mid - perp * h]
                p = min(cands, key=lambda q: (q - wall).length)
                fil[i][1] = p
                fil[j][0] = p
    edges = []
    def arc(c, r, a, b):
        m = c + ((a - c) + (b - c)).normalized() * r
        return ThreePointArc(a, m, b)
    start = [fil[i][0] if fil[i] else P[i] for i in range(n)]
    end = [fil[i][1] if fil[i] else P[i] for i in range(n)]
    for i in range(n):
        if fil[i]:
            edges.append(arc(fil[i][2], fil[i][3], fil[i][0], fil[i][1]))
        if i < n - 1:
            a, b = end[i], start[i + 1]
            if (b - a).length > 1e-6:
                edges.append(Line(a, b))
    a, b = end[n - 1], start[0]
    if close_r is None:
        edges.append(Line(a, b))
    else:
        a0 = math.atan2(a.Y, a.X)
        a1 = math.atan2(b.Y, b.X)
        d = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        if close_long:
            d -= math.copysign(2 * math.pi, d)
        am = a0 + d / 2
        edges.append(ThreePointArc(a, Vector(close_r * math.cos(am), close_r * math.sin(am), 0), b))
    return make_face(Wire(edges))

# ---- shaft (the vendor hub's tube) ----------------------------------------
y_lo = 2 * y_mirror - tube_y1 if mirror else tube_y0   # shaft bottom
shaft = cyl_y(tube_r, y_lo, tube_y1) - cyl_y(bore_r, y_lo - 1, tube_y1 + 1)

# ---- spring disc (vendor solid s1) ----------------------------------------
disc = cyl_y(disc_r, disc_y0, disc_y1)
# rim notches on the triangle-vertex directions
for k in range(n_arms):
    ang = pattern_rot + 180 + 360 * k / n_arms
    x0, x1 = notch_floor_r - 1, disc_r + 2
    cutter = Rot(0, -ang, 0) * (
        Pos((x0 + x1) / 2, (disc_y0 + disc_y1) / 2, 0) * Box(x1 - x0, disc_t + 2, notch_w))
    disc -= cutter - cyl_y(notch_floor_r, disc_y0 - 2, disc_y1 + 2)
if notch_chamfer > 0:
    floor_edges = [e for e in disc.edges()
                   if e.geom_type == GeomType.CIRCLE and abs(e.radius - notch_floor_r) < 1e-3
                   and abs(e.arc_center.Y - disc_y0) < 1e-3]
    disc = chamfer(floor_edges, notch_chamfer)
# flexure slots: one measured outline, polar-patterned n_arms times
slot_verts = list(SLOT)
p0 = ray_circle(Vector(*SLOT[1][:2], 0), Vector(*SLOT[0][:2], 0), tube_r)
p1 = ray_circle(Vector(*SLOT[-2][:2], 0), Vector(*SLOT[-1][:2], 0), tube_r)
slot_verts[0] = (p0.X, p0.Y, 0)
slot_verts[-1] = (p1.X, p1.Y, 0)
slot_face = rounded_outline(slot_verts, close_r=tube_r)
slot = prism_y(Plane.XZ * slot_face, disc_y0 - 1, disc_y1 + 1)
for k in range(n_arms):
    disc -= Rot(0, 360 * k / n_arms, 0) * slot
# hub ring with counterbore and bore
disc += cyl_y(boss_r, disc_y0, boss_y1)
disc -= cyl_y(cbore_r, disc_y1, boss_y1 + 1)
disc -= cyl_y(bore_r, disc_y0 - 1, boss_y1 + 1)
# the lower disc is the un-engraved disc, mirrored
disc_lower = disc.mirror(Plane.XZ.offset(-y_mirror)) if mirror else None
# engraved label in the underside (top disc only)
if engrave:
    txt = Text(text_str, font_size=text_size, align=(Align.MIN, Align.MIN))
    ta = math.radians(text_angle)
    txt = Pos(text_r * math.cos(ta), text_r * math.sin(ta), 0) * Rot(0, 0, text_rot) * txt
    for glyph in prism_y(Plane.XZ * txt, disc_y0 - 1, disc_y0 + text_depth).solids():
        disc -= glyph

show_object(shaft, name="shaft", color="goldenrod")
show_object(disc, name="disc", color="steelblue")
if mirror:
    show_object(disc_lower, name="disc_lower", color="steelblue")
