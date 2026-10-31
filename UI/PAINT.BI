''
' bu1ld0r - UI/PAINT.BI
' =============================================================================
' The painter (as NEON-CASTER's): a face's picture opened over the whole
' window to paint on - Ctrl+P on a face (or the faces picked in E), PAINT IT
' in the panel or the bin's right-click. Pencil, brush, line, box, ellipse,
' fill, a gradient fill (NEON-CASTER's ways), pick; mirrors, wrap, tiled;
' MAKE (a picture made from the two colours: noise, wood, brick...) and
' FILTERS (blur, emboss...). Ctrl+S saves the PNG and it shows on its faces.
'
CONST PN_PENCIL = 1, PN_BRUSH = 2, PN_LINE = 3, PN_RECT = 4, PN_RECTF = 5, PN_ELL = 6, PN_ELLF = 7, PN_FILL = 8, PN_GRAD = 9, PN_PICK = 10
CONST PN_SEL = 11
CONST PN_UNDO = 40
CONST PN_MAKES = 14, PN_FILTERS = 10
DIM SHARED pntOn, pntRef$, pntImg&, pntW AS LONG, pntH AS LONG, pntDirty, pntAsk
DIM SHARED pntTool, pntSize, pntFg AS _UNSIGNED LONG, pntBg AS _UNSIGNED LONG
DIM SHARED pntMirX, pntMirY, pntWrap, pntTile, pntGrid, pntWay$ ' (pntWay$: the gradient's - V H D R M)
DIM SHARED pntZ, pntOX, pntOY ' (zoom: screen pixels a picture pixel; where its top left is in the canvas)
DIM SHARED pntDown, pntBtn, pntLX AS LONG, pntLY AS LONG, pntSX AS LONG, pntSY AS LONG, pntBack$ ' (a stroke: which button, its last pixel, where it began; the picture as it was - shapes are drawn again over it)
DIM SHARED pntPan, pntPanX, pntPanY
DIM SHARED pntU$(PN_UNDO), pntUN, pntR$(PN_UNDO), pntRN
DIM SHARED pntHex$, pntTyping
DIM SHARED pntSeed AS LONG, pntM AS _MEM ' (the picture's pixels)
DIM SHARED pntSelOn, pntQX AS LONG, pntQY AS LONG, pntQW AS LONG, pntQH AS LONG ' (SELECT: the box picked, picture pixels)
DIM SHARED pntSq, pntSqX AS LONG, pntSqY AS LONG, pntFltOn, pntBase$ ' (dragging: 1 a box, 2 moving it; lifted: the picture under it)
REDIM SHARED pntFl(0) AS _UNSIGNED LONG, pntCb(0) AS _UNSIGNED LONG ' (its pixels lifted; copied)
DIM SHARED pntFW AS LONG, pntFH AS LONG, pntCW AS LONG, pntCH AS LONG
REDIM SHARED pntGMk(0) AS _BYTE ' (GRADIENT: the pixels it fills)
DIM SHARED pntGLive, pntGBase$, pntGd, pntGSX!, pntGSY!, pntGEX!, pntGEY!, pntGRev, pntGX0 AS LONG, pntGY0 AS LONG, pntGX1 AS LONG, pntGY1 AS LONG, pntGGX!, pntGGY!
DIM SHARED pntGSpread, pntGRep ' (past its ends: 0 PAD, 1 REP, 2 BNC; how many times across)
DIM SHARED pntFx, pntFxDrag, pntClean, pntScl ' (MAKE: Shift's strength 0-100; CLEAN - no stray random colours; the parts' size, 2 ^ pntScl)
