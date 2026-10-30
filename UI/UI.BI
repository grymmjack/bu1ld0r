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
DIM SHARED orbitOn, panOn, lmX, lmY
DIM SHARED dragArm, dragOn, dragVert, dragPX, dragPY, dragFirst
DIM SHARED dragG AS V3, dragN AS V3
DIM SHARED dragX0(MAX_PARTS), dragY0(MAX_PARTS), dragZ0(MAX_PARTS)
DIM SHARED ghostKey$ ' (where the ghost was last made: made again only when it moves)

' Typing into a field
DIM SHARED typeField, typeBuf$, typeFresh
DIM SHARED wheelField, wheelT AS DOUBLE ' (a run of wheel turns on one field is one undo step)

DIM SHARED helpOn, openOn, openN, openTop
DIM SHARED openName$(500)
DIM SHARED quitAsk
DIM SHARED qCtrl, qShift, qAlt ' (the modifier keys as the key queue has them)
DIM SHARED helpLine$(40), helpN
