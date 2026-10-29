# Capstan — lower cap (lower_cap.py, the flange on the horn), spring shaft
# (dynamixel_spring.py: shaft + discs) and the upper cap that meshes with the
# tool (coupling_interface.py), as one unit.
#
# Frame = the spring's own: axis +Y through the origin, lower cap underside
# at y = 2.9 (sits on the XL330 horn), top disc at the +Y end.
#     p_capstan = R @ p_local + t      (R row-major 3x3, t in mm)
# Units mm.
#
# The upper cap is seated, not copied: the original assembly's placement
# (motor_1) left it 0.22 mm off axis, 0.03 deg off the notches and 1 mm low,
# overlapping the top disc by ~154 mm3. Here its axis is put on the spring
# axis, it is turned about that axis so its lugs sit on the disc's notch
# directions, and its flange face rests on the disc top so the 2 mm lugs sit
# inside the 3 mm notches.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

import sys
from pathlib import Path

COMPONENTS = Path(__file__).resolve().parent / "components"
sys.path.insert(0, str(COMPONENTS))
import math  # noqa: E402

from partlib import I3, show_placed  # noqa: E402

# ---- knobs ---------------------------------------------------------------
include_upper_cap = True

# ---- upper cap seating -----------------------------------------------------
# coupling_interface.py (vendor frame): axis +Z through (CAP_AXIS_X, CAP_AXIS_Y),
# flange face at z CAP_FLANGE_Z, first lug at CAP_LUG_DEG (vendor XY degrees).
CAP_AXIS_X = -0.0390318
CAP_AXIS_Y = 30.0490949
CAP_FLANGE_Z = -7.40551 + 4.5 + 1.0 + 3.0     # bottom + body_h + cone_h + flange_h
CAP_LUG_DEG = 86.5
# dynamixel_spring.py: top disc top face and notch directions
DISC_TOP_Y = 17.4 + 3.0                       # tube_y1 + disc_t
NOTCH_DEG = 26.47 + 180 - 120                 # pattern_rot + 180 + k*120, k = -1 (86.47)

# cap Z -> -Y (lugs point down at the disc), cap X -> X, cap Y -> Z ...
R_FLIP = ((1, 0, 0), (0, 0, -1), (0, 1, 0))
# ... then turn about Y so the lug lands on the notch (angle = atan2(z, x))
d = math.radians(NOTCH_DEG - CAP_LUG_DEG)
R_TURN = ((math.cos(d), 0, -math.sin(d)), (0, 1, 0), (math.sin(d), 0, math.cos(d)))
R_CAP = tuple(tuple(sum(R_TURN[i][k] * R_FLIP[k][j] for k in range(3)) for j in range(3))
              for i in range(3))
# axis point at the flange face -> (0, DISC_TOP_Y, 0)
_p = (CAP_AXIS_X, CAP_AXIS_Y, CAP_FLANGE_Z)
_Rp = [sum(R_CAP[i][k] * _p[k] for k in range(3)) for i in range(3)]
T_CAP = (-_Rp[0], DISC_TOP_Y - _Rp[1], -_Rp[2])

PLACEMENTS = [
    ("lower_cap", "lower_cap.py", I3, (0, 0, 0)),
    ("spring", "dynamixel_spring.py", I3, (0, 0, 0)),
    ("upper_cap", "coupling_interface.py", R_CAP, T_CAP),
]

# ---- build ---------------------------------------------------------------
for inst, script, R, t in PLACEMENTS:
    if inst == "upper_cap" and not include_upper_cap:
        continue
    show_placed(show_object, inst, COMPONENTS / script, R, t)
