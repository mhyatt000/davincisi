# Lower cap — the horn-side part of the capstan, the mirror of the upper cap
# (coupling_interface.py) at the other end of the symmetric spring
# (dynamixel_spring.py with mirror=True).
#
# It is screwed to the XL/XC-330 horn through 4 holes on the 12 mm horn bolt
# circle (counterbored from the top), then the spring is set on it: three
# 3 mm lugs (the "pins") standing on the top face drop into the lower disc's
# three rim notches, the same way the upper cap's lugs engage the top disc.
# Shaped like the upper cap: a r13 body, a 45 deg cone out to a r14 flange.
# The lugs fill the notches: full disc depth, from the notch floor to the
# rim. The top face takes the lower disc's plate underside; a pocket clears
# the disc's hub ring. Underneath, a hemispherical
# dimple clears the horn's M2.6 screw head, and a centre hole joins it to the
# spring's bore (screwdriver access to the horn screw).
#
# Frame = dynamixel_spring.py's: axis +Y through the origin, underside at
# y 2.9 (on the horn face), top face at y 9.0 (lower disc plate underside).
# Units mm.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

# ---- body ----------------------------------------------------------------
y0 = 2.9                   # underside (on the horn)
face_y = 9.0               # top face = lower disc plate underside
body_r = 13.0              # like the upper cap: r13 body ...
cone_h = 1.0               # ... 45 deg cone ...
flange_r = 14.0            # ... r14 flange up to the face
flange_h = 3.0

# ---- lugs (pins into the lower disc's notches) ---------------------------
lug_count = 3
lug_w = 3.0                # notch_w in dynamixel_spring.py
lug_h = 3.0                # full notch depth (disc_t): flush with the disc top
lug_r0 = 11.1              # inner end on the notch floor (notch_floor_r)
lug_deg = 26.47 + 180      # pattern_rot + 180 in dynamixel_spring.py (notch directions)

# ---- pocket for the lower disc's hub ring (r5 x 1 mm below the plate) ----
pocket_r = 5.2
pocket_d = 1.0

# ---- horn screws: 4 x on the 12 mm bolt circle ---------------------------
bolt_circle = 12.0
bolt_hole_r = 1.0
bolt_cbore_r = 2.0         # M2 head clearance
bolt_seat = 2.0            # material under the heads (y0 .. y0 + bolt_seat)

# ---- centre: horn screw clearance + driver access -----------------------
dimple_r = 3.0             # hemisphere in the underside; 0 = none
center_hole_r = 2.8

# ========================================================================

def cyl_y(r, y0, y1, x=0.0, z=0.0):
    return Pos(x, (y0 + y1) / 2, z) * (Plane.XZ * Cylinder(r, y1 - y0))

def cone_y(r0, y0, r1, y1):
    """Frustum with radius r0 at y0 and r1 at y1 (y1 > y0)."""
    return Pos(0, (y0 + y1) / 2, 0) * (Plane.XZ * Cone(r1, r0, y1 - y0))

y_cone = face_y - flange_h            # flange underside
y_body = y_cone - cone_h              # body top
cap = cyl_y(body_r, y0, y_body + 0.01)
cap += cone_y(body_r, y_body, flange_r, y_cone)
cap += cyl_y(flange_r, y_cone - 0.01, face_y)

# lugs: radial blocks on the face, trimmed to the flange radius
lug = Pos((lug_r0 + flange_r + 1) / 2, face_y + lug_h / 2, 0) * Box(flange_r + 1 - lug_r0, lug_h, lug_w)
rim = cyl_y(flange_r, face_y - 0.01, face_y + lug_h)
for k in range(lug_count):
    cap += Rot(0, -(lug_deg + 360 * k / lug_count), 0) * lug & rim

cap -= cyl_y(pocket_r, face_y - pocket_d, face_y + 1)
for loc in PolarLocations(bolt_circle / 2, 4):
    p = loc.position
    cap -= cyl_y(bolt_hole_r, y0 - 1, face_y + 1, p.X, p.Y)
    cap -= cyl_y(bolt_cbore_r, y0 + bolt_seat, face_y + 1, p.X, p.Y)
cap -= cyl_y(center_hole_r, y0 - 1, face_y + 1)
if dimple_r > 0:
    cap -= Pos(0, y0, 0) * Sphere(dimple_r)

show_object(cap, name="lower_cap", color="goldenrod")
