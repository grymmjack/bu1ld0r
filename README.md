# bu1ld0r

A 3D model builder in QB64 Phoenix Edition. Put simple shapes together
(boxes, cylinders, spheres, cones, wedges and tubes), size, turn and colour
them, and save the model. It saves as its own file to edit again, as an
OBJ for any 3D program, and as a ready-made NEON-CASTER prop.

Coming next (see [PLAN.md](PLAN.md)):
- a bin of your own prefabs to drag in;
- pictures on faces, and painting straight onto the model;
- divide and push/pull;
- a starter set of prefabs (toggles, buttons, knobs, pipes...).

## Build

```
~/git/qb64pe/qb64pe -w -x bu1ld0r.bas -o bu1ld0r.run
```

## Using it

- **Put a shape down:** pick it on the left (or press 1-6), then click where it goes. It stands on the face you point at, standing out from it, or on the grid. You can also drag it straight from the bin. Shift keeps putting more down; Esc stops.
- **Select:** click a part (Shift adds it to the selection; Tab goes to the next).
- **Move:**
  - drag a part to move it across the ground (Shift: up and down);
  - arrows nudge it, and PgUp/PgDn raise and lower it;
  - R turns it 15 degrees;
  - = and - make it bigger or smaller.

  Moves snap to the grid (SNAP in the panel); hold Alt for none.
- **Exact numbers:** the panel on the right has the position, turn, size, slices (round shapes), the amount (a cone's top, a tube's hole, how much of a sphere) and the colour. Click a field and type (Enter), or turn the wheel over it.
- **The view:** right drag turns round it, middle drag (or Shift + right drag) pans, the wheel zooms, F frames the model, Home goes back to the start.
- **Edit:** Ctrl+Z undo, Ctrl+Y redo, Ctrl+D copy, Delete removes, Ctrl+A selects everything.
- **Files:**
  - Ctrl+S saves `models/NAME.bld` (the NAME box at the top);
  - Ctrl+O opens one;
  - Ctrl+N starts a new model;
  - Ctrl+E exports `export/NAME.obj`, `.mtl` and `_tex.png`.
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
bu1ld0r.run [FILE.bld] [--open NAME] [--export] [--neon DIR] [--shot FILE.png] [--quit]
```

`--export`, `--shot` and `--quit` act a few frames after start-up, for tests.
