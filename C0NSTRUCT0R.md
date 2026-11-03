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
skill, alarmpc rebuilt on Rick's screen) done; 21 props rebuilt (stage 5);
FIX THIS (stage 6) built, both halves, and `ask`.

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

**Built (2026-11-01): the panel and its bu1ld0r-alone fixes** (UI/FIX;
F2, or FIX in the top bar). The checks are report.py's, run on what
EXPORT makes (hidden parts too, tidied if it's to be), so the SCORE is the
report card's: the game's alarmpc 64, c0-alarmpc 25, in both. Each row has
SHOW (selects the parts carrying it) and LEAVE (out of the score; saved
in the .bld as `fixleave asym ...`). What changed from the table above:

- SMEAR got a bu1ld0r-alone fix, **MAKE PLAIN**: each smeared face its
  pixels' average colour (the game's bench: 84 -> 21). Re-mapping it from
  the painting stays Claude's (PICTURES).
- PIXEL SIZE has **no** bu1ld0r-alone fix: refitting a face's spots shows
  a different piece of the picture, a judgement - it goes with PICTURES.
- SYMMETRY: **KEEP L / KEEP R** (as seen from the front; the mirror at
  x = 0 if the model's across it, else its middle). The other side's parts
  go, this side's are mirrored (`PartMirror&`, as the port's `mirror`), and
  a part across the middle that's off its own mirror (its outline, or a
  box with no twin) is cut there and rebuilt from its kept half and that
  half mirrored (`FxHalfMesh&`) - what an imported game prop needs, one
  mesh: the bench's asymmetry 21% -> 0, no seam.
- ANGLES: **SQUARE UP** snaps turns 0.75-8 degrees off a multiple of 45,
  then puts each face still that far off onto its nice way's plane (24
  passes, shared points agree; a shape made a mesh first). A face meeting a
  neighbour at 0.5-20 degrees is a round thing's facet: left, and no longer
  counted - in report.py too (its docstring always said so; no score here
  changed).
- TRIANGLES: **TIDY** turns EXPORT: TIDIED on with the report card's
  budget (1000).
- PICTURES and REPEATS are shown (what EXPORT packs 2x2 or cuts), not
  scored - as report.py.
- The port: `fix [check | open | close | plain | square | keep left | keep
  right | tidy | show W | leave W]` answers with every number
  (`ok score 25 smear 0 size 44.6 ...`).

