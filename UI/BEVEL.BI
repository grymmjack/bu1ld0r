''
' bu1ld0r - UI/BEVEL.BI
' =============================================================================
' BEVEL (B, in E with edges or faces picked): a mode, as MOVE IT is. The
' picked edges (faces: all their edges) are cut off - each face beside one
' moved in from it by WIDTH, and the gap filled by a strip of SEGMENTS
' faces (1: a flat chamfer; more: rounded). Where bevelled edges meet, a
' corner face fills in. Shown as it would be while the sliders move;
' APPLY (Enter) makes it, Esc leaves the part as it was.
'
CONST BV_SEGMAX = 10, BV_FAN = 512
DIM SHARED bvOn, bvBase AS LONG, bvPrev AS LONG, bvDrag, bvWs, bvSeg, bvMaxW#, bvNE AS LONG, bvPtMode, bvKind ' (bvKind: the mode is 1 BEVEL, 2 LOOP - UI/LOOP)
REDIM SHARED bvSelV(0) AS _BYTE, bvSelF(0) AS _BYTE ' (what was picked when it began: the part's mesh as it was)
REDIM SHARED bvEA(0) AS LONG, bvEB(0) AS LONG, bvEF1(0) AS LONG, bvEF2(0) AS LONG ' (each edge: its ends, the face going a to b, the one going b to a)
REDIM SHARED bvHK(0) AS _INTEGER64, bvHV(0) AS LONG ' (the edges by their ends)
REDIM SHARED bvRS(0) AS LONG, bvRC(0) AS LONG, bvRL(0) AS LONG ' (each corner of the work: what it's made - bvRC points from bvRS in bvRL; 0: as it was)
DIM SHARED bvRN AS LONG
REDIM SHARED bvPA(0) AS LONG, bvPB(0) AS LONG ' (each edge's ends' rounds: from the a-to-b face's side to the other's)
REDIM SHARED bvVM(0) AS _BYTE, bvVF(0) AS LONG ' (the work's points at an edge's end; a face each point's in)
DIM SHARED bfF(BV_FAN) AS LONG, bfK(BV_FAN) AS LONG, bfP(BV_FAN) AS LONG, bfN(BV_FAN) AS LONG, bfSl(BV_FAN) AS LONG, bfD AS LONG ' (the faces round a point, in turn)
REDIM SHARED bvSA(0) AS LONG, bvSB(0) AS LONG: DIM SHARED bvSN AS LONG ' (EDGES: the edges picked when it began - the work's points, as read from bvBase)
DIM SHARED bvFold AS LONG ' (edges left out: folded flat, two faces back to back)
