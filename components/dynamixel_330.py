# DYNAMIXEL XL330 / XC330 case (shared housing) — parametric reconstruction.
#
# Reverse-engineered from the official Robotis dummy STEP (XL,XC-330.stp,
# Creo 2020) with `lamad re inspect`, one vendor solid at a time.
# Coordinate frame matches the vendor file: output (horn) axis is +Z through
# the origin, the front-cap / middle-case seam is z = 0, the body extends
# toward -Y (horn axis is 9.5 mm from the +Y end of the 34 mm body). Units mm.
# Exterior envelope + mounting interfaces are faithful; internal gearbox
# cavities are not modelled (the vendor dummy is solid inside, and its parts
# interpenetrate in places — e.g. the back-case towers and the middle case).
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.
# `only="case_back"` (etc.) shows a single vendor part for component compares.

# ---- body envelope -------------------------------------------------------
W = 20.0            # case width (X)
L = 34.0            # case length (Y)
horn_offset = 9.5   # horn axis distance from the +Y end face
corner_c = 1.0      # 45° chamfer on the four vertical body edges
edge_c = 0.2        # chamfer on the front-top and back-bottom perimeter
z_front_top = 3.5
z_front_bot = -0.5  # front cap skirt overlaps the middle case tongue
z_mid_top = 0.0     # middle case tongue tops / front cap pocket floor
z_mid_wall_hi = -0.55
z_mid_wall_lo = -14.45
z_mid_bot = -15.0
z_back_top = -14.5  # back cap rim
z_back_bot = -19.5
tongue_inset = 0.45  # middle case tongues (both ends)
pocket_inset = 0.4   # matching pockets in the front and back caps

# ---- middle case ---------------------------------------------------------
boss_r = 2.5         # bearing boss standing up into the front cap
boss_top = 3.5
mid_pin_r = 1.1      # short blind hole from the bottom on the horn axis
mid_pin_top = -14.3

# ---- side connector windows (middle + back) ------------------------------
win_x = 6.0          # inner wall of the window, |x|
win_y0 = -14.25
win_y1 = -3.75
win_c = 0.3          # chamfer on the window's inner corners
win_mid_top = -10.2  # window ceiling in the middle case
tower_x_in = 5.3     # back-case towers that frame each connector
tower_x_out = 9.5
tower_y0 = -14.95
tower_y1_r = -3.05
tower_y1_l = -3.121
tower_top = -11.9
tower_clear_r = 6.0  # gear clearance arc cut from the left tower
tower_clear_x = -0.8
tower_clear_y = -17.6
latch_w = 0.5        # connector latch bumps on the window wall
latch_len = 1.5
latch_z0 = -17.25
latch_z1 = -16.4

# ---- front cap -----------------------------------------------------------
front_bore_r = 3.0       # z 0 .. 0.5
front_bore_step = 0.5
front_cbore_r = 3.9      # houses the horn hub
front_cbore_top = 2.9    # then a 45° chamfer up to the face
ring_r0 = 5.0            # shallow ring groove around the horn (front and back)
ring_r1 = 7.0
ring_d = 0.3
key_w = 0.5              # alignment slit at the +Y end
key_d = 0.2
key_wall = 0.2
label_w = 13.3           # label recess
label_l = 5.8
label_y = -15.4
label_r = 0.5
label_d = 0.2

# ---- back cap ------------------------------------------------------------
back_boss_top = -13.5
back_bore_r = 3.35       # idler recess
back_bore_top = -18.3
back_bore2_r = 2.6
back_bore2_top = -17.7
back_pin_r = 1.1
back_pin_top = -14.3
led_w = 5.0              # LED window at the +Y end of the back cap
led_y = 7.5
led_step_y = 8.5
led_step_z = -17.5

# ---- mounting pattern (4x M2 tapped, 16 x 30 mm) ------------------------
mount_pitch_x = 16.0
mount_pitch_y = 30.0
mount_hole_r = 0.8     # M2 tap drill in the middle case
mount_clear_r = 1.0    # clearance in the front/back caps

# ---- case assembly screws (4x PHS 1.7 x 20.5, asymmetric pattern) --------
screw_hole_mid_r = 0.8
screw_hole_front_r = 0.9
screw_cbore_r = 1.6     # counterbore opens out to the nearest side
screw_cbore_floor = 2.0
screw_hole_back_r = 0.7
screw_hole_back_floor = -18.8
phs_len = 20.5
phs_shank_r = 0.7
phs_thread_r = 0.85
phs_thread_len = 4.0    # thread at the tip, larger than the shank
phs_tip_c = 0.15

