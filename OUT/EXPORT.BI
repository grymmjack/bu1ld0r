''
' bu1ld0r - OUT/EXPORT.BI
' =============================================================================
' EXPORT: the model as an OBJ (y up, its front towards -z, sizes in
' NEON-CASTER cells) with one texture - each colour a square of it - and,
' when bu1ld0r.cfg names NEON-CASTER's asset folder, as one of its props:
' the OBJ (with the "# frame" line the game reads), the texture at 64 and
' 256, and 8 pictures round it for the game's software renderer.
'
CONST EX_COLS = 64 ' (colours a texture holds: 8 x 8 squares)
CONST PIC_SIZE = 64, PIC_SS = 4 ' (the 8 pictures: 64 px, drawn 4 times bigger and shrunk)
REDIM SHARED woV(0) AS LONG ' (the OBJ's triangles: each corner's point)

DIM SHARED exCol(EX_COLS - 1) AS _UNSIGNED LONG, exColN
DIM SHARED exFrame ' (how many cells across the 8 pictures are)

' Pictures on the model (imported props' textures): the texture holds them too.
' exMode 0: colours only; 1: one picture, as it is, the colours in squares
' of it nothing uses (EX_BLK across); 2: a grid exGrid across - each picture
' a square of it, then the colours' square
CONST EX_PICS = 15, EX_BLK = 16
DIM SHARED exMode, exPicN, exPic(EX_PICS) AS INTEGER, exGrid, exBlk(EX_COLS - 1) AS INTEGER
