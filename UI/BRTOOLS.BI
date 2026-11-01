''
' bu1ld0r - UI/BRTOOLS.BI
' =============================================================================
' Painting on the model: the tools that reach past the brush (BRTOOLS.BM) -
' LINE, BOX, ELLIPSE (drawn on the view, painted onto what's under them),
' FILL, GRADIENT, MAKE and FILTERS over a REACH of the model: the colour
' joined to the click (across the part's faces), the face, the part, or
' all of it. Each works on a set of picture pixels with their places on
' the model (bx*), so it runs across faces as the model shows them.
'
CONST BR_LINE = 6, BR_BOX = 7, BR_ELL = 8, BR_GRAD = 9, BR_MAKE = 10, BR_FILTER = 11
CONST BR_TILE = 64 ' (MAKE's pattern: as the painter makes a 64 x 64 picture)
DIM SHARED brReach, brFilled, brMakeK, brFiltK, brPage ' (REACH: 0 COLOUR 1 FACE 2 PART 3 ALL; the panel's page: 0 PAINT, 1 MAKE)
DIM SHARED brFaceOnly, brFK AS LONG ' (ONE FACE: a stroke / shape / fill kept to the face it starts on - that face, part x 65536 + face)
DIM SHARED brTilt, brPlOn ' (TILT: a box / ellipse lies on the face pressed on - brPlOn: this one does)
DIM SHARED brPOX#, brPOY#, brPOZ#, brPNX#, brPNY#, brPNZ#, brPAX#, brPAY#, brPAZ#, brPBX#, brPBY#, brPBZ#, brPA1#, brPB1# ' (its plane: where pressed, its way out, across, up; the pointer there)
DIM SHARED brQN
REDIM SHARED brQX(0) AS SINGLE, brQY(0) AS SINGLE ' (the shape round, on the view)
DIM SHARED brGR ' (what BrGather lists: 0 the brush's, 1 face, 2 part, 3 all, 4 facing the eye in brSB*)
DIM SHARED brSBX0#, brSBY0#, brSBX1#, brSBY1#
DIM SHARED brSh, brSX0, brSY0, brSX1, brSY1, brGMoved ' (a drag: 1 LINE / BOX / ELLIPSE, 2 GRADIENT; where it began, where it is)
DIM SHARED brGSX!, brGSY!, brGEX!, brGEY! ' (the gradient's ends on the view)
DIM SHARED bxN AS LONG, bxGen AS LONG, brSelN AS LONG
REDIM SHARED bxK(0) AS INTEGER, bxI(0) AS LONG, bxT(0) AS LONG, bxF(0) AS LONG ' (each pixel: picture, place in it, a triangle showing it, its face)
REDIM SHARED bxX(0) AS SINGLE, bxY(0) AS SINGLE, bxZ(0) AS SINGLE, bxH(0) AS SINGLE ' (where on the model; how big a pixel is there)
REDIM SHARED bxMk(0) AS LONG, bxAt(0) AS LONG ' (per picPix: in the set this time (bxGen); which one)
REDIM SHARED brSel(0) AS LONG, brGX(0) AS SINGLE, brGY(0) AS SINGLE ' (the pixels the tool changes; GRADIENT: where each is on the view)
