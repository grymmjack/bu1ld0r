''
' bu1ld0r - MODEL/SHAPES.BI
' =============================================================================
' The shapes past the first six: the dice (DIE: 4 to 30 faces), and the
' smart shapes after DRAW's (MODEL/SHAPES.BM).
'
CONST DIE_KINDS = 7, DIE_MAXP = 32, DIE_MAXF = 30, DIE_MAXC = 6
DIM SHARED dieN(DIE_KINDS) AS INTEGER ' (4 6 8 10 12 20 30)
DIM SHARED dieSc(DIE_KINDS) AS DOUBLE ' (each one's size, made: ShapeFit)
DIM SHARED dieEX(DIE_KINDS) AS DOUBLE, dieEY(DIE_KINDS) AS DOUBLE, dieEZ(DIE_KINDS) AS DOUBLE ' (its own proportions, times dieSc - it fills its box)
DIM SHARED spAX#(DIE_MAXF), spAY#(DIE_MAXF), spAZ#(DIE_MAXF), spCX#, spCY#, spCZ# ' (a spike's points: SpikeMake)
DIM SHARED dieMade(DIE_KINDS) AS INTEGER, dieFN(DIE_KINDS) AS INTEGER
DIM SHARED dieX(DIE_KINDS, DIE_MAXP) AS DOUBLE, dieY(DIE_KINDS, DIE_MAXP) AS DOUBLE, dieZ(DIE_KINDS, DIE_MAXP) AS DOUBLE
DIM SHARED dieFC(DIE_KINDS, DIE_MAXF) AS INTEGER, dieFV(DIE_KINDS, DIE_MAXF, DIE_MAXC) AS INTEGER ' (each face's corners, anticlockwise from outside)
DIM SHARED dieNX(DIE_KINDS, DIE_MAXF) AS DOUBLE, dieNY(DIE_KINDS, DIE_MAXF) AS DOUBLE, dieNZ(DIE_KINDS, DIE_MAXF) AS DOUBLE
REDIM SHARED shX(300) AS SINGLE, shY(300) AS SINGLE, shZ(300) AS SINGLE ' (a shape's points while it's made)
