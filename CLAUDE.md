# bu1ld0r - notes for Claude

A 3D model builder in QB64PE (Rick's; started 2026-10-30 for NEON-CASTER's
props). PLAN.md has the stages; README.md the keys and files.

## Layout

`bu1ld0r.bas` (the loop) includes `_ALL.BI` / `_ALL.BM`; folders CORE (window,
input, helpers), MODEL (PARTS: the part list, .bld text, undo; PREFAB: the
prefab library, save as / edit a prefab; MESH: each shape as triangles,
holes cut; CSG: one solid less another, or their overlap; EMESH: mesh
parts; BAKE: APPLY, UNLINK, groups, tint, prefab rename; PIC: pictures;
IMPORT: an OBJ / NEON-CASTER prop opened as a model; SHAPES: dice, star,
gear, donut, diamond, spike, pill, arrow; SVG: an SVG opened as a model;
FONT: TrueType outlines), VIEW (camera, the rasterizer,
picking, outlines), UI (UI: panel, keys, mouse, putting down, dragging;
BIN: the bin - shapes, prefab folders, thumbnails; LIST: the parts list;
PICS: the bin's PICTURES tab, pictures put on faces, file drops, the
picture tools; PAINT: the painter; PEN: the pen; TEXT: the text tool;
REF: reference pictures; ALIGN: align parts / points / faces as seen; GIZMO: the
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
- **A SUB's `REDIM` of a SHARED array with a different type makes a
  local copy** (shX was DOUBLE in the .BI, SINGLE in the SUB: the shared
  one stayed size 0). Declare it once, the type it's used as.
- After `source tools/test/drv.sh`, `mv` is its mouse-move helper, not
  the shell's: move files with `/bin/mv`.
- A variable can't share a FUNCTION's name, whatever the suffix (`txKey$`
  vs `TxKey`: renamed `txRk$`). A string can't hold `""` - CHR$(34).
  A single-line IF can't hold a FOR.
- `OPEN f$ FOR BINARY` fails ("Bad file name") on a read-only file (the
  system's fonts): read with `_READFILE$`.
- `_DEVICEINPUT` pops an event each call: read it once a pass
  (`DO WHILE d ... d = _DEVICEINPUT`), never `DO WHILE _DEVICEINPUT` plus
  another call inside.
- `EmFromTris&`'s allEdges -1 merges gently curved walls into non-flat
  polygons that open gaps: text and merges pass 0.
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
cleared by EdSelClear / EdSelAll / EdSelReset / leaving EDGES), Ctrl+click
an edge picks its loop (`EdLoopPick`: `EdFan&` lists a point's neighbours
round it in `edNb`, on only through four-edged points), and
`EdPickedEdges` / `EdEdgeMeant` leave out an edge whose points are all
clicked edges' but which wasn't. WIRE's lines (`LineZ`) are the pixel under them XOR 808080, blended by
strength: `wMark` (wGen x 256 + strength) / `wOld` keep a pixel's first
colour so lines crossing don't XOR back (wGen bumped in RenderBegin; the
part colour passed in is unused). E's edge lines are light or dark by the
face's colour times how solid TEX shows it (`texOp`, 0 with TEX off).

## Shapes, the MODELS tab, the painter, SVGs

Kinds: K_DIE..K_ARROW are 7-14 (NUM_KINDS 14), K_USE 15, K_MESH 16 (the
.bld names kinds, so files don't care). MODEL/SHAPES: `ShapesSetup` (in
PartsSetup) makes each die once (`DieMake`: points, a convex hull by
triples of points, rested on its lowest face, fitted to the unit box;
d10 a trapezohedron, d30 the icosahedron's 12 + dodecahedron's 20 points
scaled onto the face planes); `pSeg` is FACES (`DieIdx`/`DieStep` snap
and step it), `pAmt` the second number (`AmtName$`/`SegName$` in UI
label them). Flat shapes are outlines in shX/shZ extruded (`MkPrism`).
The bin's shape tiles go `BinShapeCols` across, so `BI_Y0` is a
FUNCTION now (tabs at `BinTabY`); BIN_MIN 200. binTab 2 is MODELS
(`MdlBinList`; `ModelIcon` reads the model into PF_BASE+pfTop as a
throwaway prefab "*NAME" and renders it as a use, one a frame in
BinIconsDue; `MdlBinOpen` asks once when unsaved).

The painter (UI/PAINT, `pntOn`) takes the whole window: UiFrame / UiKey /
UiDraw hand over at their top. Ctrl+P (`PntFromPointer`): E's picked
faces -> `PicOfPicked$` (shared with EDIT IN DRAW), else the face under
the pointer's tTex, else `PicNewFile$` + PicPutAt. Pixels through a
`_MEM` (`pntM`); undo is whole pictures as strings (`PntSnap$`); shapes
redraw over `pntBack$` while dragging. Save: `_SAVEIMAGE`, then picW = 0
+ PicFind reloads it, the thumb dropped, PicWatch's signature refreshed.
MAKE (`PntMake`) is tileable value noise (`PntVNoise!` wraps), seeded.

