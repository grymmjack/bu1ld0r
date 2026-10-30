''
' bu1ld0r - MODEL/MESH.BI
' =============================================================================
' The model's triangles, where they are in the world: each knows its part,
' which face of it, its colour and which way it faces (out).
'
CONST MAX_TRI = 60000
DIM SHARED tA(MAX_TRI) AS V3, tB(MAX_TRI) AS V3, tC(MAX_TRI) AS V3, tNrm(MAX_TRI) AS V3
DIM SHARED tPart(MAX_TRI) AS INTEGER, tFace(MAX_TRI) AS INTEGER, tCol(MAX_TRI) AS _UNSIGNED LONG
DIM SHARED tN AS LONG ' (triangles in all: the model's, then the ghost's)
DIM SHARED sceneTN AS LONG ' (the model's alone: 1 to sceneTN)
DIM SHARED meshDirty, ghostOn

' The part being made into triangles: its size, turns and place
DIM SHARED mkPart, mkFace, mkCol AS _UNSIGNED LONG
DIM SHARED mkSX, mkSY, mkSZ, mkCX, mkSXr, mkCY, mkSYr, mkCZ, mkSZr, mkPX, mkPY, mkPZ

' A prefab's parts are made inside its use's place, turns and size: one
' level each (a prefab in a prefab is two), the innermost last
CONST MAX_USE_DEPTH = 8
DIM SHARED usN
DIM SHARED usSX(MAX_USE_DEPTH), usSY(MAX_USE_DEPTH), usSZ(MAX_USE_DEPTH), usPX(MAX_USE_DEPTH), usPY(MAX_USE_DEPTH), usPZ(MAX_USE_DEPTH)
DIM SHARED usCX(MAX_USE_DEPTH), usSXr(MAX_USE_DEPTH), usCY(MAX_USE_DEPTH), usSYr(MAX_USE_DEPTH), usCZ(MAX_USE_DEPTH), usSZr(MAX_USE_DEPTH)