# ---- output horn ---------------------------------------------------------
horn_r = 8.0
horn_z0 = 3.6
horn_z1 = 6.5
horn_c = 0.2
hub_r0 = 3.70          # hub tapers 3° outward toward the flange
hub_r1 = 3.84
hub_z0 = 0.9
hub_fillet = 0.5
hub_bore_r = 2.5       # rides on the middle case boss
hub_bore_c = 0.3
hub_bore_top = 3.5
horn_bore_r = 1.3
horn_key_w = 1.45
horn_key_y = 2.1
horn_recess_r = 2.8
horn_recess_floor = 4.9
horn_hole_r = 0.8      # 4x M2 tap holes in the horn
horn_hole_bc = 6.0     # on a 12 mm bolt circle (radius)
horn_mark_w = 0.4      # index slot at +Y
horn_mark_d = 0.2

# ---- idler horn / cap (back) ---------------------------------------------
idler_z0 = -22.5
idler_z1 = -19.6
idler_stem_r = 3.25
idler_stem_top = -18.35
idler_fillet = 0.3
idler_bore_r = 2.5
idler_cbore_r = 3.6
idler_cbore_top = -20.0
icap_r = 3.4
icap_z0 = -22.3
icap_z1 = -20.1
icap_stem_r = 2.4
icap_top = -17.7
icap_fillet = 0.2
icap_pocket_r = 2.8
icap_pocket_top = -20.7
icap_hole_r = 1.4

# ---- horn screws (2x BTS M2.6 x 8 button head) --------------------------
bts_len = 8.0
bts_r = 1.3
bts_head_r = 2.75
bts_head_h = 1.565
horn_screw_z = 4.9     # underside of the head
idler_screw_z = -20.7

# ---- side connectors (2x JST B3B-EH) -------------------------------------
conn_x0 = 6.1
conn_x1 = 9.9
conn_y0 = -14.0
conn_y1 = -4.0
conn_roof0 = -11.9
conn_roof1 = -10.4
conn_bot = -16.4
conn_back = 0.502
conn_end = 0.45
conn_pin = 0.64
conn_pin_x = 7.7
conn_pin_y = -9.0
conn_pitch = 2.5
conn_pin_z0 = -15.9
conn_pin_z1 = -7.2

include_screws = True
include_connectors = True
include_led = True
only = "all"           # show one part by name (component-level compare)

# ========================================================================
import math

yc = horn_offset - L / 2          # body centre in Y (-7.5 for stock values)
big = 100.0  # generous cutter length

_show = show_object
def show_object(obj, name, **kw):
    if only in ("all", name):
        _show(obj, name=name, **kw)

def cyl_z(r, z0, z1, x=0.0, y=0.0):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)

def cone_z(r0, r1, z0, z1, x=0.0, y=0.0):
    return Pos(x, y, (z0 + z1) / 2) * Cone(r0, r1, z1 - z0)

def ring_z(r0, r1, z0, z1):
    return cyl_z(r1, z0, z1) - cyl_z(r0, z0 - 1, z1 + 1)

def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)

def footprint(d, z):
    """Body outline inset by d (mitred, so the corner chamfers stay 45°)."""
    hx, y0, y1 = W / 2 - d, yc - L / 2 + d, yc + L / 2 - d
    c = corner_c - d * (2 - math.sqrt(2))
    pts = [(-hx + c, y0), (hx - c, y0), (hx, y0 + c), (hx, y1 - c),
           (hx - c, y1), (-hx + c, y1), (-hx, y1 - c), (-hx, y0 + c)]
    return Pos(0, 0, z) * Polygon(*pts, align=None)

def prism(d, z0, z1):
    return extrude(footprint(d, z0), z1 - z0)

def bevel(z_edge, z_in):
    """45° perimeter chamfer band between the face at z_edge and z_in."""
    return loft([footprint(abs(z_in - z_edge), z_edge), footprint(0, z_in)], ruled=True)

def window(sx, z0, z1):
    x0, x1 = sx * win_x, sx * (W / 2 + 2)
    pts = [(x0 + sx * win_c, win_y0), (x1, win_y0), (x1, win_y1),
           (x0 + sx * win_c, win_y1), (x0, win_y1 - win_c), (x0, win_y0 + win_c)]
    if sx < 0:
        pts.reverse()  # keep the face normal +Z so the extrude runs upward
    return extrude(Pos(0, 0, z0) * Polygon(*pts, align=None), z1 - z0)

