# Da Vinci SI manipulator — assembly of the per-part reconstructions.
#
# World frame = the frame of "Da vinci si manipulator.stl", so the result can
# be diffed directly with `lamad re compare "Da vinci si manipulator.stl"
# assembly.py`. Units mm.
#
# Each part script in components/ builds its part in its vendor STEP's frame.
# The placement table below maps vendor frame -> world as
#     p_world = R @ p_local + t        (R row-major 3x3, t in mm)
# measured by registering each vendor part onto the STL (residual ~0.11 mm).
#
# A part whose script is missing or fails can be drawn as a placeholder (see
# `placeholder`; off by default), in its vendor frame and placed with the same transform, so
# dropping the real script into components/ needs no change here.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

import sys
from pathlib import Path

import build123d as b3d

# ---- knobs ---------------------------------------------------------------
placeholder = "none"       # missing/broken scripts: "none" (skip), "box" (vendor bbox), "step" (vendor STEP)
include_hardware = False   # rail + carriages (no source file; plain boxes)
include_electronics = False  # left-side electronics (OpenRB-150 etc.; plain boxes)
include_bayonet = False    # bayonet casing is not in the reference STL
only = "all"               # show only nodes whose path starts with this (e.g. "motor_1")

# ---- rotations (row-major) -----------------------------------------------
I3 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
R_MOTOR_A = ((-1, 0, 0), (0, 0, 1), (0, 1, 0))   # motors 1, 2
R_MOTOR_B = ((1, 0, 0), (0, 0, 1), (0, -1, 0))   # motors 3, 4
R_COUPLING = ((1, 0, 0), (0, 0, -1), (0, 1, 0))
R_FLIP_Y = ((-1, 0, 0), (0, 1, 0), (0, 0, -1))   # 180 deg about Y

# ---- vendor fallbacks: script -> (vendor STEP or None, vendor bbox) -------
# bbox = ((xmin, xmax), (ymin, ymax), (zmin, zmax)) in the vendor frame.
VENDOR = {
    "dynamixel_330.py": (None, ((-10, 10), (-24.5, 9.5), (-22.5, 6.5))),
    "dynamixel_spring.py": ("Dynamixel Spring (15.5mm)(M) (prt 4).step",
                            ((-14, 14), (-0.1, 21.4), (-14, 14))),
    "coupling_interface.py": ("Coupling Interface (3.15)(M) (prt 4).step",
                              ((-14.04, 13.96), (16.05, 44.05), (-7.41, 3.09))),
    "grippers.py": ("Grippers.step", ((-12.15, 43.85), (-7.2, 27.1), (-41.15, 87.85))),
    "gripper.py": ("Gripper 1.step", ((-12.15, 43.85), (-7.2, 27.1), (27.85, 87.85))),
    "main_body.py": ("Main body.step", ((-50, 50), (-9.09, 5), (-65, 65))),
    "right_side.py": ("Right side.step", ((33.75, 50), (-25.4, 58.52), (-48.14, 56.33))),
    "left_side.py": ("Left side (microcont).step",
                               ((-62.5, -33.43), (-25.4, 58.52), (-48.14, 56.33))),
    "slot_holder.py": (None, ((-47.34, 47.66), (58.02, 73.02), (-60.78, 44.02))),
    "tool_slot_selection.py": (None, ((-39.84, 40.16), (60.02, 80.02), (-56.58, 43.75))),
    "bayonet_casing.py": ("Bayonet casing v10.step", None),
}

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
    ("grippers", "grippers.py", I3, (-15.85, 20.5, -23.35)),
    ("main_body", "main_body.py", I3, (0, 0, 0)),
    ("right_side", "right_side.py", I3, (0, 0, 0)),
    ("left_side", "left_side.py", I3, (0, 0, 0)),
    ("slot_holder", "slot_holder.py", I3, (0, 0, 0)),
    ("tool_slot_selection", "tool_slot_selection.py", I3, (0, 0, 0)),
    ("bayonet", "bayonet_casing.py", I3, (0, 0, 0)),   # placement unknown
]

# gripper.py (one fused gripper, placed twice) preferred over grippers.py.
GRIPPER_SINGLE = [
    ("gripper_a", "gripper.py", I3, (-15.846, 20.508, -23.357)),
    ("gripper_b", "gripper.py", R_FLIP_Y, (15.846, 20.5, 23.351)),
]

# ---- scene tree: parts that mount on a motor nest under it ---------------
# show_object names use "/" for nesting (lamad web scene tree), e.g.
# motor_1/coupling_1. A script with a single part is shown as the instance itself.
PARENT = {f"{kind}_{n}": f"motor_{n}" for kind in ("spring", "coupling") for n in range(1, 5)}

# ---- hardware with no source file (world frame boxes) --------------------
HARDWARE = [
    ("rail", ((-8.5, 8.5), (2.5, 13.3), (-65, 65))),
    ("carriage_1", ((-16, 16), (5.3, 18.5), (-46.5, -4.5))),
    ("carriage_2", ((-16, 16), (5.3, 18.5), (4.5, 46.5))),
    ("carriage_block_1", ((-10.2, -4.2), (7, 15), (-46, -5))),
    ("carriage_block_2", ((4.2, 10.2), (7, 15), (-46, -5))),
    ("carriage_block_3", ((-10.2, -4.2), (7, 15), (5, 46))),
    ("carriage_block_4", ((4.2, 10.2), (7, 15), (5, 46))),
]

