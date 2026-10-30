''
' bu1ld0r - MODEL/PIC.BI
' =============================================================================
' Pictures on faces: each PNG used, by its name in pictures/ (no .png -
' "neon/crate"), loaded once into picPix (fast to read a pixel of). A face
' with one has a texture spot (u, v: 0 to 1 across, v from the top) at each
' corner. One that's gone missing keeps its name (it's saved again as it
' was) and the face shows its colour.
'
CONST MAX_PIC = 256
DIM SHARED picN, picRef$(MAX_PIC), picW(MAX_PIC) AS LONG, picH(MAX_PIC) AS LONG, picOff(MAX_PIC) AS LONG
REDIM SHARED picPix(0) AS _UNSIGNED LONG
DIM SHARED picTop AS LONG
