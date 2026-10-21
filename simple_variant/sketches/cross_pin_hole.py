# cross_pin_hole sketch — a d = 3 mm through hole across the tower's dovetail
# pin and the mount, orthogonal to the pin.
#
# The pin runs along Y (assembly frame). The hole runs along X through the
# centre of the pin: at the middle of the tower's pin along Y, and at the
# dovetail's mid-height in Z (the cross-section's centroid would be lower,
# leaving the hole grazing the boss's base). It passes through both walls
# of the mount's boss and through the tower's pin in the slot.
#
# Two views (render one at a time with --part):
#   * side    (YZ plane, x = 0): the hole circle, with the tower's pin and the
#             mount drawn by hand around it
#   * section (XZ plane, y = 0): the pin's dovetail, the mount's slot and boss,
#             and the hole's path across them
# Units mm, assembly frame. Numbers are measured from the placed parts.
#
# Render:
#   lamad render sketch simple_variant/sketches/cross_pin_hole.py --part side --out <png>
#   lamad render sketch simple_variant/sketches/cross_pin_hole.py --part section --out <png>

import re
import sys
from pathlib import Path

import build123d as b3d

ROOT = Path(__file__).resolve().parents[1]          # simple_variant/
sys.path.insert(0, str(ROOT / "components"))

# ---- knobs ---------------------------------------------------------------
hole_d = 3.0
probe = 0.01


def placed_parts():
    parts = {}
    g = {"__name__": "__part__", "__file__": str(ROOT / "assembly.py"),
         "show_object": lambda obj, name=None, **_: parts.__setitem__(name, obj)}
    exec(compile((ROOT / "assembly.py").read_text(), str(ROOT / "assembly.py"), "exec"), g)
    return parts


def knob(script, name):
    m = re.search(rf"^{name}\s*=\s*([-+*/(). \d]+)", (ROOT / "components" / script).read_text(), re.M)
    return float(eval(m.group(1), {"__builtins__": {}}))


parts = placed_parts()
tower, mount = parts["motor_tower/tower"], parts["mount"]

# ---- the pin: ends along Y, dovetail sizes -------------------------------
tip_z = tower.bounding_box().min.Z
line = tower & b3d.Pos(0, 0, tip_z + probe) * b3d.Box(1e-3, 1000, 1e-3)
(pin_y0, pin_y1), = [(s.bounding_box().min.Y, s.bounding_box().max.Y) for s in line.solids()]
wide = knob("dovetail.py", "dovetail_bottom")
narrow = knob("dovetail.py", "dovetail_top")
height = knob("dovetail.py", "dovetail_height")

# ---- hole centre ---------------------------------------------------------
hole_y = (pin_y0 + pin_y1) / 2
centroid = height * (wide + 2 * narrow) / (3 * (wide + narrow))   # above the wide face
hole_z = tip_z + height / 2

# ---- mount sizes -----------------------------------------------------------
mb = mount.bounding_box()
disc_top = mb.min.Z + knob("dovetail_mount.py", "disc_h")
boss_r = knob("dovetail_mount.py", "boss_r")
clear = knob("dovetail.py", "dovetail_clearance")
mount_top = mb.max.Z

print(f"tower pin: y {pin_y0:.3f}..{pin_y1:.3f}, tip z {tip_z:.3f}; dovetail {wide} / {narrow} x {height}",
      file=sys.stderr)
print(f"hole: d {hole_d}, axis along X at y = {hole_y:.3f}, z = {hole_z:.3f} "
      f"(mid-height; the centroid would be {tip_z + centroid:.3f})", file=sys.stderr)
print(f"hole length through the mount: x {-boss_r:.3f}..{boss_r:.3f}", file=sys.stderr)


def P(y, z):            # side view (YZ, x = 0)
    return b3d.Vector(0, y, z)


def Q(x, z):            # section view (XZ, y = hole_y)
    return b3d.Vector(x, hole_y, z)


# ---- side view ---------------------------------------------------------------
side_plane = b3d.Plane(origin=(0, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
hole_side = b3d.Pos(0, hole_y, hole_z) * (side_plane * b3d.Circle(hole_d / 2)).face()
side_context = [
    b3d.Polyline(P(pin_y0, tip_z), P(pin_y1, tip_z), P(pin_y1, tip_z + height),
                 P(pin_y0, tip_z + height), close=True),                       # tower pin
    b3d.Polyline(P(-boss_r, disc_top), P(boss_r, disc_top), P(boss_r, mount_top),
                 P(-boss_r, mount_top), close=True),                           # boss
    b3d.Polyline(P(mb.min.Y, mb.min.Z), P(mb.max.Y, mb.min.Z), P(mb.max.Y, disc_top),
                 P(mb.min.Y, disc_top), close=True),                           # disc
    b3d.Line(P(pin_y0 - 5, hole_z), P(pin_y1 + 5, hole_z)),                    # centre marks
    b3d.Line(P(hole_y, tip_z - 3), P(hole_y, tip_z + height + 3)),
]

# ---- section view ------------------------------------------------------------
dh = (wide - narrow) / 2
w = clear / (dh / (dh ** 2 + height ** 2) ** 0.5)                 # flank clearance, horizontal
section_context = [
    b3d.Polyline(Q(-wide / 2, tip_z), Q(wide / 2, tip_z), Q(narrow / 2, tip_z + height),
                 Q(-narrow / 2, tip_z + height), close=True),                  # pin (dovetail)
    b3d.Polyline(Q(-boss_r, disc_top), Q(-boss_r, mount_top), Q(-narrow / 2 - w, mount_top)),
    b3d.Polyline(Q(narrow / 2 + w, mount_top), Q(boss_r, mount_top), Q(boss_r, disc_top)),  # boss
    b3d.Polyline(Q(-narrow / 2 - w, mount_top), Q(-wide / 2 - w, tip_z),
                 Q(wide / 2 + w, tip_z), Q(narrow / 2 + w, mount_top)),        # slot (with clearance)
    b3d.Line(Q(mb.min.X, disc_top), Q(mb.max.X, disc_top)),                    # disc top
    b3d.Polyline(Q(-boss_r, hole_z - hole_d / 2), Q(boss_r, hole_z - hole_d / 2),
                 Q(boss_r, hole_z + hole_d / 2), Q(-boss_r, hole_z + hole_d / 2),
                 close=True),                                                  # hole path
]

if "show_object" in globals():
    show_object(hole_side, name="side/hole", color="crimson")
    show_object(b3d.Compound(children=side_context), name="side/context", color="steelblue")
    show_object(b3d.Compound(children=section_context), name="section/context", color="steelblue")
