# Helpers for composing part scripts: exec a script and capture what it
# shows, and build placements. Same conventions as ../../assembly.py.
#
# Imported by assembly-style scripts; not a part itself.

import re
from pathlib import Path

import build123d as b3d

I3 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE.parents[1] / "components"   # the original project's part scripts

_cache = {}


def override_literals(source, params):
    """Rewrite top-level `name = <literal>` lines, like `lamad run --param`."""
    for k, v in params.items():
        source, n = re.subn(rf"^{k}\s*=[^#\n]*", f"{k} = {v!r}", source, count=1, flags=re.M)
        if not n:
            raise KeyError(f"no top-level literal {k!r} to override")
    return source


def load_part(path, **params):
    """Exec a part script in its own namespace; return [(name, shape, color)].

    Keyword arguments override the script's top-level literals (its knobs).
    Cached per (path, params).
    """
    path = Path(path).resolve()
    key = (path, tuple(sorted(params.items())))
    if key in _cache:
        return _cache[key]
    parts = []

    def capture(obj, name=None, color=None, **_):
        if isinstance(obj, b3d.ShapeList):
            obj = obj[0] if len(obj) == 1 else b3d.Compound(children=list(obj))
        parts.append((name or f"part{len(parts) + 1}", obj, color))

    g = {k: getattr(b3d, k) for k in getattr(b3d, "__all__", dir(b3d)) if not k.startswith("_")}
    g.update(__name__="__part__", __file__=str(path), show_object=capture)
    exec(compile(override_literals(path.read_text(), params), str(path), "exec"), g)
    _cache[key] = parts
    return parts


def location(R, t):
    """Location for p_world = R @ p_local + t (R row-major, proper rotation)."""
    x_dir = (R[0][0], R[1][0], R[2][0])
    z_dir = (R[0][2], R[1][2], R[2][2])
    return b3d.Location(b3d.Plane(origin=t, x_dir=x_dir, z_dir=z_dir))


def show_placed(show_object, node, path, R, t):
    """Load `path`, place it with (R, t) and show it under `node`."""
    parts = load_part(path)
    loc = location(R, t)
    for pname, shape, color in parts:
        name = node if len(parts) == 1 else f"{node}/{pname}"
        show_object(loc * shape, name=name, color=color)
