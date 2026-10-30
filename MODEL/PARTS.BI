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
CONST P_TPL = P_ALL + 1 ' (the shape being put down, as it's set up: its turns its own, not the face's - the ghost is made from it)
CONST P_SWAP = P_TPL + 1 ' (room for one, while two change places)
CONST K_BOX = 1, K_CYL = 2, K_SPHERE = 3, K_CONE = 4, K_WEDGE = 5, K_TUBE = 6, NUM_KINDS = 6
CONST K_USE = 7 ' (a prefab: not a shape of the bin's six)
CONST MAX_UNDO = 200

DIM SHARED pN AS LONG
DIM SHARED pKind(P_SWAP) AS INTEGER, pSeg(P_SWAP) AS INTEGER, pSel(P_SWAP) AS INTEGER
DIM SHARED pX(P_SWAP), pY(P_SWAP), pZ(P_SWAP) ' (its foot's middle)
DIM SHARED pRX(P_SWAP), pRY(P_SWAP), pRZ(P_SWAP) ' (turns, degrees: Z, then X, then Y)
DIM SHARED pSX(P_SWAP), pSY(P_SWAP), pSZ(P_SWAP) ' (the box it fills, in cells)
DIM SHARED pAmt(P_SWAP) ' (a cone's top, a tube's hole, a sphere's share - 0 to 1)
DIM SHARED pCol(P_SWAP) AS _UNSIGNED LONG
DIM SHARED pRef$(P_SWAP) ' (a use: the prefab, its path in prefabs/ without .bld - "panels/toggle")
DIM SHARED pHole(P_SWAP) AS INTEGER ' (a hole: cut out of every solid part before it in its list - MODEL/CSG)
DIM SHARED pHide(P_SWAP) AS INTEGER, pWire(P_SWAP) AS INTEGER ' (left out of the view and the export; drawn as lines only)
DIM SHARED pName$(P_SWAP) ' (its own name in the parts list, if given: no spaces)

DIM SHARED kindName$(K_USE), kindSX(K_USE), kindSY(K_USE), kindSZ(K_USE), kindAmt(K_USE)
DIM SHARED defSX(K_USE), defSY(K_USE), defSZ(K_USE), defCol AS _UNSIGNED LONG ' (each kind's own size, and the first colour: what a middle click on a field puts back)
DIM SHARED mdlName$, mdlDirty, mdlAsk ' (mdlAsk: NEW, OPEN or a prefab's edit asked once over unsaved changes)
DIM SHARED mdlPf$ ' (the model open is this prefab: Ctrl+S saves it to prefabs/)
DIM SHARED askRef$ ' (the prefab that mdlAsk, or replacing one, was about)
DIM SHARED txtName$ ' (the name line PartsFromText met)
DIM SHARED snapStep ' (the grid moves snap to: 0 none)
DIM SHARED curCol AS _UNSIGNED LONG ' (the colour a new part gets)

DIM SHARED undoS$(MAX_UNDO), undoN, redoS$(MAX_UNDO), redoN
