# Dovetail mount — variant of the bayonet casing.
#
# Keeps the bayonet casing's mounting disc and screw holes (see
# ../../components/bayonet_casing.py) but replaces the twist ring with a solid
# boss of the same size, with a dovetail slot cut straight across it.
#
# Local frame: axis +Z, disc bottom at z = 0, screw holes on X, slot running
# along Y. The slot opens on the top face with the narrow side of the
# trapezoid and widens toward the disc, so a matching dovetail slides in
# along Y and is held in Z. A cross-pin hole runs along X through the boss
# and across the slot at y = 0, at the slot's mid-height, matching the one
# through the tower's dovetail pin (tower.py) to lock it in place. Units mm.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

import sys
from pathlib import Path

import build123d as b3d

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dovetail import dovetail_height, dovetail_sketch  # noqa: E402

# ---- mounting disc (from bayonet_casing.py) ------------------------------
disc_r = 37.5
disc_h = 5.0
disc_chamfer = 1.0       # 45 deg, both faces
hole_pitch = 63.0        # two holes on the X axis, +-31.5
hole_r = 3.25            # 6.5 mm through-hole
csk_r = 6.0              # 90 deg countersink, 12 mm at the boss-side face
csk_depth = 2.75         # == csk_r - hole_r for a 90 deg countersink

# ---- boss (replaces the bayonet ring) ------------------------------------
boss_r = 28.0 * 1.00056  # bayonet ring OD
boss_h = 7.35 * 1.00056  # bayonet ring height above the disc

# ---- cross-pin hole ------------------------------------------------------
cross_pin_d = 3.0        # through hole along X, at y = 0 and the slot's mid-height

big = 200.0  # generous cutter length


def cyl_z(r, z0, z1, x=0.0, y=0.0):
    return b3d.Pos(x, y, (z0 + z1) / 2) * b3d.Cylinder(r, z1 - z0)


def dovetail_mount():
    top = disc_h + boss_h
    disc = cyl_z(disc_r, 0, disc_h)
    disc = b3d.chamfer(disc.edges().filter_by(b3d.GeomType.CIRCLE), disc_chamfer)
    body = disc + cyl_z(boss_r, disc_h, top)
    for sx in (-1, 1):
        x = sx * hole_pitch / 2
        body -= cyl_z(hole_r, -big, big, x)
        body -= b3d.Pos(x, 0, disc_h - csk_depth / 2) * b3d.Cone(hole_r, csk_r, csk_depth)
        body -= cyl_z(csk_r, disc_h, big, x)   # head clearance through the boss
    # Plane.XZ maps sketch +Y to world +Z; extruding both ways cuts along Y
    profile = b3d.Pos(0, 0, top - dovetail_height) * (b3d.Plane.XZ * dovetail_sketch())
    slot = b3d.extrude(profile, amount=big, both=True)
    hole_z = top - dovetail_height / 2
    cross_pin = b3d.Pos(0, 0, hole_z) * b3d.Rot(0, 90, 0) * b3d.Cylinder(cross_pin_d / 2, 2 * big)
    return body - slot - cross_pin


mount = dovetail_mount()

if "show_object" in globals():
    show_object(mount, name="dovetail_mount", color="steelblue")
