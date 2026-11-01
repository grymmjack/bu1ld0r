---
name: c0nstruct0r
description: Rebuild a NEON-CASTER prop as a clean low-poly bu1ld0r model by driving bu1ld0r through its port (c0nstruct0r) - read the game's painting, plan the parts, build them with the port's commands, map the painting onto every face, check the eight game views and the report card. Use when Rick says "/c0nstruct0r NAME", "rebuild the PROP prop", "c0nstruct0r the PROP", or asks to work down the report card's list.
---

# c0nstruct0r: rebuild a prop

`/c0nstruct0r NAME` rebuilds the game's prop NAME (`~/git/neon-caster/neon-caster/hd/NAME.png`
is its painting; `models/NAME.obj` the model the game uses now) as a bu1ld0r model.
C0NSTRUCT0R.md has the plan, Rick's decisions and every port command. The goal is
deliberate shapes, not more triangles: symmetry where the painting has it, no gaps,
and pixels at a sensible size on every face (never a row of pixels smeared across a side).

## The tools

The c0nstruct0r MCP server (`.mcp.json`, `tools/c0nstruct0r/mcp_server.py`) gives:

- `bu1ld0r` - port commands, a line each (stops at the first `err`)
- `look` - a picture of the view, or `eight: true` for the game's eight views in one sheet
- `inspect` - `status` / `parts` / `faces` (JSON)
- `painting` - the game's painting, its subject's pixel box, the game's height, models.py's recipe, the budget; copied to `pictures/c0nstruct0r/NAME.png`; `grid: 32` overlays a grid to measure by
- `check` - the report card of `export/NAME.obj` next to the game's own

Without the MCP tools, the same works from the shell: `python3 tools/c0nstruct0r/rc.py -f steps.txt`
(or `rc.py CMD`), shots in `c0nstruct0r/shots/`, `python3 tools/c0nstruct0r/report.py --models export NAME`.

## Where it runs