# ---- left-side electronics, no source file (world frame boxes) ----------
ELECTRONICS = [
    ("pcb", ((-62.59, -60.99), (-22.72, 2.28), (-28.91, 37.09))),
    ("header_a", ((-71.15, -62.64), (-1.2, 1.21), (-3.53, 32.03))),
    ("header_b", ((-71.15, -62.64), (-21.57, -19.15), (-3.55, 32.01))),
    ("joystick", ((-70.92, -58.59), (-13.68, -6.11), (30.43, 37.98))),
    ("elec_1", ((-66.84, -59.44), (-22.93, -14.73), (-14.67, -4.67))),
    ("elec_2", ((-66.84, -59.44), (-5.73, 2.47), (-14.66, -4.66))),
    ("elec_3", ((-68.64, -59.44), (-10.13, -6.33), (-14.67, -4.67))),
    ("elec_4", ((-68.64, -59.44), (-14.24, -10.44), (-14.67, -4.67))),
    ("switch", ((-65.8, -61.6), (-14.68, -5.73), (-28.81, -21.51))),
    ("elec_5", ((-71.18, -59.64), (-17.15, -9.53), (22.61, 25.15))),
    ("elec_6", ((-63.74, -62.64), (-12.63, -5.63), (9.15, 16.15))),
]

# ---- helpers -------------------------------------------------------------
COMPONENTS = Path(__file__).resolve().parent / "components"
_cache = {}


def load_part(path):
    """Exec a part script in its own namespace; return [(name, shape)]. Cached."""
    path = Path(path)
    if path in _cache:
        return _cache[path]   # None = script failed earlier
    parts = []

    def capture(obj, name=None, color=None, **_):
        if isinstance(obj, b3d.ShapeList):
            obj = obj[0] if len(obj) == 1 else b3d.Compound(children=list(obj))
        parts.append((name or f"part{len(parts) + 1}", obj, color))

    g = {k: getattr(b3d, k) for k in getattr(b3d, "__all__", dir(b3d)) if not k.startswith("_")}
    g.update(__name__="__part__", __file__=str(path), show_object=capture)
    exec(compile(path.read_text(), str(path), "exec"), g)
    _cache[path] = parts
    return parts


def location(R, t):
    """Location for p_world = R @ p_local + t (R row-major, proper rotation)."""
    x_dir = (R[0][0], R[1][0], R[2][0])
    z_dir = (R[0][2], R[1][2], R[2][2])
    return b3d.Location(b3d.Plane(origin=t, x_dir=x_dir, z_dir=z_dir))


def bbox_box(bb):
    (x0, x1), (y0, y1), (z0, z1) = bb
    return b3d.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b3d.Box(x1 - x0, y1 - y0, z1 - z0)


def placeholder_shape(script):
    step, bb = VENDOR.get(script, (None, None))
    if placeholder == "step" and step and (COMPONENTS / step).exists():
        return b3d.Compound(children=list(b3d.import_step(COMPONENTS / step).solids()))
    if placeholder in ("box", "step") and bb:
        return bbox_box(bb)
    return None


# ---- build ---------------------------------------------------------------
placements = list(PLACEMENTS)
if (COMPONENTS / "gripper.py").exists():
    i = next(k for k, p in enumerate(placements) if p[0] == "grippers")
    placements[i:i + 1] = GRIPPER_SINGLE

status = []
for inst, script, R, t in placements:
    node = f"{PARENT[inst]}/{inst}" if inst in PARENT else inst
    if only != "all" and not node.startswith(only):
        continue
    if inst == "bayonet" and not include_bayonet:
        continue
    loc = location(R, t)
    why = "missing"
    if (COMPONENTS / script).exists():
        try:
            parts = load_part(COMPONENTS / script)
        except Exception as e:  # a broken part script falls back to its placeholder
            _cache[COMPONENTS / script] = None
            parts, why = None, f"error: {type(e).__name__}: {e}"
        if parts:
            for pname, shape, color in parts:
                name = node if len(parts) == 1 else f"{node}/{pname}"
                show_object(loc * shape, name=name, color=color)
            status.append(f"  {inst:20s} script   {script}")
            continue
        if parts is None and why == "missing":
            why = "error (see above)"
    shape = placeholder_shape(script)
    if shape is None:
        status.append(f"  {inst:20s} skipped  ({script} {why})")
        continue
    show_object(loc * shape, name=node, color="gray")
    status.append(f"  {inst:20s} {placeholder:8s} ({script} {why})")

for enabled, group, kind in ((include_hardware, HARDWARE, "hardware"),
                              (include_electronics, ELECTRONICS, "electronics")):
    for inst, bb in group if enabled else ():
        node = f"{kind}/{inst}"
        if only == "all" or node.startswith(only):
            show_object(bbox_box(bb), name=node, color="lightgray")
            status.append(f"  {inst:20s} {kind} box")

print("assembly.py:\n" + "\n".join(status), file=sys.stderr)
