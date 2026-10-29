# Da Vinci SI manipulator — full assembly: assembly.py plus the BOM parts
# that are not in "Da vinci si manipulator.stl".
#
# assembly.py stays the STL-matched assembly (diff it with `lamad re compare`).
# This script runs it unchanged and adds:
#
#   * bayonet: components/bayonet_casing.py (the xArm mount). It locks onto the
#     main body's bayonet hub, whose axis is world -Y through the origin. Placement
#     follows from the two parts' geometry, not from the STL:
#       - axial: the main body's lobed disc (y -5.13 .. -9.0946, 3.965 thick)
#         rests on the mount disc's top face, under the ring's lugs (4.052
#         clearance); the main body's hub then sits in the ring's mouth
#         counterbore. So the mount disc top is at y = -9.0946.
#       - clocking: the angular gaps between the ring's lug teeth (124.2 / 119.0
#         / 116.8 deg) match the gaps between the hub's lobes (124.3 / 119.0 /
#         116.7) at a single rotation, ~181.7 deg, where every lobe sits under
#         a lug and butts against its tooth (the locked position).
#
# Compression springs (BOM: 4x OD 9, free length 5, wire 0.8) are not placed:
# no part has a seat for them (see the note at the bottom).
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

import ast
import sys
from pathlib import Path

import build123d as b3d

# ---- forwarded to assembly.py --------------------------------------------
placeholder = "none"
include_hardware = False
include_electronics = False
only = "all"

# ---- bayonet mount -------------------------------------------------------
include_bayonet = True
bayonet_clock = 181.7      # deg about +Y, vendor lug angles -> locked on the hub lobes
bayonet_y = 48.893740      # vendor -> world Y shift: mount disc top (-57.988375) to -9.094635
bayonet_axis_x = 13.2556572   # ring axis in the vendor frame (bayonet_casing.py)
bayonet_axis_z = 92.0822317

# ========================================================================
ROOT = Path(__file__).resolve().parent


def run_script(path, params, show):
    """Exec a lamad-style script with its top-level literals overridden."""
    tree = ast.parse(path.read_text())
    for n in tree.body:
        if (isinstance(n, ast.Assign) and len(n.targets) == 1
                and isinstance(n.targets[0], ast.Name) and n.targets[0].id in params):
            n.value = ast.Constant(value=params[n.targets[0].id])
    ast.fix_missing_locations(tree)
    g = {k: getattr(b3d, k) for k in getattr(b3d, "__all__", dir(b3d)) if not k.startswith("_")}
    g.update(__name__="__part__", __file__=str(path), show_object=show)
    exec(compile(tree, str(path), "exec"), g)


# ---- the STL-matched assembly, unchanged ---------------------------------
run_script(ROOT / "assembly.py",
           dict(placeholder=placeholder, include_hardware=include_hardware,
                include_electronics=include_electronics, only=only,
                include_bayonet=False),   # its bayonet entry sits at identity
           show_object)

# ---- bayonet mount -------------------------------------------------------
if include_bayonet and (only == "all" or "bayonet".startswith(only)):
    loc = (b3d.Pos(0, bayonet_y, 0) * b3d.Rot(0, -bayonet_clock, 0)
           * b3d.Pos(-bayonet_axis_x, 0, -bayonet_axis_z))

    def place(obj, name=None, color=None, **_):
        show_object(loc * obj, name=f"bayonet/{name}", color=color)

    run_script(ROOT / "components" / "bayonet_casing.py", {}, place)
    print("assembly_full.py: + bayonet (bayonet_casing.py), locked on the main body hub",
          file=sys.stderr)

# Compression springs, BOM 4x OD 9 / ID 7.4, free length 5: not placed. No part
# in this CAD revision has a seat for them (the spring hub tube is 10 mm OD, the
# coupling bore 8 mm with an 11 mm hub ring, the gripper motor pins 2 mm), and
# the four orthoplanar "Dynamixel Spring" parts already give each coupling its
# axial preload, so they look like a leftover from an earlier revision.
