''
' bu1ld0r - UI/BRUSH.BI
' =============================================================================
' Painting on the model (Shift+P, PAINT in the top bar): the 3D view stays
' (right drag turns, middle pans, the wheel zooms) and the left button
' paints straight onto the faces' pictures - a brush in pixels, crossing
' faces and parts. A face's pixels are painted where they are (its
' picture's file changes, as in the painter). A face with no picture - or,
' JUST HERE, one whose pixels another face shows too (BrShareScan) - is
' first given its own place: where the model's one picture (brMain) is
' see-through, else pictures/paint/MODEL.png (BR_ATLAS square, as the
' game's texture), filled with what it showed (pixel for pixel when it
' can be). A place is taken where the picture isn't see-through (alpha
' 0): kept in the picture itself, so it outlives undo and saving.
' The panel: tools, the painter's colours, sizes.
'
CONST BR_PENCIL = 1, BR_BRUSH = 2, BR_ERASE = 3, BR_FILL = 4, BR_PICK = 5
CONST BR_ATLAS = 256 ' (a model's own picture: the game's texture size)
CONST BR_UNDO = 60
DIM SHARED brOn, brTool, brSz, brAll ' (brAll: EVERYWHERE - a picture other faces use is painted where it is; else JUST HERE)
DIM SHARED brDensity#, brAuto# ' (a new place's pixels a cell - 0: brAuto#, from the model's own pictures)
DIM SHARED brDown, brLX, brLY, brHas ' (a stroke; its last dab on the view; brHas: there was one - Shift+click's line)
DIM SHARED brU$(BR_UNDO), brUN, brR$(BR_UNDO), brRN ' (strokes undone and done again: see BrStrokeEnd)
DIM SHARED brStk AS LONG, brMdl, brCN AS LONG ' (the stroke's number; it changed the model; pixels it changed)
REDIM SHARED brCK(0) AS INTEGER, brCI(0) AS LONG, brCO(0) AS _UNSIGNED LONG ' (each: picture, pixel, colour before)
REDIM SHARED brMk(0) AS LONG ' (each pixel of picPix: the stroke that noted it)
DIM SHARED brOrig$(MAX_PIC) ' (each picture as painting began: ERASE puts it back)
DIM SHARED brWarn$, brMain ' (brMain: the model's one picture - new places go in it first)
DIM SHARED brShKey$, brShN AS LONG ' (JUST HERE: which faces' places another face shares - for meshKey$)
REDIM SHARED brShK(0) AS LONG, brShS(0) AS _BYTE, brShT(0) AS INTEGER
REDIM SHARED brShX0(0) AS SINGLE, brShY0(0) AS SINGLE, brShX1(0) AS SINGLE, brShY1(0) AS SINGLE
REDIM SHARED brNL(0) AS LONG ' (the triangles a dab reaches)
DIM SHARED brNN AS LONG
REDIM SHARED brWX(0) AS DOUBLE, brWY(0) AS DOUBLE, brWZ(0) AS DOUBLE ' (a face being unwrapped: its corners in the world)
