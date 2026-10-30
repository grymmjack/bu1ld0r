''
' bu1ld0r - MODEL/EMESH.BI
' =============================================================================
' Mesh parts (K_MESH): a part that's its own polygons - corners shared, so
' moving one moves every face round it. Made from a shape (to edit its
' faces and corners), from a hole made for good (APPLY), from a prefab's
' use whose turns and sizes can't be one part's. Their points are in the
' part's own space (as a shape's 1 x 1 x 1 is): its place, turns and size
' still apply.
'
' Each mesh is kept in a pool, never changed once made (an undo step names
' it: "mesh=ID"); an edit makes a new one. The ones nothing names any more
' are let go (MeshGc) when a model or the prefabs are read in.
'
REDIM SHARED mbV0(0) AS LONG, mbVN(0) AS LONG, mbF0(0) AS LONG, mbFN(0) AS LONG ' (each mesh: its points and polygons in the pools)
DIM SHARED mbN AS LONG, mbCap AS LONG
REDIM SHARED mvX(0) AS SINGLE, mvY(0) AS SINGLE, mvZ(0) AS SINGLE ' (points)
DIM SHARED mvTop AS LONG, mvCap AS LONG
REDIM SHARED mfC0(0) AS LONG, mfCN(0) AS LONG, mfCol(0) AS _UNSIGNED LONG ' (polygons: their corners from mfC0, mfCN of them)
DIM SHARED mfTop AS LONG, mfCap AS LONG
REDIM SHARED mfTex(0) AS INTEGER ' (its picture: 0 none - MODEL/PIC)
REDIM SHARED mcTU(0) AS SINGLE, mcTV(0) AS SINGLE ' (each corner's spot on the picture)
REDIM SHARED mcV(0) AS LONG, mcE(0) AS _BYTE ' (corners: the point - its mesh's own number, from 0 - and whether the edge on to the next is the shape's own)
DIM SHARED mcTop AS LONG, mcCap AS LONG
DIM SHARED meshGen AS LONG ' (one more for each edit: the triangles are made again)
DIM SHARED mbLive AS LONG ' (points still named after the last MeshGc: when the pool's far past it, it's tidied)

' Making one from triangles: their corners welded, then flat neighbours
' joined across edges that aren't the shape's own (a quad's diagonal, a
' lid's spokes, a hole's cuts) - in these, as they're worked on
REDIM SHARED swX(0) AS DOUBLE, swY(0) AS DOUBLE, swZ(0) AS DOUBLE, swKX(0) AS LONG, swKY(0) AS LONG, swKZ(0) AS LONG
DIM SHARED swN AS LONG, swCap AS LONG
REDIM SHARED swHash(0) AS LONG
REDIM SHARED sfC0(0) AS LONG, sfCN(0) AS LONG, sfCol(0) AS _UNSIGNED LONG, sfLive(0) AS _BYTE, sfBusy(0) AS _BYTE
REDIM SHARED sfNx(0) AS DOUBLE, sfNy(0) AS DOUBLE, sfNz(0) AS DOUBLE
REDIM SHARED sfTag(0) AS LONG ' (whose it is: the export's tidying keeps each polygon's part)
DIM SHARED emTag AS LONG ' (what EmAddF tags a polygon with)
DIM SHARED sfN AS LONG, sfCap AS LONG
REDIM SHARED sfTex(0) AS INTEGER, scTU(0) AS SINGLE, scTV(0) AS SINGLE ' (a polygon's picture, each corner's spot on it)
REDIM SHARED scV(0) AS LONG, scE(0) AS _BYTE
DIM SHARED scTop AS LONG, scCap AS LONG
REDIM SHARED swMap(0) AS LONG, sfMap(0) AS LONG ' (EmWrite: where each work point and polygon went in the mesh made, -1 gone)
REDIM SHARED seKey(0) AS _INTEGER64, seVal(0) AS LONG ' (the edges: u to v, the polygon and corner)
CONST EM_MAXC = 4096 ' (a polygon's corners, at most)
DIM SHARED emU(EM_MAXC) AS SINGLE, emW(EM_MAXC) AS SINGLE, emTex ' (its corners' spots, its picture: EmAddF takes them, then emTex is 0 again)
DIM SHARED emL(EM_MAXC) AS LONG, emE(EM_MAXC) AS INTEGER ' (a polygon being put together)
DIM SHARED emX(EM_MAXC) AS DOUBLE, emY(EM_MAXC) AS DOUBLE, emR(EM_MAXC) AS LONG ' (a polygon being cut into triangles: flat, and which corners are left)
