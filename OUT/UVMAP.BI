''
' bu1ld0r - OUT/UVMAP.BI
' =============================================================================
' UV DRAW (Ctrl+U; the panel's UV DRAW): the selected parts' faces as a DRAW
' file to paint in. Each flat side (a PLANE: neighbouring faces on one plane)
' is its own layer, numbered; OUTLINES, NUMBERS and a LEGEND (a column beside
' the picture) are guides on top. The faces first get pixels of their own in
' one picture - uv/NAME.png, laid out flat (pixel for pixel where they can be)
' - unless they have them already (all one picture, no face's pixels another's).
' pictures/uv/NAME.draw is DRAW's own file (a PNG with a drAw chunk, written as
' its version 2: no tool state to carry); NAME.uv beside it says which pixels
' are which layer's. Each save in DRAW (watched) brings each side layer's
' pixels back - only its own: the guides, and paint off its side, never do.
' ("U" and "V" are a picture's across and down: x y z are the world's.)
'
CONST UV_MAXL = 60 ' (a layer a side up to this many; past it, a layer a way of facing)
CONST UV_LEG = 168 ' (a legend column: 21 letters of 8)
CONST UV_MAXPIC = 2048
CONST UV_WMAX = 8 ' (DRAW files watched)

TYPE UVSIDE
    p AS INTEGER ' (its part)
    q0 AS LONG ' (its first face in uq*, then uqNx)
    nx AS DOUBLE
    ny AS DOUBLE
    nz AS DOUBLE
    rx AS DOUBLE
    ry AS DOUBLE
    rz AS DOUBLE
    ux AS DOUBLE
    uy AS DOUBLE
    uz AS DOUBLE
    a0 AS DOUBLE ' (its box on its own plane: across, up)
    a1 AS DOUBLE
    b0 AS DOUBLE
    b1 AS DOUBLE
    area AS DOUBLE
    d AS DOUBLE ' (laid out flat: pixels a cell)
    d0 AS DOUBLE ' (as its picture shows it now - 0: none)
    dl AS DOUBLE ' (as laid out)
    num AS LONG ' (its number)
    ex AS INTEGER ' (kept pixel for pixel from picture k, its box from ox, oy)
    k AS INTEGER
    ox AS LONG
    oy AS LONG
    w AS LONG ' (its place: w x h at x, y - a pixel spare all round)
    h AS LONG
    x AS LONG
    y AS LONG
    lay AS INTEGER ' (its layer)
    cx AS LONG ' (where its number goes)
    cy AS LONG
    best AS DOUBLE
    bw AS LONG ' (how big it is on the picture: whether its number fits across)
    bh AS LONG
    col AS _UNSIGNED LONG
END TYPE

DIM SHARED uvN AS LONG, uqN AS LONG, uvLN, uvNoRun
REDIM SHARED uvS(0) AS UVSIDE
REDIM SHARED uqP(0) AS INTEGER, uqF(0) AS LONG, uqS(0) AS LONG, uqNx(0) AS LONG, uqK(0) AS INTEGER ' (each face: part, work polygon, side, the next of its side, its picture)
REDIM SHARED uvLName$(0)
DIM SHARED uvWN, uvWD$(UV_WMAX), uvWS$(UV_WMAX), uvWP$(UV_WMAX), uvWNext# ' (watched: the .draw, as last read, a change waiting to settle)
DIM SHARED argUv, argUvBack$
REDIM SHARED uvOwn(0) AS _UNSIGNED _BYTE ' (each pixel of the picture: whose layer)
DIM SHARED uvSnapK ' (the old copy of a picture being laid out again, read from as it's written)
