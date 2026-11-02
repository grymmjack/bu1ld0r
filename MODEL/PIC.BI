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
DIM SHARED picDirty(MAX_PIC) ' (painted on the model since it was read: saved with the model - PicSaveDirty)
' Each picture's file as it was read (time ms, bytes): one saved since by another program is read again
' (PicFresh: every 2 s in PicWatchFrame, and before the port's picture command maps it)
DIM SHARED picStT#(MAX_PIC), picStB#(MAX_PIC), picStNext#
DECLARE LIBRARY "../CORE/filestamp"
    FUNCTION FileTimeMs# (p$)
    FUNCTION FileBytes# (p$)
END DECLARE
