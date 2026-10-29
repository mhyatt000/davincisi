# Reverse engineering a vendor STEP into a parametric build123d script with lamad

Lessons from reconstructing the Robotis XL/XC-330 servo case
(`components/dynamixel_330.py`, 0.971 IoU against the vendor file). Written
to carry over to other lamad projects.

> **Work at the component level first.** Split the vendor assembly into its
> individual solids and reverse engineer each one on its own: one script, one
> reference solid, one compare loop. Only once every component scores well do
> you compose them into the part or assembly. A whole-model compare fuses
> everything into one body, so a 0.3 mm recess on a 2,000 mm³ cap is 2% of that
> component but 0.1% of the assembly and disappears into the noise. The
> missing/extra lists also stay short and nameable when the reference is a
> single solid. Compose last, not first.

## 1. Set up so the tool stays clean

- Run lamad from outside its own directory (`uv run --project lamad lamad ...`
  from the repo root) and always pass `--out <scratch dir>` to `re inspect` and
  `re compare`. Without `--out` they write a report folder into the current
  directory. Never let that land in the tool's tree.
- Iterate with `--no-preview`; it is several times faster. Render once at the end.
- Keep derived artifacts (split STEPs, cleaned references, compare outputs) in
  a scratch directory. Copy only the final script and one comparison image
  into the project.

## 2. Clean the vendor file before comparing

- Vendor STEPs often carry **open shells** next to the solids: cosmetic thread
  surfaces on screws, decals, cable paths. `re compare` refuses mixed input.
  Re-export solids only (`import_step(...).solids()` → `export_step`) and
  compare against that copy. Keep the original untouched.
- Files named `DUMMY`, `SIMPLIFIED`, or `ENVELOPE` are mechanical envelopes:
  exterior and mounting interfaces are accurate, internals are not, and parts
  may interpenetrate (a 3.6 mm stem in a 3.35 mm bore). Model what the file
  shows, note the oddity for the user, and do not silently "fix" it.
- Hollow things are hollow in the vendor file. A connector housing with 58
  planar faces and a third of the box volume is a shell; a solid block will
  show up as a large *extra* volume.

## 3. Read geometry out of `re inspect`, not out of your head

The inspect report is the primary source. Patterns that worked:

- **Group cylinder faces by (radius, axis).** The set of origins at one radius
  is a hole pattern. Four `r=0.8` cylinders at `(±8, ±15)` from the body centre
  is a 16 × 30 mm M2 tap pattern; the same positions at `r=1.0` in the caps are
  clearance holes.
- **Group plane faces by (normal, offset) and sum areas.** The largest
  ±Z planes give the stack heights and seams; a plane whose area equals the
  full footprint is an exterior face, one with a small area is a lip or
  tongue that nests inside a neighbour. Exterior seams sit where both mating
  faces have the full area.
- **Use `uv_bounds` of a plane for pocket extents.** The two side walls of a
  pocket plus its ceiling pin down all six limits. Watch the sign of the v
  axis: pick the reading that stays inside the part's bounding box.
- **Cones are chamfers.** `reference_radius` at `origin` with
  `semi_angle = 45°` gives the chamfer size directly.
- **Check annuli with arithmetic.** A plane with area ≈ π(r₁² − r₂²) is the
  floor of a counterbore or a shallow recess between two cylinder radii you
  already found. This is how 0.2–0.3 mm recesses reveal themselves.
- **Cross-check the datasheet.** The 330 is quoted as 20 × 34 × 26 mm; the
  bounding box is 20 × 34 × 29 because the horns stand proud. Explain every
  disagreement before moving on.

## 4. Write the script for `--param`, not just for the shape

- Every dimension is a **top-level literal**; lists and tuples are not
  overridable, so hole patterns are expressed as pitch + centre literals and
  expanded below a `# ====` separator.
- Add **boolean toggles** for optional hardware (`include_screws`,
  `include_connectors`, `include_led`). They let compare isolate the body
  from the fittings, and let the runner's parameter discovery bisect failures.
- Keep the vendor's coordinate frame exactly. Compare does no alignment, so a
  frame choice that differs by even a mirror gives a meaningless score.
- Use a generous `big` length for through cutters rather than the exact part
  thickness; it avoids coplanar cutter ends.
- One `show_object` per physical part, named like the vendor leaf. The
  comparison still fuses them, but the names make the diff readable.

## 5. Expect OCCT booleans to fail on exact coincidence

The better the model, the more of its faces land exactly on the reference's.
OCCT's cut returns *not done* when a cylinder **and** its floor plane both
coincide (a counterbore reproduced to the vendor's exact radius and depth).
Fuzzy tolerance does not rescue it.

- Diagnose by cutting the fused reference against each reconstruction part
  one at a time, then against individual reference solids. The failing pair
  localises the feature in two passes.
- Work around with a 0.05 mm nudge passed as `--param`, so the script keeps
  the true value and the workaround lives on the command line.
- Avoid exact-equal radii between your own parts too (a cap with
  `r == bore_r` is a coincident cylinder inside the fuse step).
- Long term this needs the tool's boolean to use BOPAlgo glue mode.

## 6. Read the score through the diff solids, not the number

Volume IoU saturates fast; 0.95 → 0.97 was all cosmetic. The useful output is
`missing.step` and `extra.step`:

- Run `re inspect --no-preview` on each and sort solids by volume. The
  bounding box of each fragment names the feature: a ±3.35 disc at the back
  cap's bore depth is "bore should be a 1.2 mm recess, not a through hole".
- Fix the top three by volume, re-run, repeat. Stop when the fragments are
  thinner than the tolerance you care about.
- Read the preview PNG with the solid-difference column; red is reference
  material you lack, teal is material you added.

## 7. Checklist for a new component

1. Clean reference: solids only, one solid per file for component-level work.
2. `re inspect` the solid; tabulate cylinders by radius, planes by offset.
3. Write the script in the vendor frame with literal parameters and toggles.
4. `re compare --no-preview`; if the boolean fails, bisect by toggles and
   nudge the offending literal via `--param`.
5. Inspect `missing.step` / `extra.step`, fix the largest fragments, repeat.
6. Render the preview once, check it by eye, then compose with the other
   components.
