''
' bu1ld0r - UI/UI.BI
' =============================================================================
' The screen: the bar along the top (the model's name, NEW OPEN SAVE
' EXPORT), the bin of shapes down the left, the 3D view, the panel down the
' right (the selected parts' place, turn, size, colour), the message line.
'
CONST F_PX = 1, F_PY = 2, F_PZ = 3, F_RX = 4, F_RY = 5, F_RZ = 6, F_SX = 7, F_SY = 8, F_SZ = 9
CONST F_SEG = 10, F_AMT = 11, F_COL = 12, F_NAME = 20, F_DIR = 21, F_LAST = 12 ' (F_DIR: a new folder's name, in the bin)
CONST NUM_PAL = 32

DIM SHARED palCol(NUM_PAL - 1) AS _UNSIGNED LONG

' What the mouse is doing
DIM SHARED placeKind ' (a shape being put down: the ghost follows the pointer)
DIM SHARED placeDrag ' (pressed on the bin: let go over the view puts it there)
DIM SHARED gHit AS V3, gN AS V3, gHave, gOnPart ' (where the ghost was last put: the point, the face's way out, a part's face or the ground)
DIM SHARED orbitOn, panOn, lmX, lmY
DIM SHARED dragArm, dragOn, dragVert, dragPX, dragPY, dragFirst
DIM SHARED dragG AS V3, dragN AS V3
DIM SHARED dragX0(MAX_PARTS), dragY0(MAX_PARTS), dragZ0(MAX_PARTS)
DIM SHARED ghostKey$ ' (where the ghost was last made: made again only when it moves)

' Typing into a field
DIM SHARED typeField, typeBuf$ ' (the field being typed in, what's in it)
DIM SHARED typeCur, typeAnc, typeScroll, typeDrag, typeClickF, typeClickT# ' (the cursor, the other end of what's picked; the first letter showing; a drag picking; the last click, for a double one)
DIM SHARED wheelField, wheelT AS DOUBLE ' (a run of wheel turns on one field is one undo step)

DIM SHARED helpOn, openOn, openN, openTop
' The top bar's view buttons, each with a slider: TEX (the faces, how solid), WIRE (the
' edges, how strong), GRID (the walls; how bright). Buttons 8 to 10, sliders 1 to 3
CONST TB_VIEW = 8, SL_W = 64
DIM SHARED topSlide ' (the slider being dragged: 1 to 3, 0 none)
DIM SHARED openName$(500)
DIM SHARED quitAsk
DIM SHARED qCtrl, qShift, qAlt ' (the modifier keys as the key queue has them)
DIM SHARED helpLine$(320), helpPg(320), helpN ' (HELP: its lines - "KEYS|what they do", "#HEADING" - and which page each is on)
DIM SHARED hpName$(16), hpN, helpPage ' (its pages, and the one shown)
CONST NP_N = 16 ' (the numpad's keys: NumpadHeld)
DIM SHARED npHeld(NP_N), npT#(NP_N) ' (each numpad key held last frame; when it was pressed: -1 once it's been used)
DIM SHARED guidesOn ' (GUIDES, Ctrl+H: the view's guides shown)
DIM SHARED selRect, selRX0, selRY0 ' (a box being dragged round parts, from: view coords)
