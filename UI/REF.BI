''
' bu1ld0r - UI/REF.BI
' =============================================================================
' Reference pictures, to model over: one on the ground (B), one on the back
' wall (L - on your left as the view opens), one on the side wall (R - on
' your right). Drawn see-through on their planes behind everything (before
' the grid), each its own opacity, place and size; saved in the model's .bld
' (`ref K OPACITY SHOWN A B WIDTH PATH`). The controls sit in the view's top
' right: [REF] (opacity) [TR] [B][L][R] - B / L / R pick which one the rest
' work on (Shift+click: hide / show it), REF picks a picture from disk for it
' (a PICTURES tile or a file dropped on REF too; right-click: none; Shift+
' click: hide / show them all), TR moves it (drag, arrows: on its plane; the
' wheel sizes it). A, B: its middle along the plane's two ways - ground x, z;
' back wall x, y; side wall z, y. The picture's right is -A (as seen from the
' side the view opens on), its top +B.
'
CONST REF_PX = 1048576 ' (each picture's room in refPix: 1024 x 1024 - bigger ones are shrunk)
DIM SHARED refPath$(2), refOp(2), refShow(2), refA#(2), refB#(2), refW#(2), refPW(2), refPH(2)
DIM SHARED refSel, refTr, refHideAll, refSlide, refDrag, refDA#, refDB#, refHA#, refHB#, refLock
REDIM SHARED refPix(0) AS _UNSIGNED LONG
