# Tower — the two gripper jaws (gripper_a / gripper_b of ../../assembly.py)
# fused into one part on a single baseplate, with a dovetail pin on its
# outer face.
#
# Each jaw is ../../components/gripper.py, loaded with include_tab=False (the
# bent tabs at the plate ends are dropped). In the original
# assembly the two jaws sit back to back along Z with their 4 mm back plates
# (2 mm plate + 2 mm block front wall, the side with the 4 countersunk screw
# holes) in one plane and an ~9 mm gap between them. Here that gap is filled
# with a 4 mm plate section across the full plate width, so both jaws hang
# off one continuous baseplate. The screw holes in the baseplate and the pin holes
# in the block back walls are filled in; the four large circular cut-outs in
# the back walls stay (clearance for the capstans). The side walls that hold
# the motors are solid: their truss cut-outs and top V-notch are filled. The 8
# JST 3-pin plug windows get a 45 deg chamfer on the outer face of the baseplate.
#
# Names: "baseplate" is the 4 mm plate (the jaws' back plates + the bridge,
# the side with the JST windows); "dovetail pin" is the rib + dovetail on its
# outer face. Both are fused into the one tower solid.
#
# Baseplate channel: in the strip between the two motor columns (x =
# -block_gap/2 .. +block_gap/2, the slot along the dovetail pin's axis) the
# baseplate is cut away from each end of the tower in to a slanted line. The
# line is the tool_dovetail sketch's (../sketches/tool_dovetail.py) bar_window
# construction line: from the inner edge of the tool holder's front/back bar
# on its base, to the inner edge of the nearest JST window on the top of the
# baseplate, carried on through the baseplate. Only the baseplate is cut.
#
# End cuts: the tower is trimmed at both ends by slanted planes (running
# across the full width, X) that follow the tool holder's straps: each is the
# tool_dovetail mount_outer line (mount edge at the pin tip -> the tool
# holder's outer front/back edge on its base) moved end_cut_inset inward,
# which is the straps' thickness, so the cut faces meet the straps' inner
# faces. The tower
# keeps its centre; the offcuts beyond the planes are removed.
#
# World frame = the original assembly's (that of "Da vinci si manipulator.stl"),
# so this drops in where gripper_a / gripper_b were. The original placements
# are off by ~0.01 mm from a true mirror pair; here the jaws are exactly
# symmetric: centred on x = 0, mirrored about z = 0, outer baseplate face at
# y = baseplate_y0. Units mm.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

import sys
from pathlib import Path

import build123d as b3d

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dovetail import dovetail_height, dovetail_sketch  # noqa: E402
from partlib import ORIGINAL, load_part, location  # noqa: E402

# ---- knobs ---------------------------------------------------------------
base_gap = 8.99          # between the jaws' bottoms, filled by the bridge
base_t = 4.0             # bridge thickness (Y), matches plate + front wall
baseplate_y0 = 18.508    # outer face of the baseplate, world Y
jst_chamfer = 1.0        # 45 deg chamfer on the JST plug windows, outer baseplate face
# The two slots between the four motor pockets; True fills that slot solid
# from the baseplate to the back of the blocks.
fill_gap_x = False       # x = -4..4: between the left (motors 1, 3) and right (2, 4) columns
fill_gap_z = True        # z = -4.5..4.5: between the lower (1, 2) and upper (3, 4) jaws
# Dovetail pin on the outer baseplate face, running along Z (the unfilled
# slot's axis): a rib that thickens the baseplate, then the dovetail (nominal
# dovetail.py profile, narrow side on the rib) that slides into
# dovetail_mount.py's slot. It spans only the stretch between the two middle
# rows of JST windows (and their chamfers), so it never covers a window.
include_pin = True
rib_w = 10.0             # X, centred on x = 0
rib_d = 4.0              # Y, below the outer baseplate face (4 + rib_d thick here)
cross_pin_d = 3.0        # hole along X through the pin's middle, at its mid-height
                         # (matches dovetail_mount.py's cross-pin hole)
# Baseplate channel (see header). The tool holder's numbers are from the
# tool_dovetail sketch, in this file's frame: assembly +Y (the tool holder's
# front, its curved end) is -Z here, and assembly z = Y here - 2.153884.
include_channel = True
holder_base_y = 60.017   # tool holder base (its bottom face)
holder_front_z = 48.187  # front bar inner edge, at z = -holder_front_z
holder_back_z = 36.458   # back bar inner edge, at z = +holder_back_z
# End cuts (see header): mount_outer lines, in this file's frame.
include_end_cuts = True
end_cut_inset = 6.0      # in from mount_outer; = tool_holder.py strap_t (flush with the straps)
mount_r = 37.5           # dovetail_mount.py disc_r, at the pin tip
holder_outer_front_z = 56.579   # tool holder's outer front edge, at z = -this
holder_outer_back_z = 43.752    # tool holder's outer back edge, at z = +this

