''
' bu1ld0r - MODEL/SVG.BI
' =============================================================================
' An SVG opened as a model (OPEN, a drop, --open F.svg): each filled shape
' (path, rect, circle, ellipse, polygon, polyline - through the transforms
' of it and its groups) a flat outline, holes found by what's inside what,
' made thick: a mesh part standing up facing the front, all one group, the
' whole 1 cell across. E then extrudes, insets... its faces as any mesh's.
'
CONST SV_THICK = .1 ' (how thick, of its size)
REDIM SHARED svPX(0) AS DOUBLE, svPY(0) AS DOUBLE ' (every outline's points, y up)
REDIM SHARED svR0(0) AS LONG, svRN(0) AS LONG, svRE(0) AS LONG ' (each outline: its first point, how many, whose)
REDIM SHARED svECol(0) AS _UNSIGNED LONG ' (each shape's fill)
DIM SHARED svPN AS LONG, svRC AS LONG, svEN AS LONG
DIM SHARED svT#(32, 5), svFill(32) AS _UNSIGNED LONG, svNone(32), svTop ' (groups: transform a b c d e f, fill)
DIM SHARED svM#(5) ' (the shape being read: its transform)
DIM SHARED svCurX#, svCurY#, svRing AS LONG ' (where the pen is; the outline being drawn: 0 none)
REDIM SHARED svTX(0) AS DOUBLE, svTY(0) AS DOUBLE ' (a cap's triangles, 3 points each)
DIM SHARED svTN AS LONG
REDIM SHARED svRA(0) AS DOUBLE, svRD(0) AS LONG, svRP(0) AS LONG ' (each outline's area - anticlockwise more than 0 - how many it's inside, the one it's straight inside)
REDIM SHARED svWX(0) AS DOUBLE, svWY(0) AS DOUBLE, svVX(0) AS DOUBLE, svVY(0) AS DOUBLE ' (a face being made: its outline, holes bridged in)
DIM SHARED svWN AS LONG, svHid(32), svOp(32), svDeep, svFull, svSrc$