**Built (2026-11-01): the Claude half.** ASK CLAUDE in the panel (shown
where `claude` and `tools/c0nstruct0r/` + `.mcp.json` are beside bu1ld0r):
the "What should I fix?" field (`F_FIXASK`), PICTURES / DETAIL / REBUILD.
`FxClaude` opens the port if it's shut, writes the model to
`c0nstruct0r/backup/NAME-DATE.bld`, the prompt to `c0nstruct0r/fix-prompt.txt`
(`/c0nstruct0r fix KIND`, the parts, Rick's words, the findings) and runs
`c0nstruct0r/fix-run.sh`: `claude -p --mcp-config .mcp.json
--strict-mcp-config --allowedTools mcp__c0nstruct0r` (no Bash, no file
edits: bu1ld0r through the port only), its output in `fix-out.txt`, its pid
in `fix-pid.txt`, its exit code in `fix-done.txt` - polled each second
(`FxRunPoll`): the score before -> after and its last two lines in the
panel. Esc kills it (`FxClaudeStop`). The skill's "Fixing" section is what
it follows. First runs (hidden): a no-change plumbing test, then c0-console
PICTURES 25 -> 3 in ~4 minutes (the cabinet sides re-mapped from a cabinet
patch at the front's pixel size; beacon and antenna plain colours); Esc
mid-run stopped it at once.

`ask QUESTION | ANSWER | ANSWER...` (built 2026-11-01): a box over the strip,
the question and a button per answer (yes / no when none are given, up to
four); the one click let through the lock. The reply waits for Rick:
`ok ANSWER`, or `err stopped` if he presses Esc instead (rc.py waits with
no timeout on an `ask` line). The downloads carry the c0nstruct0r tools,
the skill and `.mcp.json` (build-release.yml), so ASK CLAUDE works from
an unzipped bu1ld0r with Claude Code installed (Linux / macOS).

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
| `ask QUESTION [\| ANSWER \| ANSWER...]` | asks Rick, buttons on the view (yes / no by default, up to four): `ok ANSWER` once he clicks, `err stopped` on Esc |
| `fix [check \| open \| close \| plain \| square \| keep left \| keep right \| tidy \| show W \| leave W]` | FIX THIS: the report card on the model (`ok score S smear ...`), its panel, a fix, SHOW / LEAVE a finding (W: smear size angle asym tris pics repeats) |
| `edit P` / `done` | E on part P (made a mesh), faces mode, camera to it / E off |
| `pick [add] none \| all \| F... \| facing X Y Z [DEG]` | faces picked (facing: within DEG, 10, of that way) |
| `extrude D` | picked faces out D (negative: in) with sides |
| `inset K` | each picked face inset, corners K of the way to its middle |
| `push D`, `move DX DY DZ`, `scale K [KY KZ]` | picked faces (move: the selected parts, outside E) |
| `colour RRGGBB`, `flip` | picked faces' colour (selected parts', outside E); faces turned over |
| `picture REF fit \| tile N \| view YAW X0 Y0 X1 Y1 [own] \| top X0 Y0 X1 Y1 [own] \| none` | pictures/REF.png on the picked faces: stretched; repeated at N px a cell; seen from YAW with the model's box filling those pixels (a painting's part for each face; X0 > X1 mirrors); `top` the same from above, front at the bottom; `own`: the edited part's box instead of the model's |

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
   time after stage 1, before the Claude ones. The panel and its
   bu1ld0r-alone fixes done 2026-11-01 (see *Built* under FIX THIS above);
   the Claude ones next.

Later, pixelmon: its AI meshes (`--mesh`) as a see-through reference to
build a clean low-poly version over. bu1ld0r would need glTF import for
that, or pixelmon could write OBJ as well.

## Rebuilt

Each prop's steps are `tools/c0nstruct0r/props/NAME.txt` (its painting in
`pictures/c0nstruct0r/`), its model `models/c0-NAME.bld`; exported to
bu1ld0r's `export/` only. SCORE: higher is worse.

