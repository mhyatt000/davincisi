# Motor tower — the four Dynamixel XL330s with their springs and couplings,
# and the tower (the two gripper jaws fused on one back plate, tower.py).
#
# Motors, springs and couplings are a straight copy of how ../../assembly.py
# places them: the part
# scripts are loaded from the original project's components/ and placed with
# the same (R, t) table, in the same world frame (that of
# "Da vinci si manipulator.stl"). Springs and couplings nest under their
# motor in the scene tree (motor_1/spring_1, motor_1/coupling_1, ...).
# tower.py replaces the original gripper_a / gripper_b and is already built in
# this world frame.
#     p_world = R @ p_local + t        (R row-major 3x3, t in mm)
# Units mm.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from partlib import HERE, I3, ORIGINAL, show_placed  # noqa: E402

# ---- knobs ---------------------------------------------------------------
include_springs = True
include_couplings = True
include_tower = True

# ---- rotations (row-major) -----------------------------------------------
R_MOTOR_A = ((-1, 0, 0), (0, 0, 1), (0, 1, 0))   # motors 1, 2
R_MOTOR_B = ((1, 0, 0), (0, 0, 1), (0, -1, 0))   # motors 3, 4
R_COUPLING = ((1, 0, 0), (0, 0, -1), (0, 1, 0))

# ---- placement table: (instance, script, R, t) ---------------------------
PLACEMENTS = [
    ("motor_1", "dynamixel_330.py", R_MOTOR_A, (-16, 42.1, -16)),
    ("motor_2", "dynamixel_330.py", R_MOTOR_A, (16, 42.1, -16)),
    ("motor_3", "dynamixel_330.py", R_MOTOR_B, (-16, 42.1, 16)),
    ("motor_4", "dynamixel_330.py", R_MOTOR_B, (16, 42.1, 16)),
    ("spring_1", "dynamixel_spring.py", I3, (-16, 45.6, -16)),
    ("spring_2", "dynamixel_spring.py", I3, (16, 45.7, -16)),
    ("spring_3", "dynamixel_spring.py", I3, (-16, 45.6, 16)),
    ("spring_4", "dynamixel_spring.py", I3, (16, 45.6, 16)),
    ("coupling_1", "coupling_interface.py", R_COUPLING, (-15.746, 66.096, -46.013)),
    ("coupling_2", "coupling_interface.py", R_COUPLING, (15.96, 65.001, -45.887)),
    ("coupling_3", "coupling_interface.py", R_COUPLING, (-16.028, 66.089, -14.243)),
    ("coupling_4", "coupling_interface.py", R_COUPLING, (15.887, 66.087, -14.24)),
    ("tower", HERE / "tower.py", I3, (0, 0, 0)),
]

# ---- scene tree: parts that mount on a motor nest under it ---------------
PARENT = {f"{kind}_{n}": f"motor_{n}" for kind in ("spring", "coupling") for n in range(1, 5)}

# ---- build ---------------------------------------------------------------
for inst, script, R, t in PLACEMENTS:
    if inst.startswith("spring") and not include_springs:
        continue
    if inst.startswith("coupling") and not include_couplings:
        continue
    if inst == "tower" and not include_tower:
        continue
    node = f"{PARENT[inst]}/{inst}" if inst in PARENT else inst
    show_placed(show_object, node, ORIGINAL / script, R, t)
