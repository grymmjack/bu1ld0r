# bu1ld0r - notes for Claude

A 3D model builder in QB64PE (Rick's; started 2026-10-30 for NEON-CASTER's
props). PLAN.md has the stages; README.md the keys and files.

## Layout

`bu1ld0r.bas` (the loop) includes `_ALL.BI` / `_ALL.BM`; folders CORE (window,
input, helpers), MODEL (PARTS: the part list, .bld text, undo; PREFAB: the
prefab library, save as / edit a prefab; MESH: each shape as triangles,
holes cut; CSG: one solid less another), VIEW (camera, the rasterizer,
picking, outlines), UI (UI: panel, keys, mouse, putting down, dragging;
BIN: the bin - shapes, prefab folders, thumbnails; LIST: the parts list),
OUT (OBJ + NEON-CASTER export). As NEON-CASTER: `.BI`
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
- `base`, `list`, `out` are reserved words (OPTION BASE, LIST, OUT): not names.
- **The window** (as DRAW): `$RESIZE:ON` in bu1ld0r.bas is what lets the
  window manager resize it (the `_RESIZE` statement alone doesn't; `STRETCH`
  / `SMOOTH` lock its shape to the screen's). Everything draws on `uiImg&`
  (`scrW x scrH`); `Present` shows it `uiK` times bigger on the window's
  SCREEN (`winImg&`, uiK x ours) as a hardware image (`_DISPLAYORDER
  _HARDWARE`); the mouse is divided by `uiK`. A settled drag remakes both
  (`ScreenSet`, `Layout`) - a new SCREEN sizes the window itself. `rZ`/`rId`
  grow as needed (`RCap`). xdotool resizes any window, resizable or not:
  check `xprop WM_NORMAL_HINTS` has no min = max size or aspect. Test on a
  3840x2160 Xvfb to see 2x (Rick's display); CPU on Xvfb is llvmpipe's -
  measure on headless weston with the real GPU.
- **Modifiers held with the mouse** (Shift+wheel, Alt+drag): `xdotool
  keydown --window` sends synthetic events `_KEYDOWN` doesn't see. Use real
  (XTEST) input: `xdotool windowfocus --sync $W`, then `xdotool keydown
  shift; xdotool click 4; xdotool keyup shift` with no `--window`.
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

## Holes (booleans)

`pHole(i)`: part i is cut out of every solid part before it in its list
(the model's, or a prefab's: `MeshRun` does both, so prefabs hold holes and
a use can be one). Triangles: 1 to `sceneTN` the model with holes cut (what's
exported), to `holeTN` the holes' own shapes (drawn see-through grey, in
rId: a click picks them), then the ghost. `MeshBuild` skips the model when
`ModelText$` + `pfGen` is unchanged (`meshKey$`): only the ghost moved.
CSG (`CsgSubtract&`): polygons in a stack pool (`CsgMark`/`CsgRelease`
round each cut, nested ones too); only faces near the other's box are
looked at, only those that meet one of the other's (`CsgPolysMeet`) are
split - by the planes of the ones they meet; each piece is kept by rays up
from its middle (`CsgInside`, an x/z grid, three leaning rays voting); a
piece lying on the other's surface is tested nudged off it (that's what
makes flush tops cut through); a split none of whose pieces went is undone
(`cgPar`). BSP clipping (csg.js) was tried first: right, but every plane
sliced faces far away - 20,000 triangles and a second a build, against
3,000 and 27 ms now (`--bench 10` on a 48-slice sphere, three holes).
`$CHECKING:OFF` round MODEL/CSG.BM. `tools/test/parity.py X.obj` checks
every face faces out (one solid at a time: overlapping ones confuse it).

## Putting down, and the panel

While placing with nothing selected (`TplOn`), the panel edits `P_TPL`, a
part slot past the end (part 0, the ghost, is overwritten by RenderIcon):
its turns are its own, and `GhostRemake` puts them on top of the face's
(`RotMat`/`MatMul`/`MatTurns`: M = Ry Rx Rz). A hole put on a part's face
goes into it (the normal flipped). The parts list (UI/LIST, `listOn`,
`parts_list=` in the cfg) sits between the bin and the view: `vX0` moves.
`pHide` is the view's alone (the export makes all: `meshAll`), and only the
model's own parts (a prefab's hidden parts show in its uses).

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
--neon DIR --shot F.png --quit` checks with no input (`--bench N`: build
time to bench.txt). `tools/test/wind.py X.obj` counts triangles wound
outward/inward from the middle (no good with holes: parity.py).
Never `--neon` the real game folder in a test (use a scratch copy of
`neon-caster/models` and `hd/models`). No GUI launches from subagents. Run
long tests in the background, one at a time (`nice`, `LP_NUM_THREADS=2`).
Clean up after: `ps -eo pid,etime,args | grep -E 'bu1ld0r|Xvfb'`.

## Git

Commit or push only when Rick asks. Remote: github.com/grymmjack/bu1ld0r
(public), branch main - first commit 2026-10-30 (stage 1).
