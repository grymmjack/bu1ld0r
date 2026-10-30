''
' bu1ld0r - MODEL/PARTS.BI
' =============================================================================
' A model is a list of parts: each a shape, where it stands, how it's
' turned, how big, its colour. Part 0 is no part of the model: it's the
' shape being put down (the ghost that follows the pointer).
'
CONST MAX_PARTS = 1024
CONST K_BOX = 1, K_CYL = 2, K_SPHERE = 3, K_CONE = 4, K_WEDGE = 5, K_TUBE = 6, NUM_KINDS = 6
CONST MAX_UNDO = 200

DIM SHARED pN AS LONG
DIM SHARED pKind(MAX_PARTS) AS INTEGER, pSeg(MAX_PARTS) AS INTEGER, pSel(MAX_PARTS) AS INTEGER
DIM SHARED pX(MAX_PARTS), pY(MAX_PARTS), pZ(MAX_PARTS) ' (its foot's middle)
DIM SHARED pRX(MAX_PARTS), pRY(MAX_PARTS), pRZ(MAX_PARTS) ' (turns, degrees: Z, then X, then Y)
DIM SHARED pSX(MAX_PARTS), pSY(MAX_PARTS), pSZ(MAX_PARTS) ' (the box it fills, in cells)
DIM SHARED pAmt(MAX_PARTS) ' (a cone's top, a tube's hole, a sphere's share - 0 to 1)
DIM SHARED pCol(MAX_PARTS) AS _UNSIGNED LONG

DIM SHARED kindName$(NUM_KINDS), kindSX(NUM_KINDS), kindSY(NUM_KINDS), kindSZ(NUM_KINDS), kindAmt(NUM_KINDS)
DIM SHARED mdlName$, mdlDirty, mdlAsk ' (mdlAsk: NEW or OPEN pressed once over unsaved changes)
DIM SHARED snapStep ' (the grid moves snap to: 0 none)
DIM SHARED curCol AS _UNSIGNED LONG ' (the colour a new part gets)

DIM SHARED undoS$(MAX_UNDO), undoN, redoS$(MAX_UNDO), redoN
