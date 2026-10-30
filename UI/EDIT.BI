''
' bu1ld0r - UI/EDIT.BI
' =============================================================================
' Editing one part's faces, edges and points (E): the part made a mesh part if it
' isn't one, then its faces (or its points) picked - click, Shift adds, or
' drag a box round them - and moved, sized, turned, pushed out along the
' way they face, extruded, inset, divided, merged, coloured.
'
CONST ED_POINTS = 1, ED_FACES = 2, ED_EDGES = 3 ' (edges: picked as their two points - they move, align and merge as points do)
DIM SHARED edEA AS LONG, edEB AS LONG ' (the edge EdEdgeAt found: its ends)
DIM SHARED edPart, edMode ' (the part being edited: 0 none)
REDIM SHARED edSelV(0) AS _BYTE, edSelF(0) AS _BYTE ' (its mesh's points and polygons picked, from 0)
DIM SHARED edVN AS LONG, edFN AS LONG, edId AS LONG ' (the mesh they're of)
DIM SHARED edArm, edDrag, edRect, edRX0, edRY0 ' (pressed on a picked one: a drag moves them; pressed on nothing: a box picks)
DIM SHARED edGen AS LONG ' (one more when the picking changes)
DIM SHARED edBoxKey$, edLo AS V3, edHi AS V3, edCnt AS LONG ' (the picked points' box in the world, and how many)
REDIM SHARED wsV(0) AS _BYTE, wsF(0) AS _BYTE ' (the picking as the work has it, while an edit's made)
REDIM SHARED edMv(0) AS _BYTE ' (the work's points an edit moves)
REDIM SHARED edX0(0) AS DOUBLE, edY0(0) AS DOUBLE, edZ0(0) AS DOUBLE ' (where they were in the world when a drag began)
DIM SHARED edWheelT AS DOUBLE, edWheelF ' (a run of wheel turns: one undo step)
REDIM SHARED edPkA(0) AS LONG, edPkB(0) AS LONG ' (the edges clicked in EDGES, in turn - the mesh's points: two opposite sides of a four-sided face picked pick all its corners, and these say which sides were meant)
REDIM SHARED wkPkA(0) AS LONG, wkPkB(0) AS LONG ' (the same while an edit's made: the work's points)
DIM SHARED edPkN AS LONG, wkPkN AS LONG
REDIM SHARED edPkIn(0) AS _BYTE ' (the mesh's points on a clicked edge still picked: EdPkInMake)
