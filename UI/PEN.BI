''
' bu1ld0r - UI/PEN.BI
' =============================================================================
' PEN (P, or the pen tile after the shapes): an outline drawn on the ground,
' as DRAW's pen - a click a corner, a click and drag a curve's handles (the
' other side mirrored; Ctrl: only the side dragged), on the snap. Clicking
' the first point (or Enter) closes it: a flat mesh part a snap step thick,
' selected, to size up (Y: thicker) or edit in E.
'
CONST PEN_MAX = 256
DIM SHARED penOn, penN, penDown, penPX, penPY, penHot, penHOk, penHX#, penHZ#
' (penDown: 1 dragging the new point's handle, 2 the closing click's)
DIM SHARED penAX#(PEN_MAX), penAZ#(PEN_MAX) ' (each point)
DIM SHARED penOX#(PEN_MAX), penOZ#(PEN_MAX), penIX#(PEN_MAX), penIZ#(PEN_MAX) ' (its handles: out, in - on the point: none)
