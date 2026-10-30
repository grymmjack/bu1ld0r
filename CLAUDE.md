# bu1ld0r - notes for Claude

A 3D model builder in QB64PE (Rick's; started 2026-10-30 for NEON-CASTER's
props). PLAN.md has the stages; README.md the keys and files.

## Layout

`bu1ld0r.bas` (the loop) includes `_ALL.BI` / `_ALL.BM`; folders CORE (window,
input, helpers), MODEL (PARTS: the part list, .bld text, undo; PREFAB: the
prefab library, save as / edit a prefab; MESH: each shape as triangles),
VIEW (camera, the rasterizer, picking, outlines), UI (UI: panel, keys,
mouse, putting down, dragging; BIN: the bin - shapes, prefab folders,
thumbnails), OUT (OBJ + NEON-CASTER export). As NEON-CASTER: `.BI`
declarations, `.BM` routines, no GOSUB/GOTO, DIM every local.

## Gotchas met so far

- **QB64 names ignore case, and a local array can't share a shared one's
  name**: `DIM px(2)` in a SUB when `pX()` is shared is a runtime "Duplicate
  definition". A variable can't share a SUB's name either (`msg$` vs `Msg`),
  nor a FUNCTION another's with a different suffix (`IIF` / `IIF$`).
- **A FUNCTION's name read inside it is a call to it**: work in a local, assign at the end.
- **Colours through a SINGLE lose bits**: anything carrying an
  `_UNSIGNED LONG` colour is typed so (`IIFC~&`, not `IIF`).
- **Keys**: Ctrl/Shift/Alt are followed through `_KEYHIT`'s own queue
  (`qCtrl`...: they come as 100305/-100305...), so a quick Ctrl+S from xdotool
  still counts; `CtrlIs` also takes the control code (Ctrl+S = 19).
- No DATA in SUBs: lists are built in code (`Words`, `HelpAdd`).
- `base` is a reserved word (OPTION BASE): not a parameter name.
- **The window** (as DRAW): our screen is `scrW x scrH` (no CONST size),
  shown `uiK` times bigger with `_RESIZE ON , _STRETCH` - QB64PE maps the
  mouse back to our pixels. A settled drag remakes the SCREEN (`ScreenSet`,
  `Layout`) and sets the window with `CORE/winsize.h`. A new SCREEN snaps
  the window to its own size first: WindowFrame sees that echo (a resize to
  `scrW x scrH`) and sets it back. `rZ`/`rId` grow as needed (`RCap`). Test
  on a 3840x2160 Xvfb to see 2x (Rick's display).
- `pkill -f 'Xvfb :99'` kills the shell running it (its own command line
  matches): `pgrep -x Xvfb | xargs -r kill`.
- `_FILES$` is one iterator: list a folder's names first, then recurse
  (`PfLoadAll`). Folders come back with a trailing `/`, plus `./` `../`.

## How it draws

Software, in BASIC (`RasterTri` / `FillTri`): `rZ` a depth buffer (q bigger
is nearer: 1/z, or 1000 - depth flat), `rId` the triangle per pixel - picking
is `rId` at the pointer, and `tPart`/`tFace` say which part and face. The
ghost (part 0, the shape being put down) is drawn see-through and kept out of
`rId`, so picking sees through it. Anything else drawn with RenderBegin (bin
icons, export pictures) overwrites rId: set `viewDirty` after.

Shapes are 1 x 1 x 1 on their own foot (x, z -0.5..0.5, y 0..1), sized
(the box they fill), turned Z then X then Y (`XformRot`), placed. `MkTri`
takes an outward hint and winds each triangle anticlockwise from outside
(OBJ's way - checked against the game's crate.obj).

## Prefabs

A prefab is `prefabs/[FOLDER/]NAME.bld`; a model uses one as a part of kind
`K_USE` (`pRef$` its name, its size its scale; `.bld`: `use NAME x y z
turns scales`). Linked: the library (`PfLoadAll`, at start and after any
prefab save) reads every prefab's parts into the same part arrays after the
model's (`PF_BASE + 1` on); `PfFind` maps a name to it (or to the one
prefab of that base name, if it moved). `MeshItem` makes a use's parts with
the use's place/turn/scale pushed on a stack (`usN`, up to 8: XformPt and
XformHint apply it), all counted as the use's part, so picking, outlines,
drag, undo and export work unchanged. `mdlPf$` = the prefab open (Ctrl+S
saves there); `PfLoops` / `ModelUses` stop a prefab going in itself.
Prefab thumbnails are made in `BinIconsDue` at the end of UiFrame (before
the view is drawn: RenderIcon uses part 0 and rId).

## Export (NEON-CASTER)

As models.py: OBJ y up, front -z, `# frame F` (max of 2 x reach and
height, x 1.04), one texture (each colour an 8th-square block), 8 pictures
at 64 px drawn 4x and shrunk, lit `eye*.55 + up*.8 - right*.35`, shade
`.72 + .45 x lit`, see-through below half coverage. Picture f's eye is
(sin f45, 0, -cos f45). The game's models share MAX_MDL_TRIS (16,000).

## Build

`~/git/qb64pe/qb64pe -w -x bu1ld0r.bas -o bu1ld0r.run` - check it by its
`Output:` line (grep `Output:|in use|LINE|Caused`): QB64PE reports most
mistakes as `Name already in use` plus a `LINE nnnn:`, not "error".

## Testing

Never on Rick's display: Xvfb `:99` (start it, `xdpyinfo` first), WAYLAND
unset, `QT_QPA_PLATFORM=xcb` (QB64's error boxes go to the Wayland desktop
otherwise), `PULSE_SINK=claude_mute`. `tools/test/run.sh ARGS` does all
that, from a copy in `/tmp/claude-1000/bu1ld0r-test`; `source
tools/test/drv.sh` then `win` gives xdotool helpers (`clk`, `drag`, `key`,
`typ`, `shot NAME`) on the program's own window. `--open NAME --export
--neon DIR --shot F.png --quit` checks with no input. `tools/test/wind.py
X.obj` counts triangles wound outward/inward.
Never `--neon` the real game folder in a test (use a scratch copy of
`neon-caster/models` and `hd/models`). No GUI launches from subagents. Run
long tests in the background, one at a time (`nice`, `LP_NUM_THREADS=2`).
Clean up after: `ps -eo pid,etime,args | grep -E 'bu1ld0r|Xvfb'`.

## Git

Commit or push only when Rick asks. Remote: github.com/grymmjack/bu1ld0r
(public), branch main - first commit 2026-10-30 (stage 1).
