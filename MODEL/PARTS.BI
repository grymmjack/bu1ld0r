''
' bu1ld0r - MODEL/PARTS.BI
' =============================================================================
' A model is a list of parts: each a shape, where it stands, how it's
' turned, how big, its colour. Part 0 is no part of the model: it's the
' shape being put down (the ghost that follows the pointer). A part can be
' a prefab used whole (K_USE: pRef$ its name; its size is its scale). The
' prefab library's own parts are kept in the same arrays, after the model's
' (PF_BASE + 1 on: MODEL/PREFAB).
'
CONST MAX_PARTS = 1024
CONST MAX_PFP = 16000 ' (every prefab's parts, all told)
CONST PF_BASE = MAX_PARTS, P_ALL = MAX_PARTS + MAX_PFP
CONST K_BOX = 1, K_CYL = 2, K_SPHERE = 3, K_CONE = 4, K_WEDGE = 5, K_TUBE = 6, NUM_KINDS = 6
CONST K_USE = 7 ' (a prefab: not a shape of the bin's six)
CONST MAX_UNDO = 200

DIM SHARED pN AS LONG
DIM SHARED pKind(P_ALL) AS INTEGER, pSeg(P_ALL) AS INTEGER, pSel(P_ALL) AS INTEGER
DIM SHARED pX(P_ALL), pY(P_ALL), pZ(P_ALL) ' (its foot's middle)
DIM SHARED pRX(P_ALL), pRY(P_ALL), pRZ(P_ALL) ' (turns, degrees: Z, then X, then Y)
DIM SHARED pSX(P_ALL), pSY(P_ALL), pSZ(P_ALL) ' (the box it fills, in cells)
DIM SHARED pAmt(P_ALL) ' (a cone's top, a tube's hole, a sphere's share - 0 to 1)
DIM SHARED pCol(P_ALL) AS _UNSIGNED LONG
DIM SHARED pRef$(P_ALL) ' (a use: the prefab, its path in prefabs/ without .bld - "panels/toggle")

DIM SHARED kindName$(K_USE), kindSX(K_USE), kindSY(K_USE), kindSZ(K_USE), kindAmt(K_USE)
DIM SHARED mdlName$, mdlDirty, mdlAsk ' (mdlAsk: NEW, OPEN or a prefab's edit asked once over unsaved changes)
DIM SHARED mdlPf$ ' (the model open is this prefab: Ctrl+S saves it to prefabs/)
DIM SHARED askRef$ ' (the prefab that mdlAsk, or replacing one, was about)
DIM SHARED txtName$ ' (the name line PartsFromText met)
DIM SHARED snapStep ' (the grid moves snap to: 0 none)
DIM SHARED curCol AS _UNSIGNED LONG ' (the colour a new part gets)

DIM SHARED undoS$(MAX_UNDO), undoN, redoS$(MAX_UNDO), redoN
