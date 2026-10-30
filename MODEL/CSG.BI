''
' bu1ld0r - MODEL/CSG.BI
' =============================================================================
' Holes: one solid's faces less another's. Faces are polygons here - flat,
' convex, any number of corners - in a pool used as a stack (a cut takes
' from the top and gives it all back when it's made its triangles).
'
CONST CSG_EPS = 0.0001 ' (nearer a plane than this is on it: a ten-thousandth of a cell)
CONST CSG_ON = 0, CSG_FRONT = 1, CSG_BACK = 2, CSG_SPAN = 3

' Polygons: their plane (n . p = w), their corners (from cgV0, cgVn of them),
' the next in whatever list they're in, and what they came from
REDIM SHARED cgNx(0) AS DOUBLE, cgNy(0) AS DOUBLE, cgNz(0) AS DOUBLE, cgW(0) AS DOUBLE
REDIM SHARED cgV0(0) AS LONG, cgVn(0) AS INTEGER, cgNext(0) AS LONG
REDIM SHARED cgPart(0) AS INTEGER, cgFace(0) AS INTEGER, cgCol(0) AS _UNSIGNED LONG, cgCut(0) AS INTEGER
REDIM SHARED cgPar(0) AS LONG, cgOn(0) AS INTEGER ' (a piece: the face it was split from; lying on the other's surface)
DIM SHARED cgTop AS LONG, cgCap AS LONG

' Corners: where, and whether the edge from it to the next is one of the shape's own
REDIM SHARED cvX(0) AS DOUBLE, cvY(0) AS DOUBLE, cvZ(0) AS DOUBLE, cvE(0) AS INTEGER
DIM SHARED cvTop AS LONG, cvCap AS LONG

' A split's work: one polygon's corners - how far in front, which side - and its two pieces
CONST CSG_MAXV = 256
DIM SHARED csT(CSG_MAXV + 4) AS DOUBLE, csP(CSG_MAXV + 4) AS INTEGER
DIM SHARED csFX(CSG_MAXV + 4) AS DOUBLE, csFY(CSG_MAXV + 4) AS DOUBLE, csFZ(CSG_MAXV + 4) AS DOUBLE, csFE(CSG_MAXV + 4) AS INTEGER
DIM SHARED csBX(CSG_MAXV + 4) AS DOUBLE, csBY(CSG_MAXV + 4) AS DOUBLE, csBZ(CSG_MAXV + 4) AS DOUBLE, csBE(CSG_MAXV + 4) AS INTEGER

' The near faces of both: their boxes, and which meet which (each one's
' list in csAdj, csAdN of them from csAd0); which faces lost a piece
REDIM SHARED csXP(0) AS LONG, csXLo(0) AS V3, csXHi(0) AS V3, csAd0(0) AS LONG, csAdN(0) AS LONG
REDIM SHARED csPrI(0) AS LONG, csPrJ(0) AS LONG, csAdj(0) AS LONG
DIM SHARED csXCap AS LONG, csPrCap AS LONG, csPrN AS LONG
REDIM SHARED csGone(0) AS _BYTE, csDone(0) AS _BYTE
DIM SHARED csGoneCap AS LONG

' The inside tests: both solids as triangles (a corner, two sides), and a
' grid over x and z of each (the rays go up, all but straight: each looks
' only at what's in its cell)
REDIM SHARED rbAx(0) AS DOUBLE, rbAy(0) AS DOUBLE, rbAz(0) AS DOUBLE, rbUx(0) AS DOUBLE, rbUy(0) AS DOUBLE, rbUz(0) AS DOUBLE
REDIM SHARED rbVx(0) AS DOUBLE, rbVy(0) AS DOUBLE, rbVz(0) AS DOUBLE
DIM SHARED rbN AS LONG, rbCap AS LONG
CONST CSG_GRID = 24
DIM SHARED rgX0(1) AS DOUBLE, rgZ0(1) AS DOUBLE, rgCW(1) AS DOUBLE, rgCH(1) AS DOUBLE, rgLo(1) AS V3, rgHi(1) AS V3
DIM SHARED rgStart(1, CSG_GRID * CSG_GRID) AS LONG
REDIM SHARED rgIdx(0) AS LONG
DIM SHARED rgIdxCap AS LONG
