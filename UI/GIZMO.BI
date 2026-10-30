''
' bu1ld0r - UI/GIZMO.BI
' =============================================================================
' Moving along one axis (as Blender): the widget's three arrows on what's
' selected (parts, or the picked points / faces in E) - drag one and it
' moves only that way - and X, Y or Z held while dragging does the same.
' The axis is drawn through it, with a tick at each snap step.
'
DIM SHARED gzAxis ' (the arrow grabbed: 1 x, 2 y, 3 z - 0 none)
DIM SHARED gzHover, gzOk, gzL, gzC AS V3 ' (the arrow under the pointer; the widget's middle and its arrows' length, in the world)
DIM SHARED dragAxis ' (the axis the drag keeps to now)
DIM SHARED dragLX0, dragLY0 ' (where in the view the drag began)
