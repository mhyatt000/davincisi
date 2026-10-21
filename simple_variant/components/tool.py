# Tool — rough placeholder for the tool that sits in the tool holder.
#
# Its cross-section is the tool holder's inner geometry seen from the top: the
# through-window at the holder's top face (the back-half window profile),
# closed along the holder's back edge. The profile is taken from
# tool_holder.py's own outline and window edges, so it follows that part.
#
# The placeholder starts at the holder's top face, rises tool_h above it, then
# finishes with a dome_h dome lofted smoothly to a point at the profile's
# centroid. The part of the tool inside the holder is not modelled.
#
# Frame: the tool holder's (the original assembly's), so the assembly places
# it with the same transform as the tool holder. "Up" (away from the holder's
# base) is +Y here. Units mm.
#
# Top-level literals below are the knobs `lamad run --param K=V` can turn.

import math
import sys
from pathlib import Path

import build123d as b3d

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from partlib import override_literals  # noqa: E402

# ---- knobs ---------------------------------------------------------------
tool_h = 5.0             # straight part above the holder's top face
dome_h = 15.0            # dome on top, lofted to the profile's centroid
dome_steps = 12          # intermediate dome sections (more = rounder)


def holder_namespace():
    """Run tool_holder.py (without its pins, which the profile doesn't need)
    and return its namespace: knobs, outline and window edges."""
    path = HERE / "tool_holder.py"
    g = {k: getattr(b3d, k) for k in b3d.__all__}
    g.update(__name__="__part__", __file__=str(path), show_object=lambda *a, **k: None)
    src = override_literals(path.read_text(), {"include_pins": False})
    exec(compile(src, str(path), "exec"), g)
    return g


h = holder_namespace()
# window at the top face = back-half window profile, clipped to the outline
local = b3d.make_face(h["outline"]) & b3d.make_face(h["back_profile"])
top_y = h["y_front"] + h["thick"]                           # holder's top face
profile = b3d.Pos(h["x_center"], 0, 0) * local.faces()[0]  # XZ plane at y = 0
centre = profile.center()


def section(y, scale):
    """The profile scaled about its centroid, on the plane at height y."""
    f = b3d.Pos(centre.X, 0, centre.Z) * b3d.scale(b3d.Pos(-centre.X, 0, -centre.Z) * profile, scale)
    return b3d.Pos(0, y, 0) * f


body_top = top_y + tool_h
straight = b3d.Pos(0, top_y, 0) * b3d.extrude(profile, amount=tool_h, dir=(0, 1, 0))
# dome: quarter-ellipse in height, sections shrinking to a point at the
# centroid; ruled between sections (a smooth loft overshoots the height)
sections = [section(body_top, 1.0)]
for i in range(1, dome_steps + 1):
    t = i / (dome_steps + 1)
    sections.append(section(body_top + dome_h * t, math.sqrt(1 - t * t)))
tip = b3d.Vertex(centre.X, body_top + dome_h, centre.Z)
dome = b3d.loft(sections + [tip], ruled=True)
tool = straight + dome

if "show_object" in globals():
    show_object(tool, name="tool", color="khaki")
