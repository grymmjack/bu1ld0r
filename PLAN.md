# bu1ld0r - the plan

A 3D model builder in QB64PE: put simple shapes together, picture and paint
them, save what you build as a prefab and build bigger things from those.
It writes plain OBJ + PNG, and a NEON-CASTER export the game loads as a prop.

Started 2026-10-30, after NEON-CASTER v0.12.0. A program of its own (like
DRAW) rather than a screen in the game: a modeler's 3D view, picking and
painting are simpler outside the game's OpenGL pipeline, and other projects
can use it.

## What it makes

- `models/NAME.bld` - the model as built (text, below): what you open and edit.
- `prefabs/[FOLDER/]NAME.bld` - a model saved as a prefab (the same text):
  what the bin shows, and what a model's `use` lines point to.
- `export/NAME.obj` + `NAME.mtl` + `NAME_tex.png` - for any 3D program.
- NEON-CASTER export (`neon_dir=` in `bu1ld0r.cfg`, the game's asset folder
  `neon-caster/neon-caster`): `models/NAME.obj` (with its `# frame` line),
  `models/NAME_tex.png` (64), `hd/models/NAME_tex.png` (256),
  `models/NAME_0.png` ... `NAME_7.png` (64 px, the model from 8 ways round,
  lit as models.py lights them - the software renderer's pictures).

Units are NEON-CASTER map cells: 1 is a wall's width. A model's foot is at
y = 0 round the origin; OBJ axes are y up, its front towards -z.

## The .bld file

```
bu1ld0r 1
name toggle
part box     0 0 0   0 0 0   0.25 0.1 0.25   C0C8D0  0  0
part cylinder 0 0.1 0  20 0 0  0.04 0.12 0.04 FF3040 12 0
```

`part KIND  x y z  turnX turnY turnZ  sizeX sizeY sizeZ  RRGGBB  slices  amount`
- kinds: box, cylinder, sphere, cone, wedge, tube. Each stands on its own
  origin (the middle of its foot), 1 x 1 x 1 at size 1.
- slices: round shapes' sides (0 = the usual 12).
- amount: a cone's top (0 a point, 1 a cylinder), a tube's hole (0-0.95),
  a sphere's share from the top (1 whole, 0.5 a dome).
- Turns are degrees, applied Z, then X, then Y.
- A prefab used whole: `use NAME  x y z  turnX turnY turnZ  scaleX scaleY scaleZ`
  (NAME its path in prefabs/ without .bld: `panels/toggle`). Its parts
  come from the prefab's file, so it's linked; prefabs can use prefabs.
- After the numbers, a part's flags, as words: `hole` (it cuts the solid
  parts before it), `hide` (not in the view; still exported), `wire`
  (lines only), `name=NAME` (no spaces), `keep` (a hole that keeps only
  the overlap), `group=N`, `tint=RRGGBBAA` (a use's: AA how much).
  Older copies ignore them.
- A mesh part: `part mesh  x y z  turns  sizes  RRGGBB 0 0`, then its
  points (`v x y z`, in its own 1 x 1 x 1) and polygons (`f RRGGBB 1 2 -3
  ...`: points from 1, less than 0 when the edge on isn't the shape's own).
  A polygon with a picture on it: `f RRGGBB @REF 1:u:v 2:u:v ...` - REF
  the picture in `pictures/` without .png (`neon/crate`), u and v each
  corner's spot on it (0..1 across and down from the top left).
- `budget N`: the tidied export's triangles at most (0: none); `tidy 1`:
  EXPORT tidies it (else it's sent as built).
- Later stages add lines after a part (`face`, `paint`).

## Stages

1. **Shapes and building** (done, 0.1.0): the 3D view (software-drawn: depth and
   which-part-is-where buffers, so picking and painting are exact), orbit /
   pan / zoom, the six shapes, select (Shift adds), drag to move (Shift: up
   and down), the panel's fields (position, turn, size, slices, amount,
   colour - typed, or the wheel), a palette, snap, duplicate, delete,
   undo/redo, NEW / OPEN / SAVE, EXPORT (OBJ, and NEON-CASTER's).
2. **The bin** (done, 0.2.0): shapes and prefabs as thumbnails, in folders
   (+ FOLDER, `..`); click or drag one onto the model and it lands on the
   face under the pointer, turned to stand out from it (a toggle stands up
   on a panel), snapped; Alt: free. SAVE AS PREFAB (PREFAB, Ctrl+Shift+S),
   and uses linked from the start (brought forward from stage 5);
   right-click a prefab in the bin to change it. Missing ones are red
   boxes, and EXPORT waits for them. Also: the window any size (as DRAW:
   laid out again to fill it, the UI at a whole-number scale - Ctrl+ /
   Ctrl-, F11 full screen).
3. **Pictures on faces**: any PNG on a part's face, with wrap, slide,
   stretch, turn and tint (as NEON-CASTER's level faces). Started (0.5.0):
   a mesh polygon can carry a picture with a spot per corner, drawn
   perspective-correct (VIEW: FillTriT), saved in the .bld, kept by the
   edit tools and by tidy, and exported in the one texture (OUT/EXPORT:
   ExAtlas). NEON-CASTER's props open as models with it (MODEL/IMPORT:
   OPEN lists them). Then (0.5.0, UI/PICS): the bin's PICTURES tab, a
   picture dragged or clicked onto a face (fitted), a PNG dropped on the
   window, and the picked faces' FIT / ACROSS ALL / TURN / FLIP / REPEAT /
   slide / NO PICTURE; the export cuts repeats (the game clamps). Still to
   do: tint. Also ALIGN (UI/ALIGN): parts, points, faces, as seen.
4. **Painting**: brushes straight onto the model, in 3D (every texel within
   the brush's reach, so strokes cross from part to part), on a layer of
   their own over the pictures. Export bakes it all into the one texture.
5. **Prefabs** (done, 0.4.0): what's left after stage 2 - unlink a use (its parts into
   the model as parts, as a group: turns combined into one Z-X-Y set, or a
   mesh part when a scale can't be one part's), a use's tint, renaming or
   moving a prefab (and its uses) from the bin's right-click menu.
6. **Divide and push/pull** (done, 0.4.0, as editing): any part's faces and points
   (E) - mesh parts (`part mesh`, then `v` and `f` lines in the .bld) -
   picked and moved, sized, turned, pushed out, extruded, inset, divided
   across or down (H / V), merged, flipped, coloured, taken away.
7. **Booleans**: holes done (0.3.0) - any part (a prefab too) can be a
   HOLE (C): its shape is taken out of every solid part before it in the
   list (a hole, a slot, a recess), live, so it can still be moved and
   sized; shown see-through grey and pickable; the walls take the colour
   of the part they're cut into; flattened on export. Faces near the hole
   are split only where they cross it, each piece kept or not by rays from
   its middle (MODEL/CSG). With it: the shape set up before it's put down
   (a hole put on a face drills into it), and the parts list (L: select,
   hide, lines only, rename, order). Still to do: KEEP (only where it
   overlaps: an intersection), and a hole cutting only the parts it's
   grouped with - both done (0.4.0), with APPLY: a hole made for good.
8. **Retopology** (done, 0.4.0: OUT/TIDY): the mesh tidied for the game, as the last step before
   export (and shown: the count before and after): corners welded, faces
   hidden inside other parts or pressed flat against them taken away,
   flat neighbours of one colour merged into fewer triangles, slivers
   from booleans cleaned up - and, if it's still over a budget
   (NEON-CASTER's ~200 a prop, set in the panel), simplified (edge
   collapse, keeping the outline, colour borders and the 8 pictures'
   look). The .bld keeps the parts as built; only the export is reduced.
   (The budget is the model's: `budget N` in the .bld. T shows it tidied.)
   Since 0.5.0 it's the model's choice (`tidy 1`, EXPORT: TIDIED in the
   panel): it loses detail, so EXPORT sends the model as built by default.
9. **Starter prefabs** (done, 0.4.0: `prefabs/starter/`): toggle, button, knob, dial, screen, vent, handle,
   pipe (straight, elbow, T), lamp, antenna (vents and dials use stage 7's
   cuts).

And on NEON-CASTER's side (its own work, later): a thing to place any
exported model in a sector (a `prop NAME` thing), the level editor's picker
showing them, and the game opening bu1ld0r (as it opens DRAW) and reloading
a model when its files change.

## Testing

As NEON-CASTER: build to `bu1ld0r.run`, run on Xvfb `:99` with
`WAYLAND_DISPLAY` unset, never on the user's display. Command line for
tests: `--open FILE`, `--export`, `--shot FILE.png`, `--quit`.
