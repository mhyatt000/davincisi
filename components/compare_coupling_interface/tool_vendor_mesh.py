"""Fine, watertight tessellation of the vendor STEP.

OCCT's mesher mis-triangulates three sloppy 45-degree cone faces of the vendor
solid at any deflection finer than 0.1 mm (their triangulation area is off by
30-40 %), which leaves the STL open. We mesh everything at 0.004 mm, drop those
faces' triangles and re-triangulate each one by zipping its two boundary loops
(they are all annular cones between two circles).

usage: vendor_mesh.py OUT.stl [deflection] [angle]
"""
import sys, math
import numpy as np
import trimesh
from build123d import import_step
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
from OCP.TopAbs import TopAbs_REVERSED
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cone

REF = "/Users/matthewhyatt/repo/davincisi/components/Coupling Interface (3.15)(M) (prt 4).step"
out = sys.argv[1]
defl = float(sys.argv[2]) if len(sys.argv) > 2 else 0.004
ang = float(sys.argv[3]) if len(sys.argv) > 3 else 0.08

ref = import_step(REF).solids()[0]
BRepMesh_IncrementalMesh(ref.wrapped, defl, False, ang, True)

V, T, bad = [], [], []
for f in ref.faces():
    loc = TopLoc_Location()
    t = BRep_Tool.Triangulation_s(f.wrapped, loc)
    if t is None:
        bad.append(f); continue
    tr = loc.Transformation()
    P = np.array([[p.X(), p.Y(), p.Z()] for p in (t.Node(k + 1).Transformed(tr) for k in range(t.NbNodes()))])
    tri = np.array([[t.Triangle(k + 1).Value(i) - 1 for i in (1, 2, 3)] for k in range(t.NbTriangles())])
    if f.wrapped.Orientation() == TopAbs_REVERSED:
        tri = tri[:, ::-1]
    a, b, c = P[tri[:, 0]], P[tri[:, 1]], P[tri[:, 2]]
    area = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1).sum()
    if abs(area - f.area) > 0.02 * max(f.area, 0.05) + 0.01:
        bad.append(f); continue
    T.append(tri + sum(len(v) for v in V))
    V.append(P)
V = np.vstack(V); T = np.vstack(T)
m = trimesh.Trimesh(V, T, process=False)
trimesh.tol.merge = 1e-6
m.merge_vertices()
print(f"meshed {len(ref.faces()) - len(bad)} faces normally; {len(bad)} faces re-zipped:",
      [(f.geom_type.name, round(f.area, 2)) for f in bad])

# boundary loops of the open mesh
from trimesh.grouping import group_rows
es = m.edges_sorted
bidx = group_rows(es, require_count=1)
bedges = es[bidx]
adj = {}
for u, v in bedges:
    adj.setdefault(u, []).append(v); adj.setdefault(v, []).append(u)
loops, seen = [], set()
for s in adj:
    if s in seen: continue
    loop, prev, cur = [s], None, s
    seen.add(s)
    while True:
        nxt = [w for w in adj[cur] if w != prev and w not in seen]
        if not nxt: break
        prev, cur = cur, nxt[0]
        loop.append(cur); seen.add(cur)
    loops.append(np.array(loop))
print("boundary loops:", [len(l) for l in loops])

new_tris = []
for f in bad:
    ad = BRepAdaptor_Surface(f.wrapped)
    assert ad.GetType() == GeomAbs_Cone, f.geom_type
    cone = ad.Cone(); L = cone.Location(); D = cone.Axis().Direction()
    axis = np.array([D.X(), D.Y(), D.Z()]); origin = np.array([L.X(), L.Y(), L.Z()])
    # loops that lie on this face
    mine = [l for l in loops if all(f.distance_to(tuple(m.vertices[i])) < 0.02 for i in l[::max(1, len(l) // 8)])]
    assert len(mine) == 2, (f.geom_type, len(mine))

    def angles(l):
        p = m.vertices[l] - origin
        p -= np.outer(p @ axis, axis)
        ex = np.cross(axis, [0, 0, 1.0]) if abs(axis[2]) < 0.9 else np.cross(axis, [1.0, 0, 0])
        ex /= np.linalg.norm(ex); ey = np.cross(axis, ex)
        return np.arctan2(p @ ey, p @ ex)
    A, B = mine
    ta, tb = angles(A), angles(B)
    A = A[np.argsort(ta)]; B = B[np.argsort(tb)]; ta.sort(); tb.sort()
    # zip the two loops by angle (merge walk around the full circle)
    i = j = 0; na, nb = len(A), len(B)
    while i < na or j < nb:
        next_a = (ta[(i + 1) % na] + (2 * math.pi if i + 1 >= na else 0)) if i < na else math.inf
        next_b = (tb[(j + 1) % nb] + (2 * math.pi if j + 1 >= nb else 0)) if j < nb else math.inf
        if next_a <= next_b:
            new_tris.append([A[i % na], B[j % nb], A[(i + 1) % na]]); i += 1
        else:
            new_tris.append([A[i % na], B[j % nb], B[(j + 1) % nb]]); j += 1

full = trimesh.Trimesh(np.vstack([m.vertices]), np.vstack([m.faces, np.array(new_tris)]), process=False)
full.merge_vertices()
full.update_faces(full.nondegenerate_faces())
trimesh.repair.fix_winding(full)
trimesh.repair.fix_normals(full)
print(f"final: watertight={full.is_watertight} winding_consistent={full.is_winding_consistent} "
      f"vol={full.volume:.3f} (brep {ref.volume:.3f}) tris={len(full.faces)}")
full.export(out)