def edges_at(shape, z, r):
    return [e for e in shape.edges()
            if e.geom_type == GeomType.CIRCLE and abs(e.center().Z - z) < 1e-3
            and abs(e.radius - r) < 1e-2]

def cross_recess(r_out, arm, c, rc, z0, z1):
    h = z1 - z0
    cut = box(-r_out, r_out, -arm, arm, z0, z1) + box(-arm, arm, -r_out, r_out, z0, z1)
    centre = box(-c, c, -c, c, z0, z1)
    for sx in (-1, 1):
        for sy in (-1, 1):
            centre -= cyl_z(rc, z0 - 1, z1 + 1, sx * c, sy * c)
    return (cut + centre) & cyl_z(r_out, z0, z1)

def pan_head(R_t, r_t, z_band, z_top):
    """Head with underside at z=0: toroidal rim up to z_band, spherical dome to z_top."""
    zc = z_band / 2
    band = (Pos(0, 0, zc) * Torus(R_t, r_t) + cyl_z(R_t, zc - r_t, zc + r_t)) & cyl_z(R_t + r_t, 0, z_band)
    r_band = R_t + math.sqrt(r_t ** 2 - zc ** 2)
    h = z_top - z_band
    R_s = (r_band ** 2 + h ** 2) / (2 * h)
    dome = (Pos(0, 0, z_top - R_s) * Sphere(R_s)) & cyl_z(r_band + 1, z_band, z_top)
    return band + dome

def bts_screw():
    """BTS M2.6 x 8 button-head screw, head underside at z = 0, pointing -Z."""
    s = pan_head(bts_head_r - 0.608, 0.608, 1.12, bts_head_h)
    s += cyl_z(bts_r, -bts_len + 0.225, 0) + cone_z(bts_r - 0.225, bts_r, -bts_len, -bts_len + 0.225)
    s -= cross_recess(1.55, 0.269, 0.919, 0.65, 0.8, big)
    return s

def phs_screw():
    """PHS 1.7 x 20.5 pan-head screw, head underside at z = 0, pointing -Z."""
    s = pan_head(0.95, 0.55, 0.899, 1.259)
    z_t = -phs_len + phs_thread_len
    s += cyl_z(phs_shank_r, z_t, 0)
    s += cyl_z(phs_thread_r, -phs_len + phs_tip_c, z_t)
    s += cone_z(phs_thread_r - phs_tip_c, phs_thread_r, -phs_len, -phs_len + phs_tip_c)
    s -= cross_recess(1.1, 0.176, 0.601, 0.425, 0.65, big)
    return s

mount_xy = [(sx * mount_pitch_x / 2, yc + sy * mount_pitch_y / 2)
            for sx in (-1, 1) for sy in (-1, 1)]
screw_xy = [(8.4, 4.5), (-8.4, 4.5), (4.9, -22.9), (-8.4, -19.4)]
screw_dir = [(1, 0), (-1, 0), (0, -1), (-1, 0)]   # counterbore opens this way

# ---- middle case ---------------------------------------------------------
mid = prism(0, z_mid_wall_lo, z_mid_wall_hi)
mid += prism(tongue_inset, z_mid_bot, z_mid_top)
mid += cyl_z(boss_r, z_mid_top, boss_top)
for x, y in mount_xy + screw_xy:
    mid -= cyl_z(mount_hole_r if (x, y) in mount_xy else screw_hole_mid_r, -big, z_mid_top + 0.5, x, y)
for sx in (-1, 1):
    mid -= window(sx, -big, win_mid_top)
mid -= cyl_z(mid_pin_r, -big, mid_pin_top)

# ---- front cap -----------------------------------------------------------
front = prism(0, z_front_bot, z_front_top - edge_c) + bevel(z_front_top, z_front_top - edge_c)
front -= prism(pocket_inset, -big, z_mid_top)
front -= cyl_z(front_bore_r, -big, z_mid_top + front_bore_step)
front -= cyl_z(front_cbore_r, z_mid_top + front_bore_step, front_cbore_top)
front -= cone_z(front_cbore_r, front_cbore_r + big, front_cbore_top, front_cbore_top + big)
front -= ring_z(ring_r0, ring_r1, z_front_top - ring_d, big)
front -= box(-key_w / 2, key_w / 2, ring_r1 - 0.1, big, z_front_top - key_d, big)
front -= box(-key_w / 2, key_w / 2, yc + L / 2 - key_wall, big, -big, big)
front -= Pos(0, label_y, z_front_top - label_d) * extrude(RectangleRounded(label_w, label_l, label_r), big)
for x, y in mount_xy:
    front -= cyl_z(mount_clear_r, -big, big, x, y)
