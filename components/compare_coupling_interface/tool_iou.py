"""Mesh-boolean IoU between the vendor STEP and the script (manifold3d via trimesh).

usage: iou.py OUTDIR [K=V ...]
"""
import sys, os, math, re, json
import numpy as np
import trimesh
import build123d as b3d
from build123d import import_step

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
params = dict(a.split("=", 1) for a in sys.argv[2:])
SCRIPT = "/Users/matthewhyatt/repo/davincisi/components/coupling_interface.py"
REF = "/Users/matthewhyatt/repo/davincisi/components/Coupling Interface (3.15)(M) (prt 4).step"
CX, CY, ZB = -0.0390318, 30.0490949, -7.40551

src = open(SCRIPT).read()
for k, v in params.items():
    src, n = re.subn(rf"^{k} = .*$", f"{k} = {v}", src, count=1, flags=re.M)
    assert n == 1, k
g = {k: getattr(b3d, k) for k in b3d.__all__}
shown = {}
g["show_object"] = lambda obj, name=None, color=None: shown.__setitem__(name, obj)
exec(compile(src, SCRIPT, "exec"), g)
mine = list(shown.values())[0]
ref = import_step(REF).solids()[0]


def to_mesh(shape, tol=0.004, ang=0.08, tag="m"):
    """Watertight STL via OCCT's own mesher + writer (shared edge polygons)."""
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.StlAPI import StlAPI_Writer
    import tempfile
    BRepMesh_IncrementalMesh(shape.wrapped, tol, False, ang, True)
    path = os.path.join(OUT, f"_{tag}.stl")
    w = StlAPI_Writer(); w.ASCIIMode = False
    assert w.Write(shape.wrapped, path)
    m = trimesh.load(path, process=False)
    trimesh.tol.merge = 1e-5
    m.merge_vertices()
    if not m.is_watertight:
        trimesh.repair.fill_holes(m)
    if m.volume < 0:
        m.invert()
    return m


mr = trimesh.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor_fine.stl"), process=False)
trimesh.tol.merge = 1e-6
mr.merge_vertices()
assert mr.is_watertight and mr.is_volume, "vendor mesh not a volume"
mm = to_mesh(mine, tag="mine")
print(f"ref mesh: watertight={mr.is_watertight} vol={mr.volume:.3f} (brep {ref.volume:.3f}) faces={len(mr.faces)}")
print(f"mine mesh: watertight={mm.is_watertight} vol={mm.volume:.3f} (brep {mine.volume:.3f}) faces={len(mm.faces)}")

inter = trimesh.boolean.intersection([mr, mm], engine="manifold")
missing = trimesh.boolean.difference([mr, mm], engine="manifold")
extra = trimesh.boolean.difference([mm, mr], engine="manifold")
vi, vmiss, vext = inter.volume, missing.volume, extra.volume
union = mr.volume + mm.volume - vi
res = {"ref_volume": mr.volume, "script_volume": mm.volume, "intersection": vi,
       "missing_volume": vmiss, "extra_volume": vext, "iou": vi / union,
       "params": params}
print(json.dumps(res, indent=1))
json.dump(res, open(os.path.join(OUT, "iou.json"), "w"), indent=1)
missing.export(os.path.join(OUT, "missing.stl"))
extra.export(os.path.join(OUT, "extra.stl"))


def describe(name, m, top=25):
    parts = sorted(m.split(only_watertight=False), key=lambda p: -abs(p.volume))
    print(f"\n{name}: {len(parts)} pieces, total {m.volume:.3f} mm3")
    for p in parts[:top]:
        c = p.centroid
        r = math.hypot(c[0] - CX, c[1] - CY)
        a = math.degrees(math.atan2(c[1] - CY, c[0] - CX))
        b = p.bounds
        print(f"  vol={p.volume:7.3f}  r={r:6.2f} ang={a:7.1f} z={c[2] - ZB:6.2f}  "
              f"dz={b[0][2] - ZB:5.2f}..{b[1][2] - ZB:5.2f}  rmin/max≈ "
              f"{min(math.hypot(x - CX, y - CY) for x, y, _ in p.vertices):5.2f}/"
              f"{max(math.hypot(x - CX, y - CY) for x, y, _ in p.vertices):5.2f}")


describe("MISSING (in vendor, not in script)", missing)
describe("EXTRA (in script, not in vendor)", extra)
