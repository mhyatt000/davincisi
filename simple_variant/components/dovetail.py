# Dovetail profile shared by the dovetail mount (slot) and its mating rail.
#
# Imported by other part scripts (`from dovetail import dovetail_sketch`);
# run on its own it shows the profile. Units mm.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

import math

import build123d as b3d

# ---- knobs ---------------------------------------------------------------
dovetail_bottom = 30.0   # wide base of the trapezoid
dovetail_top = 10.0      # narrow top
dovetail_height = 10.0   # 45 deg flanks when (bottom - top) / 2 == height
dovetail_clearance = 0.1 # flanks pushed out this far, normal to the flank


def dovetail_sketch(bottom=dovetail_bottom, top=dovetail_top, height=dovetail_height,
                    clearance=dovetail_clearance):
    """Isosceles trapezoid in XY, base centred on the origin along X, top at +Y.

    The two angled flanks are offset outward by `clearance` (measured normal
    to the flank); the top and bottom edges stay at y = 0 and y = height.
    Moving a flank at angle a by c along its normal widens the trapezoid by
    c / sin(a) per side at every height, so the angle is unchanged.
    Pass clearance=0 for the nominal (rail) profile.
    """
    angle = math.atan2(height, (bottom - top) / 2)
    widen = 2 * clearance / math.sin(angle)
    with b3d.BuildSketch() as sk:
        b3d.Trapezoid(bottom + widen, height, math.degrees(angle),
                      align=(b3d.Align.CENTER, b3d.Align.MIN))
    return sk.sketch


if "show_object" in globals():
    show_object(dovetail_sketch(), name="dovetail")
