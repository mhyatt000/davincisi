# Da Vinci SI manipulator — simplified variant, deviating from ../assembly.py.
#
# Composition only: each part lives in its own script in components/ and is
# built in its own local frame. The placement table below maps local -> world
# as
#     p_world = R @ p_local + t        (R row-major 3x3, t in mm)
# World frame = the dovetail mount's: axis +Z, disc bottom at z = 0, slot
# running along Y. Units mm.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

import sys
from pathlib import Path

COMPONENTS = Path(__file__).resolve().parent / "components"
sys.path.insert(0, str(COMPONENTS))
from partlib import I3, show_placed  # noqa: E402

# ---- knobs ---------------------------------------------------------------
only = "all"   # show only nodes whose path starts with this (e.g. "mount")

# ---- dovetail fit --------------------------------------------------------
# The motor tower (tower.py, in the original assembly's frame) has its
# dovetail pin along its Z, pointing toward its -Y, centred on x = 0, z = 0.
# The mount's slot runs along Y and opens toward +Z. R_TOWER takes tower X ->
# X, tower Y -> Z (pin points down into the slot) and tower Z -> -Y (pin along
# the slot). The pin's wide face sits on the slot floor, which puts the rib on
# the mount's top face; pin and slot are both centred on x = 0, y = 0.
MOUNT_TOP = 5.0 + 7.35 * 1.00056     # dovetail_mount.py: disc_h + boss_h
DOVETAIL_HEIGHT = 10.0               # dovetail.py: dovetail_height (= slot depth)
PIN_TIP_Y = 18.508 - 4.0 - 10.0      # tower.py: baseplate_y0 - rib_d - dovetail_height
R_TOWER = ((1, 0, 0), (0, 0, -1), (0, 1, 0))
T_TOWER = (0, 0, MOUNT_TOP - DOVETAIL_HEIGHT - PIN_TIP_Y)
# tool_holder.py (copied from the original project's tool_slot_selection.py)
# and tool.py (placeholder for the tool in it) are still in the original
# assembly's frame (the motor tower's frame), so they take the same transform
# as the motor tower.

# ---- placements: (instance, script, R, t) --------------------------------
PLACEMENTS = [
    ("mount", "dovetail_mount.py", I3, (0, 0, 0)),
    ("motor_tower", "motor_tower.py", R_TOWER, T_TOWER),
    ("tool_holder", "tool_holder.py", R_TOWER, T_TOWER),
    ("tool", "tool.py", R_TOWER, T_TOWER),
]

# ---- build ---------------------------------------------------------------
status = []
for inst, script, R, t in PLACEMENTS:
    if only != "all" and not inst.startswith(only):
        continue
    show_placed(show_object, inst, COMPONENTS / script, R, t)
    status.append(f"  {inst:20s} {script}")

print("assembly.py:\n" + "\n".join(status), file=sys.stderr)