# ---- gripper.py vendor frame (see that file) -----------------------------
plate_cx = 15.851        # vendor X of the jaw centre line
plate_z0 = 27.8485       # vendor Z of the jaw bottom
plate_w = 56.0
plate_h = 38.0
plate_t = 2.0            # vendor plate spans y = -plate_t .. 0
front_t = 2.0            # block front wall, y = 0 .. front_t
csk_r = 2.75             # countersunk screw hole, radius at y = front_t
screw_dx = 12.5
screw_dzs = (7.0, 27.0)  # below the plate top
block_w = 24.0
block_gap = 8.0
block_d = 27.1
back_t = 2.0             # block back wall, y = block_d - back_t .. block_d
pin_r = 1.0
pin_dx = 8.0
pin_dz = 15.0            # +- from the block mid-height
wall_t = 1.0             # block side walls (the truss walls)
floor_t = 2.0
window_w = 6.015         # JST plug window at each side edge of each block, X
window_y1 = plate_t + 1  # plate windows cut through to y = 3 (into the side walls)
window_z0 = 15.22        # above the plate bottom
window_z1 = 25.75

R_UP = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
R_FLIP_Y = ((-1, 0, 0), (0, 1, 0), (0, 0, -1))   # 180 deg about Y


def cyl_y(r, y0, y1, x, z):
    """Cylinder along Y from y0 to y1 at (x, z)."""
    return b3d.Pos(x, (y0 + y1) / 2, z) * b3d.Rot(-90, 0, 0) * b3d.Cylinder(r, y1 - y0)


def hole_plugs():
    """Solids that exactly refill gripper.py's screw and pin holes (vendor frame).

    The 4 countersunk screw holes go through plate + front wall; the 16 pin
    holes go through the block back walls. The large circular capstan
    cut-outs in the back walls are left open.
    """
    plugs = []
    for sx in (-1, 1):
        for dz in screw_dzs:
            plugs.append(cyl_y(csk_r, -plate_t, front_t, plate_cx + sx * screw_dx,
                               plate_z0 + plate_h - dz))
    x0 = plate_cx - plate_w / 2
    for bx in (x0, x0 + block_w + block_gap):
        for sx in (-1, 1):
            for sz in (-1, 1):
                plugs.append(cyl_y(pin_r, block_d - back_t, block_d, bx + block_w / 2 + sx * pin_dx,
                                   plate_z0 + plate_h / 2 + sz * pin_dz))
    return b3d.Compound(children=plugs)


def wall_plugs():
    """Solids that refill the truss cut-outs (incl. the top V-notch) in all
    four side walls of each jaw, leaving the plate windows open (vendor frame)."""
    MIN = (b3d.Align.MIN,) * 3
    x0 = plate_cx - plate_w / 2
    y0, y1 = front_t, block_d - back_t
    plugs = []
    for bx in (x0, x0 + block_w + block_gap):
        for wx in (bx, bx + block_w - wall_t):
            wall = b3d.Pos(wx, y0, plate_z0 + floor_t) * b3d.Box(
                wall_t, y1 - y0, plate_h - floor_t, align=MIN)
            window = b3d.Pos(wx - 1, y0 - 1, plate_z0 + window_z0) * b3d.Box(
                wall_t + 2, window_y1 - y0 + 1, window_z1 - window_z0, align=MIN)
            plugs.append(wall - window)
    return b3d.Compound(children=plugs)


