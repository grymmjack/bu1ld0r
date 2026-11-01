''
' bu1ld0r - UI/BIN.BI
' =============================================================================
' The bin, down the left: the shapes, then a tab - the prefabs of the folder
' open in prefabs/ (its folders first, .. to go back up), PICTURES, or MODELS
' (models/: a click opens one) - as pictures.
'
CONST MAX_BI = 400
CONST BI_UP = 1, BI_DIR = 2, BI_PF = 3
CONST BI_MDL = 5 ' (a model in models/: the MODELS tab)
DIM SHARED biIcon&(MAX_BI) ' (a model's picture: made a frame at a time, let go when the list's made again)

DIM SHARED binIcon&(NUM_KINDS), binFill ' (binFill: how many pixels across the box's icon came out - the newer shapes are drawn as big)
DIM SHARED binDir$ ' (the folder open, in prefabs/: "" or "panels/")
DIM SHARED binTop ' (the first row showing)
DIM SHARED biN, biKind(MAX_BI), biName$(MAX_BI), biRef$(MAX_BI) ' (what's in it: .., folders, prefabs)
DIM SHARED placeRef$ ' (the prefab being put down, when placeKind is K_USE)
CONST F_PFNAME = 23 ' (a prefab's new name, typed where + FOLDER is)
DIM SHARED binMenu, binMenuRef$, binMenuX, binMenuY ' (a prefab right-clicked: EDIT IT, RENAME / MOVE)
DIM SHARED binMenuKind ' (0 a prefab; 1 a picture: EDIT IN DRAW, KALEIDOTRON; 2 a pictures folder: OPEN, KALEIDOTRON)
DIM SHARED askOn, askArg$ ' (opening askArg$ over unsaved work: SAVE FIRST / OPEN ANYWAY / CANCEL)
DIM SHARED mdlPress$, mdlPressI, mdlTmpPf, mdlTmpTop AS LONG ' (a MODELS tile pressed; a model being put in: its prefab for now, where its parts began)
DIM SHARED binMdlExt$ ' (MODELS showing a folder outside models/: from /, ending in /; "" - models/)
' Favourite folders, one list a tab (0 PREFABS: folders in prefabs/, "starter/"; 1 PICTURES and
' 2 MODELS: from /, ending in /), "|" between. The star at the path's end lists them (binMenuKind 3)
DIM SHARED binFav$(2), binFavSet(2) ' (binFavSet: bu1ld0r.cfg had fav_..= - else NEON-CASTER's folders to start)
CONST BIN_FAV_MAX = 16
DIM SHARED bfN, bfRef$(BIN_FAV_MAX + 2), bfShow$(BIN_FAV_MAX + 2) ' (the menu's rows: the tab's own folder, the favourites, then + / - this one)
