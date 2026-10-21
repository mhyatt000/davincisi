# tool_dovetail sketch — hand-drawn side profile (YZ plane, looking along X)
# of the simple-variant assembly: simplified outlines of the tool holder (and
# its two dovetail pins), the tower and the dovetail mount, plus construction
# lines from the tool holder's bars down to
# the dovetail pin. Back (open end of the U, top bar) is -Y, front (curved end
# of the U) is +Y.
#
# Construction lines, three named pairs (front / back each):
#   * bar_pin:     inner edge of the tool holder's front/back bar on its base
#                  -> front/back end of the tower's dovetail pin
#   * bar_window:  the same bar edges -> inner edge (the edge nearer the pin)
#                  of the front/back JST window opening on the top side of
#                  the tower's baseplate; defines the baseplate channel
#                  (tower.py)
#   * mount_outer: the mount's edge (radius disc_r, at the pin tip) -> the
#                  tool holder's OUTER front/back edge on its base; the tool
#                  holder's dovetail pins end along these and its 4 mm straps
#                  (pin -> holder) run along them (tool_holder.py)
#
# The outlines are drawn by hand (no small chamfers / windows), but the
# numbers they use are measured from the placed parts (assembly.py is run to
# get them) on the centre line x = 0, so the sketch follows the model.
# Units mm, assembly frame.
#
# Render: lamad render sketch simple_variant/sketches/tool_dovetail.py --out <png>

import re
import sys
from pathlib import Path

import build123d as b3d

ROOT = Path(__file__).resolve().parents[1]          # simple_variant/
sys.path.insert(0, str(ROOT / "components"))

# ---- knobs ---------------------------------------------------------------
probe = 0.01             # how far inside a face the edge probes look


def placed_parts():
    """Run assembly.py and return {name: placed shape}."""
    parts = {}

    def capture(obj, name=None, **_):
        parts[name] = obj

    g = {"__name__": "__part__", "__file__": str(ROOT / "assembly.py"), "show_object": capture}
    exec(compile((ROOT / "assembly.py").read_text(), str(ROOT / "assembly.py"), "exec"), g)
    return parts


def knob(script, name):
    """A top-level numeric knob from a part script (a literal or plain arithmetic)."""
    m = re.search(rf"^{name}\s*=\s*([-+*/(). \d]+)", (ROOT / "components" / script).read_text(), re.M)
    return float(eval(m.group(1), {"__builtins__": {}}))


def y_runs(shape, z, x=0.0):
    """Material intervals along Y on the line (x, z)."""
    line = shape & b3d.Pos(x, 0, z) * b3d.Box(1e-3, 1000, 1e-3)
    return sorted((s.bounding_box().min.Y, s.bounding_box().max.Y) for s in line.solids())


def P(y, z):
    return b3d.Vector(0, y, z)


def rect(y0, y1, z0, z1):
    return b3d.Polyline(P(y0, z0), P(y1, z0), P(y1, z1), P(y0, z1), close=True)


parts = placed_parts()
holder = parts["tool_holder"]                    # body + straps + dovetail pins, one solid
tower = parts["motor_tower/tower"]
mount = parts["mount"]

# ---- tool holder: outer block + the bars' inner edges ---------------------
hb = holder.bounding_box()
top_z = hb.max.Z
base_z = top_z - knob("tool_holder.py", "thick")    # the holder's base (straps and pins hang below)
runs = y_runs(holder, base_z + probe)
back_bar, front_bar = runs[0], runs[-1]          # back bar at -Y, front bar at +Y
back_edge, front_edge = P(back_bar[1], base_z), P(front_bar[0], base_z)
holder_lines = [
    rect(hb.min.Y, hb.max.Y, base_z, top_z),
    b3d.Line(back_edge, P(back_edge.Y, top_z)),      # back bar | window
    b3d.Line(front_edge, P(front_edge.Y, top_z)),    # window | front bar
]