def window_chamfers():
    """45 deg cutters that chamfer the 8 JST plug windows on the outer
    baseplate face (world frame). Each is a frustum starting slightly outside the face so
    it does not share a plane with it; the outer windows are notches open to
    the baseplate edge, where the cutter just runs off the part."""
    e = 0.5
    c = jst_chamfer + e
    h = window_z1 - window_z0
    xs = []
    for bx in (-plate_w / 2, block_gap / 2):
        xs += [bx + window_w / 2, bx + block_w - window_w / 2]
    cutters = []
    for sz in (-1, 1):
        zc = sz * (base_gap / 2 + (window_z0 + window_z1) / 2)
        for xc in xs:
            pl = b3d.Plane(origin=(xc, baseplate_y0 - e, zc), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
            cutters.append(b3d.extrude(pl * b3d.Rectangle(window_w + 2 * c, h + 2 * c),
                                       amount=c, taper=45))
    return b3d.Compound(children=cutters)


def dovetail_pin():
    """Rib + dovetail on the outer baseplate face, centred on z = 0 and
    stopping at the chamfer of the nearest JST windows (world frame)."""
    length = 2 * (base_gap / 2 + window_z0 - jst_chamfer)
    rib_y0 = baseplate_y0 - rib_d
    rib = b3d.Pos(0, (rib_y0 + baseplate_y0) / 2, 0) * b3d.Box(rib_w, rib_d, length)
    # sketch +Y is world +Y: wide base at rib_y0 - dovetail_height, narrow
    # top on the rib face; extruded both ways along Z
    profile = b3d.Pos(0, rib_y0 - dovetail_height, 0) * dovetail_sketch(clearance=0)
    pin = rib + b3d.extrude(profile, amount=length / 2, both=True)
    # cross-pin hole along X through the dovetail, at its middle and mid-height
    hole_y = rib_y0 - dovetail_height / 2
    return pin - b3d.Pos(0, hole_y, 0) * b3d.Rot(0, 90, 0) * b3d.Cylinder(cross_pin_d / 2, 100)


def baseplate_channel():
    """Cutters for the baseplate channel (world frame): between the motor
    columns, from each tower end in to the line bar edge -> window edge."""
    y0, y1 = baseplate_y0, baseplate_y0 + base_t          # baseplate outer face, top
    win_z = base_gap / 2 + window_z0                       # inner edge of the JST windows
    far = 100.0
    cutters = []
    for side, bar_z in ((-1, holder_front_z), (1, holder_back_z)):
        def z_at(y):
            # line from (holder_base_y, side*bar_z) to (y1, side*win_z)
            return side * (bar_z + (win_z - bar_z) * (y - holder_base_y) / (y1 - holder_base_y))
        prof = b3d.Polygon((y0, z_at(y0)), (y0, side * far), (y1, side * far), (y1, z_at(y1)),
                           align=None)
        cutters.append(b3d.extrude(b3d.Plane.YZ * prof, amount=block_gap / 2, both=True))
    return b3d.Compound(children=cutters)


def end_cuts():
    """Offcut removers (world frame): beyond each mount_outer line moved
    end_cut_inset toward the tower's centre, across the full width."""
    tip_y = baseplate_y0 - rib_d - dovetail_height        # pin tip
    far = 200.0
    cutters = []
    for side, outer_z in ((-1, holder_outer_front_z), (1, holder_outer_back_z)):
        a = b3d.Vector(0, tip_y, side * mount_r)
        b = b3d.Vector(0, holder_base_y, side * outer_z)
        d = (b - a).normalized()
        n = b3d.Vector(0, -d.Z, d.Y)                        # normal in the YZ plane
        if n.Z * side > 0:                                  # point toward z = 0
            n = -n
        a, b = a + n * end_cut_inset, b + n * end_cut_inset
        # the inset line, extended far both ways, closed on the outboard side
        p0, p1 = a - d * far, b + d * far
        q0, q1 = p0 - n * far, p1 - n * far
        prof = b3d.Polygon((p0.Y, p0.Z), (p1.Y, p1.Z), (q1.Y, q1.Z), (q0.Y, q0.Z), align=None)
        cutters.append(b3d.extrude(b3d.Plane.YZ * prof, amount=far, both=True))
    return b3d.Compound(children=cutters)


def tower():
    # no bent tabs: nothing but the dovetail pin sticks out past the baseplate
    (_, jaw, _), = load_part(ORIGINAL / "gripper.py", include_tab=False)
    jaw = jaw + hole_plugs() + wall_plugs()
    ty = baseplate_y0 + plate_t
    jaw_a = location(R_UP, (-plate_cx, ty, base_gap / 2 - plate_z0)) * jaw
    jaw_b = location(R_FLIP_Y, (plate_cx, ty, plate_z0 - base_gap / 2)) * jaw
    bridge = b3d.Pos(0, baseplate_y0 + base_t / 2, 0) * b3d.Box(plate_w, base_t, base_gap)
    body = jaw_a + jaw_b + bridge
    depth = plate_t + block_d                # outer baseplate face to the back of the blocks
    yc = baseplate_y0 + depth / 2
    height = 2 * (base_gap / 2 + plate_h)    # full tower height
    if fill_gap_x:
        body += b3d.Pos(0, yc, 0) * b3d.Box(block_gap, depth, height)
    if fill_gap_z:
        body += b3d.Pos(0, yc, 0) * b3d.Box(plate_w, depth, base_gap)
    body -= window_chamfers()
    if include_pin:
        body += dovetail_pin()
    if include_channel:
        body -= baseplate_channel()
    if include_end_cuts:
        body -= end_cuts()
    return body


part = tower()

if "show_object" in globals():
    show_object(part, name="tower", color="steelblue")
