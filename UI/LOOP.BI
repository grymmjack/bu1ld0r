''
' bu1ld0r - UI/LOOP.BI
' =============================================================================
' LOOP (O, in E with an edge picked): a ring of new edges round the part,
' across the picked edge - through it, and on through each four-sided face
' to the side opposite, and the face past that, till it comes round or meets
' a face that isn't four-sided (or the shape's open edge). A mode, as BEVEL
' is (it shares bevel's - bvKind 2): POSITION slides the cut from one side
' of the faces to the other, CUTS makes more of them, evenly; shown as it
' would be. APPLY (Enter) makes it, its new edges picked; Esc: as it was.
'
CONST LC_MAX = 10, LC_K = 12 ' (LC_K: room for each edge's points, its two ends and the cuts)
DIM SHARED lcPos, lcCuts, lcNS AS LONG, lcEN AS LONG, lcFN AS LONG
REDIM SHARED lcSA(0) AS LONG, lcSB(0) AS LONG ' (the picked edges it began on - the work's points, as read from bvBase)
REDIM SHARED lcP(0) AS LONG, lcQ(0) AS LONG ' (the ring's edges, each from the side its cuts are measured from)
REDIM SHARED lcF(0) AS LONG, lcFA(0) AS LONG, lcFB(0) AS LONG ' (the ring's faces, each between two of its edges)
REDIM SHARED lcC(0) AS LONG ' (each edge's points in turn: lcC(e * LC_K + j) - j 0 its p, 1.. the cuts, cuts + 1 its q)
REDIM SHARED lcUsed(0) AS _BYTE, lcNew(0) AS _BYTE ' (the work's faces in a ring; its points made by the cut)