for (x, y), (dx, dy) in zip(screw_xy, screw_dir):
    front -= cyl_z(screw_hole_front_r, -big, big, x, y)
    slot = SlotCenterToCenter(10, 2 * screw_cbore_r, rotation=math.degrees(math.atan2(dy, dx)))
    front -= Pos(x + 5 * dx, y + 5 * dy, screw_cbore_floor) * extrude(slot, big)

# ---- back cap ------------------------------------------------------------
back = prism(0, z_back_bot + edge_c, z_back_top) + bevel(z_back_bot, z_back_bot + edge_c)
back -= prism(pocket_inset, z_mid_bot, big)
for sx, y1 in ((1, tower_y1_r), (-1, tower_y1_l)):
    xs = sorted((sx * tower_x_in, sx * tower_x_out))
    t = box(xs[0], xs[1], tower_y0, y1, z_mid_bot, tower_top)
    t += box(*sorted((sx * tower_x_in, sx * (W / 2 - pocket_inset))), tower_y0, y1, z_mid_bot, z_back_top)
    if sx < 0:
        t -= cyl_z(tower_clear_r, -big, big, tower_clear_x, tower_clear_y)
    back += t
for sx in (-1, 1):
    back -= window(sx, -big, tower_top + 1)
    for y0 in (win_y0, win_y1 - latch_len):
        back += box(*sorted((sx * win_x, sx * (win_x + latch_w))), y0, y0 + latch_len, latch_z0, latch_z1)
for x, y in mount_xy:
    back -= cyl_z(mount_clear_r, -big, big, x, y)
for x, y in screw_xy:
    back -= cyl_z(screw_hole_back_r, screw_hole_back_floor, big, x, y)
back += cyl_z(boss_r, z_mid_bot, back_boss_top)
back -= cyl_z(back_bore_r, -big, back_bore_top)
back -= cone_z(back_bore_r + 0.3, back_bore_r, z_back_bot - 0.1, z_back_bot + 0.2)
back -= cone_z(back_bore2_r + 0.25, back_bore2_r, back_bore_top - 0.05, back_bore_top + 0.2)
back -= cyl_z(back_bore2_r, back_bore_top - 0.1, back_bore2_top)
back -= cone_z(back_pin_r + 0.25, back_pin_r, back_bore2_top - 0.05, back_bore2_top + 0.2)
back -= cyl_z(back_pin_r, back_bore2_top - 0.1, back_pin_top)
back -= ring_z(ring_r0, ring_r1, -big, z_back_bot + ring_d)
back -= box(-led_w / 2, led_w / 2, led_y, big, -big, led_step_z)
back -= box(-led_w / 2, led_w / 2, led_y, led_step_y, -big, big)

# ---- horn ----------------------------------------------------------------
horn = cone_z(horn_r - horn_c, horn_r, horn_z0, horn_z0 + horn_c)
horn += cyl_z(horn_r, horn_z0 + horn_c, horn_z1 - horn_c)
horn += cone_z(horn_r, horn_r - horn_c, horn_z1 - horn_c, horn_z1)
horn += cone_z(hub_r0, hub_r1, hub_z0, horn_z0)
horn = fillet(edges_at(horn, hub_z0, hub_r0) + edges_at(horn, horn_z0, hub_r1), hub_fillet)
horn -= cyl_z(hub_bore_r, -big, hub_bore_top)
horn -= cone_z(hub_bore_r + hub_bore_c + 0.1, hub_bore_r, hub_z0 - 0.1, hub_z0 + hub_bore_c)
horn -= cyl_z(horn_bore_r, -big, big)
horn -= box(-horn_key_w / 2, horn_key_w / 2, 0, horn_key_y, -big, horn_recess_floor + 0.1)
horn -= cyl_z(horn_recess_r, horn_recess_floor, big)
horn -= cone_z(horn_recess_r, horn_recess_r + big, horn_z1 - horn_c, horn_z1 - horn_c + big)
for loc in PolarLocations(horn_hole_bc, 4):
    horn -= loc * cyl_z(horn_hole_r, -big, big)
horn -= box(-horn_mark_w / 2, horn_mark_w / 2, horn_r - horn_mark_d, big, -big, big)

