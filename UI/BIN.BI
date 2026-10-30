''
' bu1ld0r - UI/BIN.BI
' =============================================================================
' The bin, down the left: the six shapes, then the prefabs of the folder
' open in prefabs/ (its folders first, .. to go back up), as pictures.
'
CONST MAX_BI = 400
CONST BI_UP = 1, BI_DIR = 2, BI_PF = 3
CONST BI_Y0 = 194 ' (where the prefab tiles start: BinRows say how many rows show)

DIM SHARED binIcon&(NUM_KINDS)
DIM SHARED binDir$ ' (the folder open, in prefabs/: "" or "panels/")
DIM SHARED binTop ' (the first row showing)
DIM SHARED biN, biKind(MAX_BI), biName$(MAX_BI), biRef$(MAX_BI) ' (what's in it: .., folders, prefabs)
DIM SHARED placeRef$ ' (the prefab being put down, when placeKind is K_USE)
CONST F_PFNAME = 23 ' (a prefab's new name, typed where + FOLDER is)
DIM SHARED binMenu, binMenuRef$, binMenuX, binMenuY ' (a prefab right-clicked: EDIT IT, RENAME / MOVE)
DIM SHARED binMenuKind ' (0 a prefab; 1 a picture: EDIT IN DRAW, KALEIDOTRON; 2 a pictures folder: OPEN, KALEIDOTRON)
