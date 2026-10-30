''
' bu1ld0r - MODEL/MESH.BI
' =============================================================================
' The model's triangles, where they are in the world: each knows its part,
' which face of it, its colour and which way it faces (out).
'
CONST MAX_TRI = 60000
DIM SHARED tA(MAX_TRI) AS V3, tB(MAX_TRI) AS V3, tC(MAX_TRI) AS V3, tNrm(MAX_TRI) AS V3
DIM SHARED tPart(MAX_TRI) AS INTEGER, tFace(MAX_TRI) AS INTEGER, tCol(MAX_TRI) AS _UNSIGNED LONG
DIM SHARED tEdge(MAX_TRI) AS INTEGER ' (which of its edges are the shape's own - 1 A-B, 2 B-C, 4 C-A - not a quad's diagonal or a lid's spoke: the wireframe draws those)
DIM SHARED tN AS LONG ' (triangles in all: the model's, its holes', then the ghost's)
DIM SHARED sceneTN AS LONG ' (the model's alone, holes cut: 1 to sceneTN - what's exported)
DIM SHARED holeTN AS LONG ' (then the holes themselves, to sceneTN + 1 to holeTN: drawn see-through)
DIM SHARED meshDirty, ghostOn
DIM SHARED meshAll ' (hidden parts too: the export's)
DIM SHARED meshKey$ ' (the model the triangles to holeTN were made from: if it's the same, only the ghost's are made again)

' The part being made into triangles: its size, turns and place
DIM SHARED mkPart, mkFace, mkCol AS _UNSIGNED LONG
DIM SHARED mkTriE, mkQuadE ' (the edges the next MkTri / MkQuad makes are real: 1 2 4 (8) round from its first corner - 7 and 15 usually)
DIM SHARED mkSX, mkSY, mkSZ, mkCX, mkSXr, mkCY, mkSYr, mkCZ, mkSZr, mkPX, mkPY, mkPZ

' A prefab's parts are made inside its use's place, turns and size: one
' level each (a prefab in a prefab is two), the innermost last
CONST MAX_USE_DEPTH = 8
DIM SHARED usN
DIM SHARED usSX(MAX_USE_DEPTH), usSY(MAX_USE_DEPTH), usSZ(MAX_USE_DEPTH), usPX(MAX_USE_DEPTH), usPY(MAX_USE_DEPTH), usPZ(MAX_USE_DEPTH)
DIM SHARED usCX(MAX_USE_DEPTH), usSXr(MAX_USE_DEPTH), usCY(MAX_USE_DEPTH), usSYr(MAX_USE_DEPTH), usCZ(MAX_USE_DEPTH), usSZr(MAX_USE_DEPTH)
