# bu1ld0r

A 3D model builder in QB64 Phoenix Edition. Put simple shapes together
(boxes, cylinders, spheres, cones, wedges and tubes), size, turn and colour
them, and save the model. It saves as its own file to edit again, as an
OBJ for any 3D program, and as a ready-made NEON-CASTER prop.

Save what you build as a prefab and it goes in the bin, ready to drop
onto another model's faces, linked: change the prefab and every model
using it changes.

Coming next (see [PLAN.md](PLAN.md)):
- pictures on faces, and painting straight onto the model;
- divide and push/pull;
- booleans (a part that cuts a hole, or keeps only the overlap), and retopology (a clean, light mesh for the game);
- a starter set of prefabs (toggles, buttons, knobs, pipes...).

## Build

```
~/git/qb64pe/qb64pe -w -x bu1ld0r.bas -o bu1ld0r.run
```

## Using it

- **Put a shape down:** pick it on the left (or press 1-6), then click where it goes. It stands on the face you point at, standing out from it, or on the grid. You can also drag it straight from the bin. Shift keeps putting more down; Esc stops.
- **Set it up first:** while you're putting a shape down (nothing selected), the panel is the new shape's: its size, its own turn (on top of the face's), slices, amount, colour, HOLE. Type, use the wheel, or middle-click a field, then click where it goes. The ghost stays where it was while you work in the panel.
- **Holes:** C (or HOLE in the panel) makes the selection a hole: it's cut out of every solid part before it in the parts list, and its walls take that part's colour. It stays a part: move it, size it, make it solid again (C). A hole shows as see-through grey; click it to pick it. One put down onto a face goes into it, top flush, like a drill: a narrow cylinder on a cylinder's top as tall as it goes straight through. Prefabs can hold holes, and a hole can be a prefab.
- **The parts list** (L, or PARTS at the top): every part by name, between the bin and the view, so you can pick one hidden inside another. Click to select (Shift adds), double-click to rename. The dot shows or hides a part (the export still has it); the square shows it as lines only. UP and DOWN move the selection earlier or later in the list: a hole cuts only what's above it.
- **Select:** click a part (Shift adds it to the selection; Tab goes to the next).
- **Move:**
  - drag a part to move it across the ground (Shift: up and down);
  - arrows nudge it, and PgUp/PgDn raise and lower it;
  - R turns it 15 degrees;
  - = and - make it bigger or smaller.

  Moves snap to the grid (SNAP in the panel); hold Alt for none.
- **Exact numbers:** the panel on the right has the position, turn, size, slices (round shapes), the amount (a cone's top, a tube's hole, how much of a sphere) and the colour. Click a field and type (Enter), or turn the wheel over it: 1 a step, 10 with Shift, 0.1 with Alt. A middle click puts a field back to its usual value (position and turn 0, the shape's own size, a prefab's scale 1).
- **The view:** right drag turns round it, middle drag (or Shift + right drag) pans, the wheel zooms, F frames the model, Home goes back to the start. W (or WIRE at the top) switches to a wireframe: each part's edges in its own colour, with the grid seen through, and clicking still picks parts and faces.
- **Edit:** Ctrl+Z undo, Ctrl+Y redo, Ctrl+D copy, Delete removes, Ctrl+A selects everything.
- **Files:**
  - Ctrl+S saves `models/NAME.bld` (the NAME box at the top);
  - Ctrl+O opens one;
  - Ctrl+N starts a new model;
  - Ctrl+E exports `export/NAME.obj`, `.mtl` and `_tex.png`.
- **Prefabs:**
  - PREFAB at the top (Ctrl+Shift+S) saves the model as `prefabs/NAME.bld`, in the bin's open folder. From then on Ctrl+S saves it there.
  - The bin shows them under the shapes. Click one, or drag it, onto a face: it stands out from that face like a shape does.
  - A prefab in a model stays linked to its file. Move, turn and scale it as one piece (its SIZE fields are its SCALE); right-click it in the bin to open and change it, and every model using it follows.
  - Folders: + FOLDER makes one in the folder that's open; click a folder to go in, `..` to go back up.
  - A prefab that's gone missing shows as a red box, and EXPORT waits until it's back.
- **The window:** drag it to any size; once you let go, everything is laid out again to fill it (the 3D view takes the room). The UI is drawn at a whole-number scale, so it stays crisp: 2x on a 4K display, chosen for you at first. Ctrl+ and Ctrl- change it. F11 (or Alt+Enter) is full screen. The size and scale are kept in `bu1ld0r.cfg` (`window=`, `ui_scale=`), and whether the parts list is shown (`parts_list=`).
- **Help:** H (or F1) lists every key.

Sizes are NEON-CASTER map cells: 1 is a wall's width, and the purple
square on the grid is one cell. A model's foot is the middle of that
square, and its front faces -Z (the short blue line).

## NEON-CASTER

Put the game's asset folder in `bu1ld0r.cfg`, beside the program:

```
neon_dir=/home/you/git/neon-caster/neon-caster
```

Then EXPORT also writes:
- `models/NAME.obj`;
- its texture at 64 and 256 (`hd/models/`);
- the 8 pictures round it that the software renderer draws.

The game draws any decoration or pickup as a model when a `models/NAME.obj`
of its picture's name exists. Until the game can place models of its own
(planned), export under a prop's name (`terminal`, `crate`...) to replace
that prop's model; `git checkout` the game's files to get the old one back.

Keep a prop near 200 triangles: the game works out every corner of every
nearby model each frame. The view shows the count, and slices change it.

## Command line

```
bu1ld0r.run [FILE.bld] [--open NAME] [--export] [--neon DIR] [--shot FILE.png] [--quit] [--bench N]
```

`--export`, `--shot` and `--quit` act a few frames after start-up, for tests.
`--bench N` makes the opened model's triangles N times (holes cut each
time) and writes how long one took to `bench.txt`.