# ---- idler horn (back) ---------------------------------------------------
idler = cone_z(horn_r - horn_c, horn_r, idler_z0, idler_z0 + horn_c)
idler += cyl_z(horn_r, idler_z0 + horn_c, idler_z1 - horn_c)
idler += cone_z(horn_r, horn_r - horn_c, idler_z1 - horn_c, idler_z1)
idler += cyl_z(idler_stem_r, idler_z1, idler_stem_top)
idler = fillet(edges_at(idler, idler_z1, idler_stem_r), idler_fillet)
idler -= cyl_z(idler_bore_r, -big, big)
idler -= cone_z(idler_bore_r + 0.3, idler_bore_r, idler_cbore_top - 0.1, idler_cbore_top + 0.2)
idler -= cyl_z(idler_cbore_r, -big, idler_cbore_top)
idler -= cone_z(idler_cbore_r + 0.3, idler_cbore_r, idler_z0 - 0.1, idler_z0 + 0.2)
for loc in PolarLocations(horn_hole_bc, 4):
    idler -= loc * cyl_z(horn_hole_r, -big, big)

# ---- idler cap -----------------------------------------------------------
idle_cap = cyl_z(icap_r, icap_z0, icap_z1) + cyl_z(icap_stem_r, icap_z1, icap_top)
idle_cap = fillet(edges_at(idle_cap, icap_z1, icap_stem_r), icap_fillet)
idle_cap -= cyl_z(icap_pocket_r, -big, icap_pocket_top)
idle_cap -= cone_z(icap_hole_r + 0.3, icap_hole_r, icap_pocket_top - 0.1, icap_pocket_top + 0.2)
idle_cap -= cyl_z(icap_hole_r, -big, big)

show_object(mid, name="case_middle", color="dimgray")
show_object(front, name="case_front", color="dimgray")
show_object(back, name="case_back", color="dimgray")
show_object(horn, name="horn", color="lightgray")
show_object(idler, name="idler_horn", color="lightgray")
show_object(idle_cap, name="idler_cap", color="gray")

if include_led:
    # side profile (y, z): lower lip reaches the end face, upper part has a 10° draft
    y1, zl = yc + L / 2, led_step_z - 0.1
    pts = [(led_y, z_back_bot), (y1 - edge_c, z_back_bot), (y1, z_back_bot + edge_c),
           (y1, zl - edge_c), (y1 - edge_c, zl), (led_step_y, zl), (led_step_y, z_mid_bot),
           (led_y + 0.106, z_mid_bot), (led_y, z_mid_bot - 0.601)]
    led = Pos(-led_w / 2, 0, 0) * extrude(Plane.YZ * Polygon(*pts, align=None), led_w)
    show_object(led, name="led_cap", color="red")

if include_screws:
    show_object(Pos(0, 0, horn_screw_z) * bts_screw(), name="horn_screw", color="silver")
    show_object(Pos(0, 0, idler_screw_z) * Rot(180, 0, 0) * bts_screw(), name="idler_screw", color="silver")
    phs = phs_screw()
    for i, (x, y) in enumerate(screw_xy):
        show_object(Pos(x, y, screw_cbore_floor) * phs, name=f"case_screw_{i + 1}", color="silver")

if include_connectors:
    for sx in (-1, 1):
        def bx(x0, x1, y0, y1, z0, z1):
            return box(*sorted((sx * x0, sx * x1)), y0, y1, z0, z1)
        c = bx(conn_x0, conn_x1, conn_y0, conn_y1, conn_roof0, conn_roof1)
        c += bx(conn_x0, conn_x0 + conn_back, conn_y0, conn_y1, conn_bot, conn_roof0)
        for y0, y1, s in ((conn_y0, conn_y0 + conn_end, 1), (conn_y1 - conn_end, conn_y1, -1)):
            yy = y0 if s > 0 else y1
            c += bx(conn_x0, 7.9, y0, y1, conn_bot, conn_roof0)                 # end wall
            c += bx(7.202, 7.9, *sorted((yy, yy + s * 1.05)), -15.4, conn_roof0)  # shoulder
            c += bx(8.6, conn_x1, *sorted((yy, yy + s * 1.05)), -14.6, conn_roof0)  # ear
            c += bx(8.302, conn_x1, *sorted((yy, yy + s * 1.05)), -15.5, -14.6)
        for k in (-1, 0, 1):
            y = conn_pin_y + k * conn_pitch
            c += bx(conn_pin_x - conn_pin / 2, conn_pin_x + conn_pin / 2,
                    y - conn_pin / 2, y + conn_pin / 2, conn_pin_z0, conn_pin_z1)
        show_object(c, name=f"connector_{'r' if sx > 0 else 'l'}", color="ivory")
