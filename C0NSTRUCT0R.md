# c0nstruct0r - plan

bu1ld0r's counterpart: Claude drives bu1ld0r, on Rick's screen where he can
watch, to rebuild NEON-CASTER's props (and later pixelmon's AI meshes) as
better low-poly models. Not Blender, and not more triangles: deliberate
shapes, symmetry where the painting has it, and pixels mapped at the right
size on every face. The model is Rick's own barrel rebuild
(`prefabs/barrel.bld`: one mesh, 206 faces, the game's barrel texture
reused).

Status: started 2026-11-01 on the `c0nstruct0r` branch. Stages 1 (the
report card, `tools/c0nstruct0r/report.py`), 2 (the port: UI/REMOTE,
`tools/c0nstruct0r/rc.py`) and 3 (the MCP server, the `/c0nstruct0r`
skill, alarmpc rebuilt on Rick's screen) done; stage 4 next.

## Why the props look the way they do

Nearly all of them aren't AI meshes. `neon-caster/neon-caster/models/models.py`
builds them from one front painting (`hd/NAME.png`):

- `extrude` traces the painting's outline on a 64 x 64 grid and pushes it
  back to one depth (optional `bands`: a top share at a depth of its own).
- `lathe` spins the outline round (barrels, tanks, lamps).

Each side, top and bottom face takes one row or column of pixels from a
little in from that edge (`INSET = 3`) and stretches it across the whole
depth: the stretched tops, sides and undersides. The outline follows the
grid's pixel steps, so the shape has no symmetry and no reason to its
angles. Rick's screenshot is `alarmpc`: `('extrude', 0.5, [(0.4, 0.2)])`.
Only the chair and the plant are pixelmon AI meshes (`models/src/*.gltf`,
`pixelmon --mesh NAME.png --lowpoly 250 --texture ...`).

## The three pieces

### 1. A remote-control port in bu1ld0r (the "devtools")

- bu1ld0r listens on a local port (127.0.0.1 only, QB64's `_OPENHOST`)
  and reads it once a frame. Off unless asked for (a flag / menu item).
- Commands are bu1ld0r's own operations: put down a shape, select, pick
  faces (e.g. "front faces of part 3", by direction / plane), extrude,
  inset, bevel, loop cut, mirror, put a picture on faces (a rectangle of
  the texture, at a given pixel size), save, export, and screenshots from
  the 8 game angles. Replies are plain text / JSON.
- It's watchable:
  - the camera moves to the part being worked on;
  - the picked faces flash before each change;
  - a strip at the bottom says what it's doing and why ("inset the
    screen 0.02: the painting shows a bezel");
  - a speed control (set before it starts); Esc stops it and hands the
    model back. While it runs, bu1ld0r ignores every other key and the
    mouse (see FIX THIS below).
- Every command is one undo step, so Ctrl+Z works afterwards as usual.
- Commands through a port rather than xdotool: exact, doesn't fight Rick
  for the mouse, works on any OS.

### 2. A small Python MCP server

Turns the port into tools for Claude: look (the 8 views next to the
original painting), inspect (parts, faces, sizes, how much of the texture
each face uses), build / edit, check (the report card), save / export.

### 3. A `/c0nstruct0r NAME` skill: the method

1. **Read** the painting, the current model's 8 views and its report
   card. Write a short build plan: parts, their sizes on the grid, the
   mirror line, which piece of the painting goes on which face.
2. **Block out** with boxes and cylinders on the 1/32 grid, as mirrored
   halves, matching the painting's front outline with a believable depth.
3. **Detail with low-poly moves**: inset + extrude for screens, panels,
   vents; a few bevels and loop cuts. A triangle budget per prop (the
   barrel is about 200).
4. **Pictures** at the same pixel size on every face, never a one-pixel
   smear:
   - front faces: their part of the painting;
   - sides and tops: a matching strip of the painting repeated (vents,
     panel lines), or a tile made from the painting's own colours (the
     painter's MAKE), or a new side / top painting from pixelmon in the
     same style.
5. **Check** the 8 views against the original, the report card, Rick's
   comments.
6. **Save** a `.bld` Rick can keep editing by hand; into the game only
   when he says (a scratch copy of the models folder until then).

### 4. FIX THIS: summoned from inside bu1ld0r (Rick's idea, 2026-11-01)

A button (and a key) in bu1ld0r that calls c0nstruct0r on the model
that's open, without leaving the program:

- It opens a small box: "What should I fix?" - empty means "the usual"
  (the report card's problems). If parts are selected, only those are
  worked on ("fix this" = this part).
- bu1ld0r turns its port on and starts Claude Code in the background
  (`claude -p "/c0nstruct0r ..."`, with the c0nstruct0r MCP server and
  `--allowedTools` limited to it, so it can only work through bu1ld0r).
  It uses Rick's own Claude Code sign-in.
- Before anything changes, the model is saved to a backup (and every
  step is an undo, as above), so FIX THIS can always be undone in full.
- While it works, the log strip shows its steps and reasons.
- **While a fix runs - or any time c0nstruct0r has control, however it
  was started (FIX THIS, or a Claude Code session through the port) -
  bu1ld0r ignores all input except Esc**: no keys,
  no clicks, no wheel, no orbiting, and even moving the mouse does
  nothing (no hover highlights, tips or pointer picking follow it) -
  nothing Rick does can collide with what it's doing. Esc is the one
  way to bail out: it ends the fix, or takes control back from the
  session (the port stops taking commands until Rick hands it back). Esc stops it at once and hands the model back as it
  is (the backup still there to go back to). Closing the window counts
  as Esc, then closes. The only exception to the lock is its own `ask`
  buttons, when it asks Rick something.
- It can ask Rick a question in the program: a line with buttons (yes /
  no / a few choices) through an `ask` command that waits for his click.
- When it's done: a short summary in the strip ("rebuilt the top band,
  mirrored, 412 triangles; the sides use the vent strip"), and the
  report card before and after.
- The button shows only where `claude` is installed (Linux first;
  Windows and macOS if Claude Code is there).

This comes after stage 3: it's the same server and skill, started by
bu1ld0r instead of from a Claude Code session.

**One button per problem**, so Rick decides exactly what gets touched.
The FIX THIS panel lists the report card's findings for the model (or
the selected parts), each with its count and its own button:

| Button | What it fixes | Who does it |
|---|---|---|
| PICTURES | stretched / smeared faces get a strip or tile at the right pixel size | Claude (choosing what goes where) |
| PIXEL SIZE | faces whose pixels are bigger or smaller than the rest, refitted | bu1ld0r alone |
| SYMMETRY | one side mirrored onto the other (Rick picks which side is right) | bu1ld0r alone |
| ANGLES | faces a few degrees off square, made square (as FLATTEN's `EdSquareN`) | bu1ld0r alone |
| TRIANGLES | over budget: tidied down to it | bu1ld0r alone (TIDY) |
| DETAIL | flat slabs given insets, extrusions, bevels from the painting | Claude |
| REBUILD | the whole thing (or the selection) rebuilt as in the method | Claude |

- "bu1ld0r alone" fixes are ordinary tools: instant, no Claude, no cost,
  usable without Claude Code installed. Only the judgement calls start
  Claude.
- Boundaries: the selection limits every fix; a part can be marked
  **LEAVE** (don't touch) and every fix skips it; the free-text box adds
  to a fix ("keep the screen as it is").
- Each fix is one undo step (a Claude fix: one backup, then its own
  steps), and its line in the panel shows before / after.

## The port's commands (stage 2)

bu1ld0r `--port`; `python3 tools/c0nstruct0r/rc.py CMD` (or `-f FILE`,
`-i`) talks to it. A line in, a line out: `ok ...` or `err why`. Control
belongs to the connection: it ends when the connection does.

| Command | Does |
|---|---|
| `hello TOKEN` | first, always (rc.py does it) |
| `help` | the commands |
| `take` / `give` | take the model (Rick's input locked out but Esc) / hand it back |
| `say TEXT` | the strip's words: what it's doing and why |
| `pace MS` | the pause after each change (250; 0 to 5000) |
| `status` | JSON: model, dirty, parts, triangles, control, stopped, edit (faces, points, picked), sel, undo, camera |
| `parts` | JSON: each part - kind, name, pos, size, turn, col, amt / seg, faces (mesh), hole, group |
| `faces [P]` | JSON: each face of a mesh part (the edited one) - f, way out n, middle c, area, corners k, col, pic, sel |
| `shot NAME [win \| clean]` | `c0nstruct0r/shots/NAME.png`: the view as shown / the window / the model alone |
| `new [force]`, `open NAME [force]` | (force: even if not saved) - NAME in models/, or `neon:PROP` |
| `save [NAME]`, `export` | save (models/); export to export/ only |
| `undo`, `redo` | as Ctrl+Z / Ctrl+Y |
| `add SHAPE [X Y Z [SX SY SZ [RX RY RZ]]] [key=value...]` | a part (its number back); keys `x y z sx sy sz rx ry rz col amt seg name hole keep hide group` |
| `set P key=value...` | change a part (all or nothing) |
| `del P...`, `sel none \| all \| P...` | delete; select |
| `look all \| P...` | camera turned to see them |
| `view YAW [PITCH [DIST]]` | camera: yaw 0 = the front (game picture f = yaw f x 45), pitch up + |
| `mesh P` | a shape made a mesh part |
| `mirror P [x \| y \| z] [at=V]` | a mirrored copy across the plane axis = V (its number back) |
| `edit P` / `done` | E on part P (made a mesh), faces mode, camera to it / E off |
| `pick [add] none \| all \| F... \| facing X Y Z [DEG]` | faces picked (facing: within DEG, 10, of that way) |
| `extrude D` | picked faces out D (negative: in) with sides |
| `inset K` | each picked face inset, corners K of the way to its middle |
| `push D`, `move DX DY DZ`, `scale K [KY KZ]` | picked faces (move: the selected parts, outside E) |
| `colour RRGGBB`, `flip` | picked faces' colour (selected parts', outside E); faces turned over |
| `picture REF fit \| tile N \| view YAW X0 Y0 X1 Y1 \| top X0 Y0 X1 Y1 \| none` | pictures/REF.png on the picked faces: stretched; repeated at N px a cell; seen from YAW with the model's box filling those pixels (a painting's part for each face); `top` the same from above, front at the bottom |

The MCP server (`tools/c0nstruct0r/mcp_server.py`) wraps these as tools:
`bu1ld0r` (lines of commands), `look` (`yaw` / `pitch` / `dist`, `how`,
`eight`), `inspect` (`status` / `parts` / `faces`), `painting` (NAME,
`grid`) and `check` (NAME, `against`).

## The report card

Plain Python on the OBJ files, no window. For each prop:

- **Stretch**: pixels across each face, each way - smeared faces flagged.
- **Symmetry**: how far the left half is from a mirror of the right.
- **Angles**: faces a few degrees off 0, 45 or 90.
- **Pixel size**: whether the pixel size matches from face to face.
- **Triangles**: the count against the budget.

Run over all ~50 props it ranks the worst first, and gives a before and
after for each rebuild.

## Stages

1. Report card and ranked list (no bu1ld0r changes; says where to start).
   Done 2026-11-01: `python3 tools/c0nstruct0r/report.py` (stdlib only;
   `--json F`, `--models DIR`, or names) grades every OBJ in the game's
   `models/`, worst first, in under 2 s. Columns: SMEAR (stretched 3:1 or
   more over pixels that differ - streaks), SIZE (pixels 1.5x off the
   prop's usual px/cell), ANGLE (0.75-8 degrees off square or 45), ASYM
   (front and top outlines against their mirror image), TRIS against the
   budget; COLOUR and PLAIN (stretched over one colour) shown, not
   scored. First run: extruded props are 40-65% smeared (their sides
   and tops); the worst are slugs, armor, turret, pickup-scatter, bench,
   turret-base, alarmpc; barrel-bot is 1547 / 600 triangles. Pickups'
   ASYM is high by nature (side views of guns): judge it on machines.
2. The bu1ld0r port: a first set of commands, the log strip, pause and
   take over. Done 2026-11-01 (UI/REMOTE; the commands above): tested on
   a hidden display - a box built, inset, recessed, a knob mirrored; keys,
   clicks and the wheel ignored while it holds the model (the same Delete
   deletes once it's given back); Esc / F9; a LAN address and a wrong
   token turned away; a dropped connection hands the model back. Developed and tested on the hidden test display (Xvfb /
   headless weston); on Rick's screen only when he starts it.
3. The MCP server and the skill; `alarmpc` the first rebuild, Rick
   watching. Done 2026-11-01: `tools/c0nstruct0r/mcp_server.py` (stdlib,
   stdio; `.mcp.json`) - tools `bu1ld0r` (commands), `look` (a shot, or
   the eight game views as one sheet), `inspect`, `painting` (the game's
   painting, its subject box, height, recipe, budget; a measuring grid),
   `check` (the report card against the game's); the skill
   `.claude/skills/c0nstruct0r`. alarmpc, run live on Rick's screen
   twice: the first pass (three pictures, `tile` sides) scored 96 - 760
   triangles of repeat cuts, small crops blown up by export's 2x2
   packing, the deck floating; the second (`tools/c0nstruct0r/props/alarmpc.txt`:
   a riser wedge under the deck, the monitors sunk into it, every face
   from the one painting with `view` / the new `top`) 72 triangles,
   score 25 against the game's 64 (smear 45% -> 0%, asymmetry 19% -> 3%;
   SIZE 45%: the sides' pixels are bigger than the front's).
4. Gaps as the rebuilds need them:
   - more commands;
   - `models.py` must skip props that have a hand-built model, or its
     `--write` overwrites them (NEON-CASTER's repo);
   - pixelmon side and top paintings.
5. Down the ranked list, one prop at a time, each approved by Rick.
6. FIX THIS: the panel in bu1ld0r, a button per problem, on the open
   model. Its bu1ld0r-alone fixes (PIXEL SIZE, SYMMETRY, ANGLES,
   TRIANGLES) and LEAVE need only the report card, so they can come any
   time after stage 1, before the Claude ones.

Later, pixelmon: its AI meshes (`--mesh`) as a see-through reference to
build a clean low-poly version over. bu1ld0r would need glTF import for
that, or pixelmon could write OBJ as well.

## Decisions (Rick, 2026-11-01)

- **Approval**: it builds straight from its written plan, shown in the
  strip; Rick can pause or stop it (Esc) any time.
- **Sides and tops**: strips and colour tiles from the painting first;
  pixelmon side paintings later.
- **Where it lives**: `tools/c0nstruct0r/` in this repo.
- **Budget**: by size - 1000 triangles for big props (machines,
  furniture), 200 for small ones (pickups, small items). (Big was 600
  at first; Rick raised it to 1000 on 2026-11-01.)