SVG (MODEL/SVG, `SvgImport` from ModelLoad / DropTake / OpenList's
models/*.svg): a tag scanner (quotes kept, comments / CDATA / defs-like
containers skipped by depth), a group stack `svT#` / `svFill` / `svOp`
(32 deep), each shape's outlines through `svM#` into svPX/svPY (rings
svR0/svRN, shape svRE). `SvBuild`: fitted (x mirrored, so it reads
right from -z), near points merged (8E-4), in-line points and needles
dropped (`SvStraighten`: else walls and caps disagree - T-junctions),
depth by containment (odd: a hole of the smallest ring round it), holes
bridged into the outline (`SvBridge`, rightmost first), ear-clipped
(`SvEars`), caps both sides and walls (`SvWalls`), each shape one part
via EmFromTris&. Layers: a shape whose box overlaps an earlier one's is
`lay` steps (.02) nearer -z. Test: comps.py (per solid: closed, volume
> 0) - parity.py's rays misfire on thin slabs; real icons in
/usr/share/icons/hicolor/scalable/apps.

## Pen, text, merge, the pivot, the numpad, references

PEN (UI/PEN, `penOn`): points `penAX#/penAZ#` on the ground (PenGround,
snapped), handles `penO*/penI*`; PenMake flattens the curves into SVG's
rings and makes one flat mesh part (SvPrep + SvSolid, as an SVG's shape).
TEXT (UI/TEXT, `txOn`; MODEL/FONT): `FontLoad` reads a .ttf/.ttc/.otf with
`_READFILE$` (head maxp hhea hmtx loca glyf cmap 4 / 12, else 3,0 symbol
at +F000), `FontRings` walks simple and composite glyphs (quadratics in 6
steps) into svPX/svPY rings, svRE = the character; `FontScan` lists
fonts/, ~/git/DRAW/ASSETS/FONTS/, ~/.local/share/fonts, ~/.fonts,
/usr/share/fonts (deduped by name). `TxMake`: per character SvSolid of its
even-depth rings, turned lying (ax+x, z, az-y) or standing (ax-x, y,
az-z), `EmFromTris&(.., 0)`, all one group (GroupNew), named by the
letter. SvBuild's ring prep is `SvPrep (tol#)` (dedup, SvStraighten,
areas, depth, parents), shared by SVG / PEN / TEXT.

MERGE (M, panel slot 25 = APPLY / UNLINK / MERGE by what's picked):
`SelMerge` (MODEL/BAKE) folds the selected solid parts with `CsgBool&`
keep 2 (union: A's pieces outside B, B's outside A; a face both share kept
once - B's on-surface pieces tested at +-.0002) into the first part's slot,
unturned, sized to the box. `MkPolyTris` fans a convex polygon from a
corner whose neighbours are corners too (`pcS`): skipping flat triangles
made T-junctions, fanning from a mid-edge point made zero-area ones.

The pivot (UI/GIZMO): Ctrl+Alt shows `PivGhost` points (0 the middle, 1-6
side middles, 7-14 corners) of the selection box (`gzLo/gzHi`);
`PivPick` sets `tfPivOn`/`tfPiv` (a ghost, else the picked surface point
snapped); `GzUpdate` drops it when `PivKey$` (the selection) changes and
moves it with a MOVE; SCALE grows from it (`TfPivMove`), TURN goes round it.
SAME (UI/ALIGN `SmDraw`/`SmClick`, `samFirst` = the part clicked first);
SCALE snaps meshes / uses by their own size (`TfNatAll`).

The numpad (UI/UI): `_KEYHIT` folds keypad keys into plain ones, so a key
the numpad could send (`NumpadOf`: digits . + - * / Enter, or with Num
Lock off End Down PgDn Left 19456 Right Home Up PgUp Ins Del) counts as the
numpad only if that key is held (`_KEYDOWN(100256+n / 200000+n)`,
`NumpadHeld`) or was pressed in the last .25 s by the keyboard device
(`NumpadDev`: X11 ids, `NumpadId`; read once a pass). Fields, the painter,
OPEN, HELP, asks and TEXT get the plain key. `--keylog F` logs each key;
`tools/test/numpad.sh` holds / taps every keypad key with Num Lock on and
off (ALL PASS).

REF (UI/REF): slot 0 ground, 1 the back wall (z = gridWZ), 2 the side wall
(x = gridWX) - the far walls, from `GridWallsAt` (pulled out of
GridWallsDraw). A, B its middle on the plane (ground x,z; back x,y; side
z,y), `refW#` its width, the picture's right is -A. Pixels in `refPix`
(slot k at k x REF_PX, shrunk to 1024). `RefRenderAll` in ViewRender after
the backdrop, before DrawGrid: 16 x 16 pieces projected, `RefTri` spans
with 16.16 steps, blended into rMem, no depth ($CHECKING:OFF; 36 ms for
three view-filling ones). Controls `RefBtn` 1-6 at the view's top right
(`onRef` in UiFrame keeps orbit / pan / clicks off them); `refTr`: drag
(`RefPress`/`RefFrame`, `RefArrowAt` locks one way), `RefKey`, `RefWheel`.
.bld: `ref K OP SHOWN A B W PATH` (`RefLines` in ModelWrite, `RefFromText`
in ModelLoad, ModelNew clears; not in undo or prefabs). Drops on REF:
DropTake; a PICTURES tile let go on it: UiFrame's mR1.

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