- **Rehearse hidden first**, always: a copy of bu1ld0r on a hidden display (Xvfb `:98` -
  `:99` is Rick's DRAW QA, never touch it), the test copy at `/tmp/claude-1000/bu1ld0r-test/app`
  with `--port`, the steps at `pace 0`. MCP: start the server with `--dir` that folder, or use
  `rc.py --dir`. A step file that fails half way is fixed here, not on Rick's screen.
- **On Rick's screen only when he asks to watch.** Then: `cd ~/git/bu1ld0r && setsid nohup
  ./bu1ld0r.run --port &` (his normal display), wait for `c0nstruct0r.port`, run the
  rehearsed steps at `pace 400` with `say` lines he can read. Say in chat before it appears.
  Never kill bu1ld0r by name (Rick's own may be running); he closes the window himself.
- Esc on his side stops it ("err stopped"): stop sending, ask what he wants. F9 gives it back.

## Writing the steps

`tools/c0nstruct0r/stepgen.py` writes a step file from painting measurements, and
`tools/c0nstruct0r/props/recipes.py` holds a recipe per prop (add one there, then
`python3 tools/c0nstruct0r/props/recipes.py NAME`): `s.add(kind, px0, py0, px1, py1, d=..)`
(a part filling that pixel box - x 0 is the subject's middle, y 0 its foot),
`s.recess(p, px0, py0, px1, py1, depth)` (the front cut in there; a negative depth
raises it), `s.pics(p, front=RECT|None, back=True|COLOUR|RECT, side=RECT|COLOUR,
top=RECT|COLOUR)`. Measure on a 16-pixel grid of the painting (`painting NAME grid=16`).

## The method

1. **Read.** `painting NAME grid=32`: the subject box (W x H + left + top) gives the scale -
   the game's height (PROPS) / H pixels = cells a pixel. `check` / `report.py NAME` the game's
   model for its score to beat. Look at the game's own eight views if useful.
2. **Plan** in a step file (scratchpad): one `add` per visible block - boxes, wedges,
   cylinders - sized from pixel measurements times the scale. Centre the front on x = 0 and
   keep it symmetric unless the painting isn't. Write `say` lines that give the reason
   ("the deck slopes up 21 degrees, as the painting's control panel").
3. **No gaps.** Parts rest on each other: work out where a turned part's corners land
   (a shape turns round its foot's middle). A sloped slab over a flat top needs a wedge
   under it (`wedge`: full height at the back, sloping to the front's foot). Things standing
   on a slope sink into it a little rather than float.
4. **Detail** with the cheap moves: `edit P`, `pick facing 0 0 -1`, `inset 0.12`,
   `extrude -0.015` (a screen in a bezel); `mirror` for the other half; `done`.
5. **Pictures - one picture, the painting.** Export keeps a single picture pixel for pixel;
   several get packed 2x2 and shrunk, and `tile` repeats get cut into extra triangles. So
   map everything from `c0nstruct0r/NAME`:
   - fronts: `pick facing 0 0 -1 75` -> `picture c0nstruct0r/NAME view 0 X0 Y0 X1 Y1`
     with the subject box (X1 = left + W, Y1 = top + H) - each face gets the part in front of it;
   - sides: `pick facing 1 0 0` -> `view 90 RECT`, `pick facing -1 0 0` -> `view 270 RECT`,
     RECT a side-like strip of the painting (a panel column, about as tall as the prop);
   - back: `pick facing 0 0 1` -> `view 180 RECT` (a plain, darker region);
   - tops: `pick facing 0 1 0` -> `top RECT` (a region seen from above, front at its bottom);
   - pick a RECT whose shape is near the faces' (else SIZE / SMEAR suffer); a turned part's
     faces need a wider `facing` angle (`0 0 1 60`). A `pick` that finds nothing makes the next
     `picture` fail: only pick ways the part has.
6. **Check.** `look eight=true` against the painting; `fix` (the port command: the same report
   card inside bu1ld0r, no export needed - `ok score 25 smear 0 size 44.6 ...`); `export`; `check NAME`. Better than the
   game's score, within budget (1000 big / 200 small - C0NSTRUCT0R.md), every view sensible.
   Fix and run again (`new force` starts over: the step file is the model's source).
7. **Keep.** `save c0-NAME` (models/), `export` (export/ only). Into the game only when Rick
   says - then a scratch copy first (CLAUDE.md: never `--neon` the real game folder in a test).
8. **Clean up**: the hidden test copy and Xvfb `:98` (`pkill -f '^/tmp/claude-1000/bu1ld0r-test/app/bu1ld0r.run'`,
   `pkill -f '^Xvfb :98'`) - only those.

## Fixing: `/c0nstruct0r fix KIND` (sent by FIX THIS)

bu1ld0r's FIX THIS panel starts you with `claude -p` when Rick presses PICTURES, DETAIL or
REBUILD: the prompt says the fix, the parts (selected ones, or the whole model), Rick's own
words (they come first) and the findings. It's **Rick's model, already open** in bu1ld0r, on
his screen - not a prop to start from nothing:

- `take` first. Never `new`, `open`, `save` or `export` (a backup's made; Rick saves). Each
  change is an undo step he can step back through.
- `fix` gives the findings (`fix show smear` / `size` / `asym`... selects the parts carrying
  one: `inspect status` lists them); `inspect parts` / `faces` the rest. Keep to the parts
  you were given.
- The painting: `painting NAME` if the model is a prop (`c0-NAME`, or NAME a game prop's),
  else work from the pictures its faces already have (`inspect faces`: `pic`).
- **PICTURES**: the faces SMEAR / PIXEL SIZE / REPEATS flag mapped again - `edit P`, pick them,
  `picture REF view YAW RECT own` / `top RECT own` from a patch the face's shape and about
  the model's usual pixel size (FIX THIS's px/cell), one picture for all; a plain colour
  where the painting has nothing for it. `done`, `fix` again.
- **DETAIL**: the method's step 4 on flat slabs (inset + extrude, bevels) where the painting
  shows panels, screens, vents; map the new faces.
- **REBUILD**: the method from step 2 for the parts given (`del` them, `add` new ones in
  place), the rest left as they are.
- Esc on Rick's side ends you (your process is stopped): don't fight it.
- End: `fix` for the score, `give`, then two short lines - what you changed and the score
  before / after. bu1ld0r shows them in the panel.

## First rebuild: alarmpc (2026-11-01)

Five parts, 72 triangles, score 25 against the game's 64 (smear 45% -> 0%, asymmetry 19% -> 3%).
The first pass (three pictures, `tile` sides) scored 96: 760 triangles of tile cuts, the
small crops blown up 4-10x by the export's 2x2 packing, and the deck floating over the desk.
Its steps: desk box, riser wedge, deck box `rx=-21` with its front edge on the desk, monitor
bank sunk into the deck (inset + extrude -0.015 for the screens), foot box; every face mapped
from the painting (`view 0 13 37 243 256`; sides `view 90/270 36 156 70 240`; back
`view 180 172 156 222 240`; tops `top 128 64 200 108`).
