''
' bu1ld0r - OUT/TIDY.BI
' =============================================================================
' The model tidied for the game, the last thing before it's exported (and,
' with T, in the view): faces hidden inside other parts or pressed against
' them taken away; corners welded (and a corner lying on a neighbour's edge
' put in it, so nothing's left with a crack); flat neighbours of one colour
' made one, and cut again into as few triangles as they can be; slivers
' taken out - and, if it's still over the model's budget, edges collapsed,
' the one that moves the shape least first (colour borders and open edges
' kept), until it's in, or until the next would show. The .bld keeps the
' parts as built: only the export is tidied.
'
CONST TD_BUDGET = 200 ' (a new model's: NEON-CASTER keeps a prop near 200 triangles)
CONST TD_SHORT = .0015 ' (an edge shorter than this, of a cell, is a sliver's: collapsed)
CONST TD_SHOW = .003 ' (a collapse that would move the shape more than this, of the model's size, isn't made)
CONST TD_LOCAL = .08 ' (nor more than this of the edge's own length: small details stay)
DIM SHARED mdlBudget AS LONG, txtBudget AS LONG ' (the model's budget, 0: none; a .bld's "budget N" as read, -1: none)
CONST F_BUDGET = 24 ' (the panel's field for it, with nothing selected)
DIM SHARED txtTidy
DIM SHARED mdlTidy ' (EXPORT sends it tidied: "tidy 1" in the .bld - else as built)
DIM SHARED tidyView, tidyNow ' (T: the view shows the model tidied; the export's own)
DIM SHARED tdHold AS LONG ' (triangles with a picture on them: kept as they are)
DIM SHARED tdIn AS LONG, tdOut AS LONG, tdMs AS LONG ' (the last tidy: triangles before and after, how long it took)

' Hidden faces: each solid's triangles (one after another: tSol) and their box; rnPart its tSol
REDIM SHARED tdHid(0) AS _BYTE
REDIM SHARED rnT0(0) AS LONG, rnT1(0) AS LONG, rnPart(0) AS LONG, rnLo(0) AS V3, rnHi(0) AS V3
DIM SHARED rnN AS LONG

' The tidied triangles: corners 3t to 3t + 2 of tdV (the work's points)
REDIM SHARED tdV(0) AS LONG, tdCol(0) AS _UNSIGNED LONG, tdPart(0) AS LONG, tdLive(0) AS _BYTE
DIM SHARED tdN AS LONG, tdLiveN AS LONG
REDIM SHARED tdHead(0) AS LONG, tdNext(0) AS LONG ' (each point's corners: slot 3t + c, linked; 0 ends it)
REDIM SHARED tdDead(0) AS _BYTE, tdVer(0) AS LONG, tdMark(0) AS LONG
DIM SHARED tdStamp AS LONG
REDIM SHARED tdQ(0) AS DOUBLE ' (each point's quadric - the planes round it, how far from them: 10 numbers, then their weight)
REDIM SHARED tdOrd(0) AS LONG, tdUse(0) AS LONG, tdLin(0) AS LONG ' (points by x; how many polygons use each, and how many on a straight edge)
CONST TD_TJ = 256
DIM SHARED tjW(TD_TJ) AS LONG, tjS(TD_TJ) AS DOUBLE ' (the points on an edge, from its start)

' A point's neighbours: each edge out, how many triangles have it, its colours
CONST TD_NB = 512
DIM SHARED nbW(TD_NB) AS LONG, nbCnt(TD_NB) AS LONG, nbCol(TD_NB) AS _UNSIGNED LONG, nbMix(TD_NB) AS _BYTE, nbN AS LONG, nbOver

' The edges to collapse, cheapest first (a heap); each with its points' versions when it was costed
REDIM SHARED hpE(0) AS DOUBLE, hpU(0) AS LONG, hpV(0) AS LONG, hpSU(0) AS LONG, hpSV(0) AS LONG
DIM SHARED hpN AS LONG