| Prop | Parts | Triangles | Score | The game's | Notes |
|---|---|---|---|---|---|
| alarmpc | 5 | 72 | 25 | 64 (186 tris) | desk, riser wedge, sloped deck, monitor bank (screens inset), foot box |
| bench | 10 | 120 | 28 | 84 | slab on four legs, pad, toolbox with a handle; the top plain dark (the painting shows only its edge) |
| generator | 7 | 244 | 23 | 61 | cabinet with the window inset and set back, three coils, pins |
| desk | 11 | 172 | 22 | 61 | top, legs, drawer unit, back panel, monitor (screen inset), mug, clutter |
| labbench | 15 | 396 | 23 | 57 | cabinet, worktop, microscope stand, round and cone flasks, rack |
| chest | 7 | 84 | 1 | 58 | body, lid, handle on two posts, two latches; painted three-quarter, so each face takes its own patch (front, left side - mirrored for the right -, lid top) |
| mimic-asleep | 7 | 84 | 1 | 58 | chest's steps on its own painting (pink glow) |
| chest-open | 4 | 48 | 14 | 59 | body, gem heap, lid open and leaning back (its inside the painting's, its outside the body's panels), latch |
| safe-open | 3 | 52 | 13 | 61 | plinth, cabinet with the open compartment cut in (inset, scale, move, pushed in 0.24: the shelves on its back wall), handle |
| lamp | 5 | 224 | 32 | 58 | base disc, pole, socket, bulb, drum shade - one axis; each round part from its own patch inside its outline |
| cryopod | 2 | 72 | 6 | 56 | the pod (front inset and pushed in 0.26: the hollow), the sleeper standing in it; the pod's outside its own blue |
| tank | 6 | 168 | 27 | 54 | drum, neck and lid, four feet; tops orange (the painting's) |
| crate | 2 | 24 | 0 | 54 | box and lid band, each face its own patch inside the rounded outline; the lid top its planks |
| locker | 3 | 84 | 15 | 54 | three lockers, vents pressed in; the ends a slice of a door |
| vending | 8 | 100 | 5 | 53 | body (snack window set in), cap, keypad, four feet; sides pink / silver as its edge |
| bookshelf | 5 | 76 | 4 | 52 | frame cut in deep (books on the back wall), four boards in front of them |
| safe | 1 | 28 | 2 | 52 | body, the inside cut in 0.14 (ring and drawer on its back wall) |
| terminal | 2 | 56 | 23 | 42 | keyboard unit (keys raised), screen unit set back (screen set in) |
| terminal-broken | 2 | 40 | 15 | 50 | monitor (screen set in), keyboard lying in front |
| console | 5 | 160 | 25 | 43 | cabinet, deck, beacon on a post with an antenna |
| rack | 5 | 76 | 3 | 42 | frame cut in deep (the lights inside), four feet |

From crate on, the steps come from `tools/c0nstruct0r/props/recipes.py`
(`python3 tools/c0nstruct0r/props/recipes.py [NAME]` writes NAME.txt) on
`tools/c0nstruct0r/stepgen.py`: parts as pixel boxes of the painting,
`recess` (inset, shrink and move to a pixel box, push in or out), `pics`
(front as seen or a patch, back mirrored / a colour, sides and top a patch
or a colour).

Learned on the way:
- `own` (the part's box, not the model's) for sides and tops: each part's
  sides take its own piece of the painting; mapped over the whole model a
  side took whatever was at that height (see-through, or the next part's).
- A top the painting never shows (a bench's, a desk's) is a plain colour,
  not a row of pixels smeared across it.
- The back is the front mirrored (`view 180 X1 Y0 X0 Y1`), so it lines up
  with the parts behind it.
- A three-quarter painting (front, side and top all showing): the true
  width is more than the front patch looks; patches kept inside the solid
  pixels (a slanted edge's see-through pixels cut holes at the corners).
- A heights helper that subtracts the wrong way gives negative sizes:
  inside-out parts that vanish - check `add` lines for a negative size.
- Round things (cylinders, spheres, cones): front half `view 0` (facing
  0 0 -1 90), back half `view 180`.
- A cylinder mapped from the front takes the painting's outline columns
  at its sides: map it over its own box onto a patch inside the outline
  (else the rounded-off corners come out as holes). What's left of SMEAR
  on round parts is the sides near +-x, where the painting has few columns.
- An export bug it found: a spot on the picture's bottom edge (v = 1)
  counted as repeating past it, so every export of a prop whose painting
  reaches the bottom row was packed 2x2 and its pixels halved
  (`ExMarkUsed`, fixed).

## New models (m0d3l)

`/m0d3l THING` (.claude/skills/m0d3l) makes a prop that doesn't exist yet: shape designed,
textures painted by pixelmon (materials) with structure drawn by code into one picture, mapped
face by face (`tools/c0nstruct0r/m0d3l.py wrap`), materials, live on Rick's screen. Each model's
sources in `tools/c0nstruct0r/m0d3l/NAME/`.

| Model | Parts | Triangles | Score | Notes |
|---|---|---|---|---|
| c0-barrel | 10 | 608 | 17 (the game's barrel 41) | bulging drum (extrude + scale bands), four iron hoops, sunk lid, bung, side canister; pixelmon wood / lid / iron; wood, iron, metal materials |
| c0-crate | 10 | 120 | 0 in bu1ld0r, 5 exported (the game's crate 54) | Raiders-style shipping crate: body, two bands, four posts, three lid cleats - all boxes; pixelmon pine (juggernautXL, heun, karras), stencils drawn in code, 512 picture laid out at 256; one pine material |
| c0-medkit | 27 | 356 | 0 in bu1ld0r and exported (the game's medkit 39) | canteen-sized white crew kit: body with a recessed red panel, raised cross (a bar and two stubs), rails stopping at the lid seam, over-centre latches, handle, feet; one glossy material. In the game as `medkit` (2026-11-01) |
| c0-bigmed | 22 | 280 | 0 in bu1ld0r and exported (against the game's medkit, 39) | tackle-box-sized red trauma kit: tray, lid with a raised panel, hinges, latches, handle, feet, raised crosses front and ends; felt box, bright steel crosses / hardware, matte iron handle (three materials: 170 px/cell exported). Mapped live with the camera turning to each side (`bigmed/`, `paint.py`, `boxmap.py`). In the game as `bigmed` (2026-11-01) |

## Decisions (Rick, 2026-11-01)

- **Approval**: it builds straight from its written plan, shown in the
  strip; Rick can pause or stop it (Esc) any time.
- **Sides and tops**: strips and colour tiles from the painting first;
  pixelmon side paintings later.
- **Where it lives**: `tools/c0nstruct0r/` in this repo.
- **Budget**: 1000 triangles for every prop, small ones too. (It was
  600 for big props and 200 for small ones at first; Rick raised it to
  1000, then dropped the small budget: "1000 is fine", 2026-11-01.)

## m0d3l overnight (2026-11-01): staged in export/neon-stage/, not installed

| Model | Notes |
|---|---|
| c0-vending | 10 boxes, 140 tris, score 8 exported (the game's 53): plinth with the delivery bin cut in, body with a deep snack window, keypad, card reader, lit sign cap, cyan feet; one paint material |
| c0-locker | 7 boxes, 132 tris, score 2 exported (the game's 54): three lockers (blue, grey, blue), doors raised from their frames, vents, name cards, numbers, steel handles, kick base; plain faces shared so 247 px/cell |
| c0-terminal | 4 boxes, 64 tris, score 0 exported (the game's 42): tan base deck (drive bays, status display), green-key keyboard and keypad on it, monitor housing with the green CRT set in (text, scanlines), vents, label |
| c0-terminal-broken | 6 boxes, 88 tris, score 4 exported (the game's 50): scorched dark CRT on a stand, carry handle, the screen cracked and glitching pink / cyan (ERR / SIGNAL LOST), torn cables, keyboard missing keys |
| c0-console | 10 parts, 156 tris, score 1 exported (the game's 43): slate cabinet with a door panel, deck with three raised buttons and a cyan light strip, instrument hood with radar and data screens set in, red beacon dome (round, wrapped) on a post with an antenna |
| c0-alarmpc | 7 parts, 116 tris, score 0 exported (the game's 64): two pedestals with module slots, desk slab with a cyan edge, underpanel of cyan light bars, raised control deck of glowing red / cyan keys, monitor bank with six camera feeds and an ALERT set in, red joystick |
| c0-desk | 13 parts, 164 tris, score 27 exported, all of it asymmetry - drawers on one side (the game's 61): wood top with papers, steel legs, three-drawer unit, modesty panel, monitor of green mail on a stand, keyboard, red mug |
| c0-chair | 13 parts, 204 tris, score 2 exported (the game's models.py chair 11): stitched black leather seat and back with raised quilted cushions, armrests on posts, steel gas lift (round), four-arm base on casters |
| c0-table-flipped | 14 boxes, 144 tris, score 0 exported (the game's models.py one 33): the top standing up with two cyan panel inlays and orange trim, underside with magenta pads, a rim, four legs out with braces and rubber feet |
| c0-bench | 9 boxes, 96 tris, score 15 exported, all asymmetry - the toolbox sits to one side (the game's 84): stitched red leather slab with brass studs, dark legs, grey headrest pad, red toolbox with latches, name plate and a steel handle |
| c0-labbench | 14 parts, 264 tris, score 9 exported (the game's 57): steel cabinet of drawers A B C, resin worktop, microscope (steel pillar and arm, green head), round red flask and conical green flask with glass necks (round, wrapped), a rack with a small orange flask |
| c0-bookshelf | 15 boxes, 168 tris, score 0 exported (the game's 52): dark metal frame - sides with pink edge lights, a back, six boards - and five rows of books (spines of every height and colour, gold bands, fallen books, glowing cyan / pink data-slates) |
| c0-rack | 5 parts, 76 tris, score 0 exported (the game's 42): grey cabinet on rubber feet, a deep mesh window onto 24 glowing fans (cyan rings, yellow hubs, a few dead), orange drive bays, vents top and sides, a door handle |
| c0-safe | 11 parts, 88 tris, score 2 exported (the game's 52): charcoal safe on a plinth, bolted armour posts with VAULT 7 flank plates, sunk door with a glowing cyan ring lock, keypad, status lights, strip light, deposit drawer |
| c0-safe-open | 25 parts, 220 tris, score 2 exported (the game's 61): c0-safe looted (the game swaps it in) - split vault doors swung open with bolt mechanisms, a lit cave: a shelf of cash bundles, a data case, gold bars |
| c0-chest | 16 parts, 132 tris, score 0 exported (the game's 58): black armoured chest on a skirt, steel corner guards, glowing cyan strips, lid with carry handle, a lock light across the seam, side grips (one spec makes chest / mimic / open) |
| c0-chest-open | c0-chest with the lid stood up at the back (a lit blue circuit inside), heaped with glowing gems and loose gem cubes; 208 tris, score 0 (the game's 59) |
| c0-mimic-asleep | c0-chest exactly, but the lock glows red - the mimic's only tell; score 0 (the game's 58) |
| c0-cryopod | 16 parts, 248 tris, score 0 exported (the game's 48): white panelled round pod on a cyan-rimmed plinth, a frosted ice-blue window wrapped round the front with a faint sleeper, bubbles, coolant pipes and clamps down both sides, capped top with a status light |
| c0-generator | 11 parts, 220 tris, score 3 exported (the game's 61): riveted grey unit on a hazard-striped skid, sunk furnace window with bars over a glowing orange core, amber lamp, side vents, three insulator coils in orange and blue windings with dark caps |
| c0-tank | 9 parts, 268 tris, score 4 exported (the game's 53): round drum of riveted grey armour plates on four dark feet, a badge with an orange arrow at the front, orange sloped shoulder with bolt slots, dark neck, glowing orange filler lid |
| c0-lamp | 16 parts, 248 tris, score 18 exported (the game's 58; asym 16, the game's 13): retro floor lamp, pink-red base and pole with facet highlights, cyan neck, cyan drum shade lit warm from inside (from below a glowing bulb), two pull chains |
| c0-plant | 11 parts, 316 tris, score 9 exported (the game's 17): terracotta pot with a rolled rim and dark soil, forked brown trunk, four low-poly leaf clumps (spheres, painted leaves; m0kit now wraps spheres and maps their tops from above) |
| c0-screens | 4 parts, 64 tris, score 0 exported (the game's 23): monitor wall on a post and foot, dark bezel round six sunk displays - green radar with sweep and blips, blue grid scope, cyan target lock, purple waveform, orange core readout, red bar graphs - scan lines, a vented housing behind |
| c0-camera | 5 parts, 92 tris, score 6 exported (the game's 38): security camera on a round foot, post and knuckle, charcoal housing with red trim, fins and a recording light, sun hood, red-eyed lens out the front, cable gland behind |
| c0-alarm | 6 parts, 72 tris, score 5 exported (the game's 23): red wall box in a yellow safety frame with circuit lines, a pipe run, a brushed face plate, a big red push button, key switch, warning lamp, PUSH IN EMERGENCY label, grey back plate |
| c0-alarm-off | c0-alarm switched off (build.py off): button and lamp dark, the red and yellow dimmed; score 5 (the game's 23) |
| c0-core | 2 parts, 42 tris, score 1 exported (the game's 29): cyan crystal cut as a gem (6 sides, a small table, a point below), lit from inside (a soft glow material), a bright collar at the girdle (m0kit maps diamonds: crown from above, pavilion wrapped) |
| c0-specimen | 4 parts, 176 tris, score 0 exported (the game's 33): dark steel base with a status light, round tank of glowing green fluid with a spiny creature floating at the front, bubbles, light strips down the glass, bolted cap and green filler ring |
| c0-spawner | 8 parts, 100 tris, score 0 exported (the game's 13): sandstone frame on edge (rounded corners drawn), sunk well with a pink energy ring and four brackets, raised glowing cyan core, cyan arrows pointing out on all four sides, dark back plate |
| c0-plate | 7 parts, 72 tris, slit light on the muzzle corner (the game lights it; needed the export fix in OUT/EXPORT.BM), score 0 exported (the game's 23): the PLATE trap's pressure plate - low steel slab, diamond tread top in a hazard-striped border, red sensor strip and two buttons on each edge, rubber corner feet |
| c0-ammo | 9 parts, 252 tris, score 2 exported (the game's 38): three glowing cyan energy cells side by side, dark bands, steel caps with brass contacts |
| c0-shells | 2 parts, 40 tris, score 0 (the game's 46): orange shell box open at the front, two rows of shotgun shells end on (brass heads, primers), 12 GA label on top |
| c0-rounds | 13 parts, 236 tris, score 0 (the game's 56): olive ammo can with a lid and handle, 7.62 MM stencil, five brass rounds with lime tips standing on top |
| c0-slugs | 11 parts, 212 tris, score 0 (the game's 107): steel clip of five glowing blue slugs with pointed steel heads |
| c0-rockets | 9 parts, 236 tris, score 0 (the game's 68): dark riveted crate with an HE-RKT stencil, four red warheads on orange-banded bodies standing out of the top |
| c0-rocket | 5 parts, 132 tris, score 6 exported (the game's 45): the flying rocket, centred on 0 0 0 with its nose at -z like the game's - grey tube with an orange band, red nose cone, crossed dark fins, a nozzle glowing orange (turned cylinders: m0kit maps them triplanar now) |
| c0-armor | 17 parts, 168 tris, score 7 (the game's 78): standing power armour - blue plates, red trim, boots and gloves, glowing orange chest core, shoulder pads, visored helmet |
| c0-amp | 3 parts, 208 tris, score 5 (the game's 49): round red flask with a cyan lightning bolt on the front and glowing studs, steel neck, dark cap with a red glowing top |
| c0-overcharge | 6 parts, 168 tris, score 0 (the game's 16): bronze medallion on edge - engraved rim with ticks, four studs, a raised cyan crystal face of glowing facets |
| c0-invuln | 4 parts, 144 tris, score 0 (the game's 21): gold medallion on edge - bronze rim, rayed gold disc, a raised gold shield with an orange-glowing emblem, white crest on top |
| c0-goggles | 5 parts, 156 tris, score 0 exported (the game's 47): night-vision goggles - dark rubber housing, three lens tubes (turned cylinders) glowing green, head strap |
| c0-suit | 13 parts, 144 tris, score 6 (the game's 49): yellow hazmat suit standing - hood and gas mask with a green visor and filter, zip, reflective tape, badge, black belt, gloves and boots |
| c0-jetpack | 13 parts, 300 tris, score 3 (the game's 48): two orange tanks with hazard bands and a gauge each on a dark harness plate, steel caps, nozzles glowing at their mouths, shoulder straps |
| c0-jetfuel | 5 parts, 92 tris, score 11 (the game's 51; asym 11 is the cap and handle side by side): orange canister with black hazard bands, a gauge reading 31, steel filler cap, carry handle |
| c0-keycard | 2 parts, 24 tris, score 0 (the game's 16): access card in greys (the game tints it red / blue / yellow by brightness) - clip slot, chip, stripe, ACCESS, magnetic strip behind, a clip |
| c0-map | map: parchment sheet on edge with woods, rooms, river, road, folds, an X; blue gem pin; score 0 (game 17) |
| c0-repairkit | repairkit: open dark case, tool tray (wrench, drivers, cyan meter), lid with tool loops and cyan strip, latches; score 0 (game 66) |
| c0-pickup-rail | pickup-rail: dark green rifle of 11 boxes (stripe, rail, green-lens scope, skeleton stock); score 32 = asymmetry, a gun's own (game 47) |
| c0-pickup-repeater | pickup-repeater: green SMG, ribbed wooden magazine, sight, flash hider; score 30 = asymmetry (game 69) |
| c0-pickup-rocket | pickup-rocket: banded tube (turned cylinders along x), magenta muzzle round a glowing core, twin top tubes, mount, wheels; tube 0.13 deep (game 0.11); score 17 (game 42) |
| c0-pickup-scatter | pickup-scatter: orange shotgun leaning 35 deg as its painting (boxes laid out along the gun, turned); score 76 = asymmetry of a leaning gun (game 83) |
| c0-barrel-acid | barrel-acid: yellow steel drum, hoops, radiation sign, lid with bung, a tap (barrels.py: one spec for all ten); score 3 (game 38) |
| c0-barrel-lava | barrel-lava: bulging charred-stave drum (three drums, steps under hoops), orange hoops, glowing cracks, green porthole, plank lid; score 2 (game 36) |
| c0-barrel-poison | barrel-poison: bulging purple drum with a cage of ribs and a skull; score 2 (game 40) |
| c0-barrel-slime | barrel-slime: grey steel drum brimming with green slime running down it, red biohazard label; score 2 (game 42) |
| c0-barrel-water | barrel-water: teal drum, hoops, white drop, a scratch, lid with bung; score 2 (game 32) |
| c0-barrel-acid-wreck | barrel-acid-wreck: the drum's bottom 0.25 with its sign, a torn crown of 16 plates (stubs and spikes) glowing at the tops, the liquid's surface inside, runs down the outside; score 3 (game 5) |
| c0-barrel-lava-wreck | barrel-lava-wreck: the drum's bottom 0.25 with its sign, a torn crown of 16 plates (stubs and spikes) glowing at the tops, the liquid's surface inside, runs down the outside; score 2 (game 29) |
| c0-barrel-poison-wreck | barrel-poison-wreck: the drum's bottom 0.25 with its sign, a torn crown of 16 plates (stubs and spikes) glowing at the tops, the liquid's surface inside, runs down the outside; score 3 (game 29) |
| c0-barrel-slime-wreck | barrel-slime-wreck: the drum's bottom 0.25 with its sign, a torn crown of 16 plates (stubs and spikes) glowing at the tops, the liquid's surface inside, runs down the outside; score 4 (game 41) |
| c0-barrel-water-wreck | barrel-water-wreck: the drum's bottom 0.25 with its sign, a torn crown of 16 plates (stubs and spikes) glowing at the tops, the liquid's surface inside, runs down the outside; score 4 (game 31) |
| c0-turret-base | turret-base: grey tripod (three legs turned round y, rubber pads), dark hub, banded pedestal, hazard collar - 0.17 high, the head's pivot its top; score 0 (game 73) |
| c0-turret-head | turret-head: hazard-yellow armoured box, big blue lens, red light pods, two barrels in shrouds (ends from the white muzzle corner: 6 triangles each, middles at x +-0.105 y 0.105 z -0.23), sensor stack with red eyes; origin at the pivot; score 1 (game 56) |
| c0-turret | turret: base + head together (head at the pivot, 0.17), 0.43 x 0.53 x 0.46; muzzles from the white corner as the head's; score 4 (game 88) |
| c0-turret-mount | turret-mount: hex plate (seg 6 turned 90: corners at +-z, as the game's), bolts, hazard stripe; score 2 (game 2) |
| c0-turret-mount-broken | turret-mount-broken: the plate with a charred ragged hole painted (glowing torn edge), a charred pit under it, four torn wires; score 9 (game 35) |
| c0-sweep | sweep: labbench rebuilt (colour 0 now; score 9 = the microscope on one side, game 57); every model folder's export is in export/neon-stage/ (69 OBJs: all the game's models but barrel and crate, done before tonight, barrel-bot, left for Rick, and untitled, skipped) |
