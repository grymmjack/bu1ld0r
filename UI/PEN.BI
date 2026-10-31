''
' bu1ld0r - UI/PEN.BI
' =============================================================================
' PEN (P, or the pen tile after the shapes): an outline drawn on the ground,
' as DRAW's pen - a click a corner, a click and drag a curve's handles (the
' other side mirrored; Ctrl: only the side dragged), on the snap. Clicking
' the first point (or Enter) closes it: a flat mesh part a snap step thick,
' selected, to size up (Y: thicker) or edit in E.
' With the pen out, a strip in the view (or R / E / L / P, Tab) picks the
' tool: RECT, ELLIPSE (filled, or an outline WIDTH wide - F) and LINE
' (WIDTH wide), each dragged on the ground (Shift: square / circle / 45
' degrees; Ctrl: from the middle) and made a flat part when let go; the
' tool stays out for the next.
'
CONST PEN_MAX = 256
DIM SHARED penOn, penN, penDown, penPX, penPY, penHot, penHOk, penHX#, penHZ#
' (penDown: 1 dragging the new point's handle, 2 the closing click's)
DIM SHARED penAX#(PEN_MAX), penAZ#(PEN_MAX) ' (each point)
DIM SHARED penOX#(PEN_MAX), penOZ#(PEN_MAX), penIX#(PEN_MAX), penIZ#(PEN_MAX) ' (its handles: out, in - on the point: none)
DIM SHARED penTool, penFill, penWid#, penSides ' (0 pen, 1 rect, 2 ellipse, 3 line; filled or an outline; how wide a line / outline; an ellipse's sides)
DIM SHARED pdOn, pdX0#, pdZ0#, pdX1#, pdZ1#, pdCtr ' (a shape being dragged: from, to; from its middle)
