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
CONST NEON_TRI_WARN = 600 ' (NEON-CASTER keeps a prop near 200 triangles; every model it loads shares 16,000)

DIM SHARED exCol(EX_COLS - 1) AS _UNSIGNED LONG, exColN
DIM SHARED exFrame ' (how many cells across the 8 pictures are)
