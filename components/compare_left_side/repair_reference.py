"""Make the vendor "Left side (microcont).step" a valid OCCT boolean argument.

The vendor solid fails BRepAlgoAPI_Check with BOPAlgo_SelfIntersect: the
vertex where its partial base chamfer ends, (-50, -8.8607, 40.002), lies on
the plate's back-top edge (x = -50, z = 40.002) without splitting it. Any
boolean against the raw solid (and therefore `lamad re compare`) is then
luck-dependent and usually returns an empty intersection.

This script splits that edge at the offending vertex (BRepTools_ReShape),
runs ShapeFix, and writes vendor_repaired_ref.step next to itself. Geometry
is untouched (volume 51717.44 mm^3 before and after); only the topology
changes (299 -> 300 edges). Compare with:

    lamad re compare components/compare_left_side/vendor_repaired_ref.step \
        components/left_side.py --out <scratch>/cmp

Run with lamad's interpreter:
    ~/.local/share/uv/tools/lamad/bin/python3 -I repair_reference.py
"""
import os
import sys

from build123d import import_step, export_step
from build123d.topology import Shape
from OCP.BRepAlgoAPI import BRepAlgoAPI_Check
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCP.BRepTools import BRepTools_ReShape
from OCP.ShapeFix import ShapeFix_Shape
from OCP.TopExp import TopExp
from OCP.TopoDS import TopoDS

here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    here, "..", "Left side (microcont).step")
dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
    here, "vendor_repaired_ref.step")

ref = import_step(src).solids()[0]
check = BRepAlgoAPI_Check(ref.wrapped, True, True)
if check.IsValid():
    print("reference already passes BRepAlgoAPI_Check; nothing to do")
    sys.exit(0)

shape = ref.wrapped
for result in check.Result():
    faulty = list(result.GetFaultyShapes1())
    verts = [s for s in faulty if s.ShapeType().name == "TopAbs_VERTEX"]
    edges = [s for s in faulty if s.ShapeType().name == "TopAbs_EDGE"]
    print("status", result.GetCheckStatus(), "vertices", len(verts), "edges", len(edges))
    if len(verts) != 1 or len(edges) != 1:
        continue
    vtx, edg = TopoDS.Vertex(verts[0]), TopoDS.Edge(edges[0])
    v1, v2 = TopExp.FirstVertex_s(edg), TopExp.LastVertex_s(edg)
    e1 = BRepBuilderAPI_MakeEdge(v1, vtx).Edge()
    e2 = BRepBuilderAPI_MakeEdge(vtx, v2).Edge()
    reshape = BRepTools_ReShape()
    reshape.Replace(edg, BRepBuilderAPI_MakeWire(e1, e2).Wire())
    shape = reshape.Apply(shape)

fix = ShapeFix_Shape(shape)
fix.Perform()
fixed = Shape.cast(fix.Shape()).solids()[0]
print("volume before %.4f after %.4f, edges %d -> %d" % (
    ref.volume, fixed.volume, len(ref.edges()), len(fixed.edges())))
export_step(fixed, dst)
print("wrote", dst)