# ---- tower: jaw block on the baseplate, rib + dovetail pin below ----------
tb = tower.bounding_box()
tip_z = tb.min.Z                                 # dovetail pin tip, in the mount's slot
(pin_y0, pin_y1), = y_runs(tower, tip_z + probe)
rib_z = tip_z + knob("dovetail.py", "dovetail_height")      # pin | rib
plate_z = rib_z + knob("tower.py", "rib_d")                 # rib | baseplate (outer face)
plate_top = plate_z + knob("tower.py", "base_t")            # 4 mm baseplate
# measure through a motor block: the centre line (x = 0) is in the baseplate channel
block_x = knob("tower.py", "block_gap") / 2 + knob("tower.py", "block_w") / 2
body = [r for r in y_runs(tower, plate_z + probe, block_x)]
body_y0, body_y1 = body[0][0], body[-1][1]
tower_lines = [
    rect(body_y0, body_y1, plate_z, tb.max.Z),                       # baseplate + jaws
    b3d.Line(P(body_y0, plate_top), P(body_y1, plate_top)),          # baseplate thickness
    rect(pin_y0, pin_y1, tip_z, plate_z),                            # rib + pin
    b3d.Line(P(pin_y0, rib_z), P(pin_y1, rib_z)),                    # pin | rib
]
pin_back, pin_front = P(pin_y0, tip_z), P(pin_y1, tip_z)


# ---- JST 3-pin plug windows through the baseplate --------------------------
# Seen from the side the 8 windows stack into two openings (one each side of
# the pin). Probe through one window at mid-baseplate for the straight walls,
# then add the 45 deg chamfer at the outer face.
win_x = knob("tower.py", "block_gap") / 2 + knob("tower.py", "window_w") / 2
cham = knob("tower.py", "jst_chamfer")
plate_runs = y_runs(tower, (plate_z + plate_top) / 2, win_x)
windows = [(a[1], b[0]) for a, b in zip(plate_runs, plate_runs[1:])]   # gaps in the baseplate
window_lines, window_corners = [], []
for wy0, wy1 in windows:
    corners = [P(wy0 - cham, plate_z), P(wy0, plate_z + cham), P(wy0, plate_top),
               P(wy1, plate_top), P(wy1, plate_z + cham), P(wy1 + cham, plate_z)]
    window_lines.append(b3d.Polyline(*corners))
    window_corners.append(corners)

# ---- mount: disc + boss, and the slot floor the pin tip sits on -----------
mb = mount.bounding_box()
disc_top = mb.min.Z + knob("dovetail_mount.py", "disc_h")
# the boss is round about the mount axis, so seen from the side it spans its
# full radius (the screw-head clearance cuts are on X, out of this view)
boss_r = knob("dovetail_mount.py", "boss_r")
boss_y0, boss_y1 = -boss_r, boss_r
mount_lines = [
    rect(mb.min.Y, mb.max.Y, mb.min.Z, disc_top),                    # disc
    rect(boss_y0, boss_y1, disc_top, mb.max.Z),                      # boss
    b3d.Line(P(mb.min.Y, tip_z), P(mb.max.Y, tip_z)),                # slot floor (hidden)
]

# ---- construction lines --------------------------------------------------
bar_pin_front = b3d.Line(front_edge, pin_front)
bar_pin_back = b3d.Line(back_edge, pin_back)
(back_win, front_win) = sorted(windows)               # back opening at -Y, front at +Y
mount_r = knob("dovetail_mount.py", "disc_r")
mount_outer_front = b3d.Line(P(mount_r, tip_z), P(hb.max.Y, base_z))
mount_outer_back = b3d.Line(P(-mount_r, tip_z), P(hb.min.Y, base_z))



def y_on(line, z):
    a, b = line @ 0, line @ 1
    return a.Y + (b.Y - a.Y) * (z - a.Z) / (b.Z - a.Z)


