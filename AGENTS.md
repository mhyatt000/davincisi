# AGENTS.md

An open platform adaptor for da Vinci SI surgical instruments. The mechanical
parts are being rebuilt as parametric build123d scripts reverse-engineered
from the original CAD.

**Before any CAD or reverse-engineering work, read `reverse-engineer.md`.** It
covers the method: work one component at a time, clean the vendor STEP, read
geometry from `lamad re inspect`, write scripts for `--param`, work around
OCCT boolean failures, and judge results by the missing/extra diff solids.

## Layout

- `components/`: one script per original part, `<snake_name>.py`, built in its
  vendor STEP's frame. The reference STEP/STL files sit beside them. Compare
  artifacts go in `components/compare_<snake_name>/`.
- `components/Vendor/`, `components/bom/`: purchased parts (Igus rail and
  carriage, Dynamixel).
- `assembly.py` / `assembly_full.py`: compose the parts in the frame of
  `Da vinci si manipulator.stl` so the result diffs directly against it.
- `simple_variant/`: the deviating design. Parts live in
  `simple_variant/components/`; `partlib.py` loads a script and overrides its
  top-level literals, and `simple_variant/assembly.py` only composes.
- `mycad/`: separate CAD tooling and projects. Leave it alone unless asked.

## Duplicate references

Most STLs are exports of a STEP, so reverse-engineer the STEP only:

- `Base.stl` = `Main body.step`
- `Left Wall.stl` = `Right side.step`, `Right wall.stl` =
  `Left side (microcont).step` (names swapped)
- `Orthoplanar Spring.stl` = `Dynamixel Spring (15.5mm)(M) (prt 4).step`
- `xarm-bayonet-mount.stl` = `Bayonet casing v10.step`
- Root `R Wall.step` duplicates `Left side (microcont).step`
- STL only: `Slot Holder.stl`, `Tool slot selection.stl`

## Script conventions

- Units are mm. Keep the vendor coordinate frame exactly; compare does no
  alignment.
- Every dimension is a top-level scalar literal so `--param` can override it.
  Negative literals and lists are not exposed, so express patterns as pitch
  plus centre.
- Add boolean toggles for optional hardware.
- Use one `show_object` per physical part, named after the vendor part.

## lamad

- lamad is an external, read-only tool. Never write into its directory.
- Always pass `--out <scratch dir>` to `re inspect`, `re compare` and
  `render`, and iterate with `--no-preview`.
- `det`, `inspect` and `measure` take STEP only; `compare` also accepts STL.
- Do not record lamad versions (use `lamad run --dry-run` only). The user does
  that.

## Git

- Don't commit PNGs, `.DS_Store` or Python caches (they are gitignored).
  Generated STLs in `exports/` and the `compare_*` folders stay untracked
  unless asked.
- Commit or push only when asked.
