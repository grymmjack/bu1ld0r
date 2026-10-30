# bu1ld0r - notes for Claude

A 3D model builder in QB64PE (Rick's; started 2026-10-30 for NEON-CASTER's
props). PLAN.md has the stages; README.md the keys and files.

## Layout

`bu1ld0r.bas` (the loop) includes `_ALL.BI` / `_ALL.BM`; folders CORE (window,
input, helpers), MODEL (PARTS: the part list, .bld text, undo; PREFAB: the
prefab library, save as / edit a prefab; MESH: each shape as triangles,
holes cut; CSG: one solid less another, or their overlap; EMESH: mesh
parts; BAKE: APPLY, UNLINK, groups, tint, prefab rename; PIC: pictures;
IMPORT: an OBJ / NEON-CASTER prop opened as a model), VIEW (camera, the rasterizer,
picking, outlines), UI (UI: panel, keys, mouse, putting down, dragging;
BIN: the bin - shapes, prefab folders, thumbnails; LIST: the parts list;
PICS: the bin's PICTURES tab, pictures put on faces, file drops, the
picture tools; ALIGN: align parts / points / faces as seen; GIZMO: the
move widget's arrows and X/Y/Z held - a drag kept to one axis (`AxisAt#`);
EDIT: a part's faces, edges (`ED_EDGES`: picked as their two points in edSelV - `EdPtMode` is points or edges) and points; BEVEL: B in E, a mode; LOOP: O in E, the same mode), OUT (EXPORT: OBJ + NEON-CASTER; TIDY:
the export's mesh tidied). As NEON-CASTER: `.BI`
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
- `base`, `list`, `out`, `common`, `any`, `on`, `key` are reserved words
  (or clash with QB64's): not names. Nor `sgn#` (SGN).
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
- **Rick often has his own bu1ld0r running: never kill by name**
  (`pgrep -x bu1ld0r.run` / `pkill bu1ld0r` kill his too). Only the test
  copy: `pkill -f '^/tmp/claude-1000/bu1ld0r-test/app/bu1ld0r.run'`
  (drv.sh's `testkill`; `win` finds only it). The `^` keeps the pattern
  from matching the shell running pkill. Xvfb: only `:99`'s -
  `pkill -f '^Xvfb :99'`.
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
Polygons carry their picture through a cut (`cgTex`, `cgMap`: u and
v as planes, 8 doubles a polygon, `CsgMapFrom` a triangle's, `CsgLike`
copies, `CsgEmit` evaluates; a hole's walls get none).
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

## Mesh parts and editing

`K_MESH` (`pMesh` its mesh): polygons in a pool (MODEL/EMESH: `mbV0`..,
first point/polygon at base + 1; corners `mcV` from 0, `mcE` the edge on
is the shape's own). Meshes never change: an edit makes a new one
(`EmLoad` -> work arrays sw/sf/sc -> `EmWrite&`, `meshGen` in meshKey$);
undo text names them (`mesh=ID`), `.bld` writes `v`/`f` lines. `MeshGc`
(model/prefab load) lets go of unnamed ones. `EmFromTris&` welds
triangles and joins flat same-colour neighbours (`EmMerge`). E (UI/EDIT)
turns any part into one (`PartMeshOf&`); picking faces is `tFace` = the
polygon. APPLY (`HoleApply`) / UNLINK (`UseUnlink`) make them too.
Groups `pGrp`, KEEP `pKeep` (`CsgBool&` keep), tint `pTint` (alpha =
amount, per use level `usTint`). The parts list shows a group as a folder
row (`ListRowsMake`: lrPart/lrHead/lrGrp; `GroupGather` keeps a group's
parts together). Several selected parts turn as one (`SelTurnBy`: round
their triangles' box middle). GRID (`gridWalls`): walls drawn in DrawGrid
(`GridWallsDraw`, the far side from the eye), the selection's box shadowed on
them in the overlay (`GridShadows`, `LineBehind`: only where rId is 0). TEX / WIRE / GRID at the top (buttons 8-10, sliders `SliderRect` 1-3): `viewWire` is TEX off; `wireOn` draws `WireTriZ` (`LineZ`: blended, depth-tested - the hidden part at the faces' see-through); `texOp` < 100 fades the faces towards a copy of the backdrop (`TexFade`). EXPORT's repeat cut (`ExSplitRepeats`) cuts a face's triangles as one outline (`ExLoop`: only if flat and evenly mapped, else a triangle at a time), pieces ear-clipped (`ExEars`, on the face itself if the picture's squashed). EdCommit spreads a squashed picture (`PicUnsquash`: extrude's sides). Panel FLIP / GROW / TURN (UI/ALIGN `ShDraw` / `ShClick` at 684: `SelFlip` mirrors a mesh's points and rewinds its polygons, `SelSizeBy`). Typing: `TypeStart`, cursor `typeCur` / `typeAnc` (picked between), `typeScroll`. Divide on any polygon: `EdDivideAny` (`EdCutOf&`, `EdAlong#` for the neighbours' spots). `BIN_W` is a variable (dragged: `DockFrame`, `DockAt`, `DockClamp` in Layout; at least `BIN_MIN`); `PANEL_W` stays `PANEL_MIN` (Rick didn't want the panel dragged). The bin's tiles go `BinCols` across, `BinTS` big (prefabs 64; PICTURES `picTS`, Shift+wheel `PicTileWheel`, `pic_size=`, at most BIN_W - 14; thumbs remade at that size, 8 a frame). HELP is
paged: `HelpTopic NAME` then `HelpAdd "KEYS|text"` / `"#HEADING"`; `draw` is
reserved (DRAW), as is `helpPage` vs a SUB `HelpPage`.

## Bevel (UI/BEVEL)

B in E (`BvStart`) is a mode, as MOVE IT is: `bvBase` is the mesh as it
was and every slider move rebuilds from it (`BvPreview`: `BvGather`,
`BvBuild`, `EmWrite&`; pMesh shows the preview, `bvPrev`). APPLY puts
bvBase back for UndoPush, then the preview; Esc (`BvCancel`) shows the
base. Edges: both ends picked (edges mode, `bvSelV`), or all of the
picked faces'; `BvTry` wants two faces, not flat (normals' dot over
.9995), and closed fans round both ends (`BvFan&` walks them by
EmEdgeFind - live faces only, so the corner patches are made before the
old faces are retired). WIDTH is % of `bvMaxW#` (half each untouched fan
edge, half `BvReach#` of each face beside a bevelled edge). BvBuild: per
point, new points slide along unbevelled edges (`BvSlide&`, w / sin) or
sit on the bisector where two bevelled edges meet (`BvCorner&`); each
corner's replacement (`bvRS/bvRC/bvRL`); each edge end's round
(`bvPA/bvPB`; `BvRound&` a quadratic Bezier through `BvCtrl` - the point
on the edge level with the two slid points: bending towards the corner
point made spikes); corner patches (a polygon, or a triangle fan when
round); old faces rebuilt (spots by `PicUVAt`); strips in the first
face's colour. E's buttons are three across (`EdBtn`, 13 = BEVEL, 14-16
SPLIT / CONNECT / LOOP on a fourth row). `BvWeldNew` makes new points on
one spot one (`EmRemap`): an unwelded corner (two ids, one place) left a
zero-area corner face, skipped, so a gap. `BvTry` refuses an edge folded
flat (normals' dot under -.9995, `bvFold`): two faces back to back, a fin -
what inset then push in by the same amount makes (Rick's friendshipcube).
In EDGES `bvSA/bvSB` (from `EdPickedEdges`) say which edges, not bvSelV.

LOOP (UI/LOOP, `LcStart`) is bevel's mode with `bvKind` 2 (BvPreview,
the sliders, BvDraw, BvKey branch on it): `LcRing` walks from each picked
edge both ways (`LcWalk`: a four-sided face's opposite side, then the face
past it; `lcUsed` stops rings crossing), `LcCut` puts `lcCuts` points on
each ring edge (`LcT#`: POSITION if one, else even), strips each ring face
(its two edges' points; `LcHas` for which way the second runs) and
`LcInsert`s the points into the faces past the ends. SPLIT (`EdSplit`,
`EdMidOf&` + `EdInsertCuts`, which EdDivide uses too) and CONNECT
(`EdConnect`: a face's two picked sides or corners, halves as
EdDivideAny's). Edges picked are points (edSelV), so two opposite sides
of a quad pick all four: `edPkA/edPkB` keep the edges clicked (EdPress,
`EdPkMark`; the work's in `wkPk`, renumbered by swMap in EdCommit;
cleared by EdSelClear / EdSelAll / EdSelReset / leaving EDGES), and
`EdPickedEdges` / `EdEdgeMeant` leave out an edge whose points are all
clicked edges' but which wasn't. E's edge lines are light or dark by the
face's colour times how solid TEX shows it (`texOp`, 0 with TEX off).

## Pictures (textures)

A mesh polygon can carry a picture: `mfTex` (pool) / `sfTex` (work) /
`tTex` (triangle), PIC's index (`PicFind(ref$)`: `pictures/REF.png`,
registered even if missing - picW 0 - and loaded once it's there), and a
spot per corner (`mcTU/mcTV`, `scTU/scTV`, `tU/tW` at 3t+k), in image
terms (v down from the top: OBJ's is 1 - v). `EmAddF&` takes `emTex` /
`emU` / `emW` and resets emTex - set them before each call. EmMerge never
joins textured polygons; the edit tools carry spots (extrude's sides take
the rim edge's, inset's ring and divide's midpoints are averaged);
EdColour takes the picture off. RasterTri draws them with `FillTriT`
(perspective-correct; spots carried through the near clip), except the
ghost / holes / wireframe. Tidy keeps textured triangles as they are
(parked at the top of the arrays, `tdHold`). Export: `ExAtlas` - one
picture with room (`ExMarkUsed`, 16x16 squares): kept pixel for pixel,
the colours in unused squares (exMode 1); else a 2x2 / 4x4 grid (2).
IMPORT (`ObjImport`; ModelLoad on `.obj` or `neon:NAME`; OPEN lists the
game's props via `NeonInDir$` - read only): pieces by welded points
(union-find), each a mesh part, all one group; the texture copied to
`pictures/neon/` (kept if already there: Rick may have changed it in DRAW;
OPEN runs `PicReloadAll`). Putting one on (UI/PICS `PicPutAt`): the hit
point from `RayPlane`, a shape made a mesh part, its polygon found again
by `PicFaceAt&`; `PicFitFrom` stretches it over the face (`PicAxes`: up
as near the part's up as it can be). The bin can show a folder outside pictures/ (`binPicExt$`, from the path box `F_PICPATH` / `PicGoTo`): its refs are paths from / with `.png` (`PicPath$` gives any ref's file), tiles from their own ring (`PicThumbOut&`, 2 loads a frame), copied in by `PicBring$` when picked (`pmSrc$` the original). Launch helpers (`DrawOpen`, `KaleidoOpen`) use a waiting SHELL with `&` inside: `SHELL _DONTWAIT` left a zombie per launch. Drops: `_ACCEPTFILEDROP`, taken 3
frames on (`DropFrame`: GLFW gives the pointer late); `--drop F` tests it.
Export: `ExSplitRepeats` cuts repeats (the game clamps). Test: `--open neon:crate --save` / `--export --neon
SCRATCH` and compare with the game's own textures (`compare -metric AE`).

## Tidying the export (OUT/TIDY)

Opt-in: `mdlTidy` (`tidy 1` in the .bld, EXPORT: TIDIED) - Rick found it
loses too much detail to be automatic. `TidyRun` replaces triangles 1..sceneTN in place when `TidyOn` (export's
`tidyNow`, or T's `tidyView` outside edit mode; in meshKey$): hidden
faces by winding number per solid (`tSol`, set in MeshRun by
`SolidMark` - not tPart: a cut's walls carry the hole's part), welded,
T-junctions filled (`TdTJoin`), `EmMerge -1`, straight corners out,
ear-clipped, short edges collapsed, then QEM edge collapse to
`mdlBudget` (`budget N` in .bld) capped at TD_SHOW of the model's size.
WriteObj writes welded indexed vertices. `--tidy` = T at start.
parity.py can't judge a tidied OBJ (open where parts meet): compare
`--shot` with and without `--tidy`.

## Export (NEON-CASTER)

As models.py: OBJ y up, front -z, `# frame F` (max of 2 x reach and
height, x 1.04), one texture (each colour an 8th-square block), 8 pictures
at 64 px drawn 4x and shrunk (textured faces drawn textured), lit `eye*.55 + up*.8 - right*.35`, shade
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
Clean up after: `ps -eo pid,etime,args | grep -E 'bu1ld0r|Xvfb'` - and stop only the test ones.

## Git

Commit or push only when Rick asks. Remote: github.com/grymmjack/bu1ld0r
(public), branch main - first commit 2026-10-30 (stage 1).
