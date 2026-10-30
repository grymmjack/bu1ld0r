''
' bu1ld0r - UI/LIST.BI
' =============================================================================
' The parts list: a column between the bin and the view (L, or PARTS, shows
' and hides it) - every part by name, so one hidden inside another can still
' be picked; shown or hidden, solid or lines, renamed, put earlier or later
' (a hole cuts what's before it).
'
CONST LIST_W = 210, LIST_ROW = 18
CONST F_PNAME = 22 ' (a part's name, typed in its row)
DIM SHARED listOn, listTop, listEdit, listFollow
DIM SHARED listClickT AS DOUBLE, listClickP ' (a second click on the same row soon after: rename it)
' The rows: a part's, or a group's (a folder: its parts under it, unless it's shut)
DIM SHARED lrN, lrPart(MAX_PARTS * 2), lrHead(MAX_PARTS * 2) AS _BYTE, lrGrp(MAX_PARTS * 2)
DIM SHARED lrDone(MAX_PARTS) AS _BYTE, grpShut(MAX_PARTS) AS _BYTE ' (a group folded up: its parts' rows left out)
