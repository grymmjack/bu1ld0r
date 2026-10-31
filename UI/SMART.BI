''
' bu1ld0r - UI/SMART.BI
' =============================================================================
' SMART GUIDES ([SG] in the top bar, as DRAW's): while parts are dragged,
' the selection's box - its low side, middle and high side on each way it can
' move - is held against every other part's box (their low, middle and high,
' so sides line up, middles line up, or one sits on / beside the other) and
' the world's zero. Within SG_PX screen pixels it snaps there (before the
' grid) and a dashed line shows what lined up with what. Alt: free.
'
CONST SG_PX = 7 ' (how near, in screen pixels, a side must come to snap)
CONST SG_MAXG = 24 ' (guides shown at once)
DIM SHARED sgOn ' (on: smart_guides= in the cfg)
DIM SHARED sgBN AS LONG ' (the other parts' boxes: 1..sgBN; box 0 is the world's zero)
REDIM SHARED sgLo(0, 3) AS DOUBLE, sgHi(0, 3) AS DOUBLE
DIM SHARED sgML#(3), sgMH#(3) ' (the moving selection's box when the drag began)
DIM SHARED sgGN, sgGA(SG_MAXG), sgGB(SG_MAXG) AS LONG, sgGV#(SG_MAXG) ' (this frame's guides: axis, box, where)
DIM SHARED sgD#(3) ' (the drag's move this frame, for drawing)
