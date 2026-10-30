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