# tool holder's dovetail pins: from the tower's pin ends out to mount_outer
holder_pin_lines = []
for out_line, inner_y in ((mount_outer_back, pin_y0), (mount_outer_front, pin_y1)):
    holder_pin_lines.append(b3d.Polyline(P(inner_y, tip_z), P(y_on(out_line, tip_z), tip_z),
                                         P(y_on(out_line, rib_z), rib_z), P(inner_y, rib_z),
                                         close=True))
# tool holder's straps: mount_outer and a parallel line strap_t inside it,
# from the dovetail's top face (rib_z) up to the holder's base
strap_t = knob("tool_holder.py", "strap_t")
strap_lines = []
for out_line in (mount_outer_back, mount_outer_front):
    a, b = out_line @ 0, out_line @ 1
    d = (b - a).normalized()
    n = b3d.Vector(0, -d.Z, d.Y)                     # normal to the line in the YZ plane
    if n.Y * a.Y > 0:                                # make it point inward, toward y = 0
        n = -n
    ia, ib = a + n * strap_t, b + n * strap_t
    inner = b3d.Line(ia, ib)
    strap_lines.append(b3d.Polyline(P(y_on(out_line, rib_z), rib_z), b,
                                    P(y_on(inner, base_z), base_z),
                                    P(y_on(inner, rib_z), rib_z), close=True))
bar_window_front = b3d.Line(front_edge, P(front_win[0], plate_top))
bar_window_back = b3d.Line(back_edge, P(back_win[1], plate_top))

print(f"tool holder: y {hb.min.Y:.3f}..{hb.max.Y:.3f}, z {base_z:.3f}..{top_z:.3f}; "
      f"bar inner edges y {back_edge.Y:.3f} (back), {front_edge.Y:.3f} (front)", file=sys.stderr)
print(f"tower: body y {body_y0:.3f}..{body_y1:.3f}, z {plate_z:.3f}..{tb.max.Z:.3f}; "
      f"pin y {pin_y0:.3f}..{pin_y1:.3f}, tip z {tip_z:.3f}, rib z {rib_z:.3f}", file=sys.stderr)
for (wy0, wy1), corners in zip(windows, window_corners):
    print(f"JST window y {wy0:.3f}..{wy1:.3f}, corners (y, z): "
          + ", ".join(f"({c.Y:.3f}, {c.Z:.3f})" for c in corners), file=sys.stderr)
print(f"mount: disc y {mb.min.Y:.3f}..{mb.max.Y:.3f}, z {mb.min.Z:.3f}..{disc_top:.3f}; "
      f"boss y {boss_y0:.3f}..{boss_y1:.3f}, top z {mb.max.Z:.3f}; slot floor z {tip_z:.3f}", file=sys.stderr)
for nm, ln in (("bar_pin front", bar_pin_front), ("bar_pin back", bar_pin_back),
               ("bar_window front", bar_window_front), ("bar_window back", bar_window_back),
               ("mount_outer front", mount_outer_front), ("mount_outer back", mount_outer_back)):
    d = ln @ 1 - ln @ 0
    print(f"{nm} line: length {ln.length:.3f}, dY {d.Y:.3f}, dZ {d.Z:.3f}", file=sys.stderr)

if "show_object" in globals():
    show_object(b3d.Compound(children=holder_lines), name="tool_holder", color="teal")
    show_object(b3d.Compound(children=holder_pin_lines), name="tool_holder/dovetail_pins", color="peru")
    show_object(b3d.Compound(children=strap_lines), name="tool_holder/straps", color="peru")
    show_object(b3d.Compound(children=tower_lines), name="tower", color="steelblue")
    show_object(b3d.Compound(children=window_lines), name="tower/jst_windows", color="crimson")
    show_object(b3d.Compound(children=mount_lines), name="mount", color="dimgray")
    for nm, ln in (("bar_pin_front", bar_pin_front), ("bar_pin_back", bar_pin_back),
                   ("bar_window_front", bar_window_front), ("bar_window_back", bar_window_back),
                   ("mount_outer_front", mount_outer_front), ("mount_outer_back", mount_outer_back)):
        show_object(ln, name=f"construction/{nm}", color="orange")
