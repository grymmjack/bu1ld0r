''
' bu1ld0r - VIEW/VIEW.BI
' =============================================================================
' The camera, and drawing: every triangle filled pixel by pixel into an
' image, nearest wins (rZ, a depth buffer), and which triangle won each
' pixel kept too (rId) - so the pointer's pixel says which part, and where.
'
CONST R_MAX = 1310720 ' (pixels, the biggest picture drawn: the view, an icon, a model's picture)

DIM SHARED camTX, camTY, camTZ, camYaw, camPitch, camDist, camFov
DIM SHARED cEX, cEY, cEZ, cFX, cFY, cFZ, cRX, cRY, cRZ, cUX, cUY, cUZ ' (eye, forward, right, up)
DIM SHARED cFoc, cMidX, cMidY ' (the focal length in pixels, the picture's middle)

' What a drawing goes into: rImg& (rW x rH), its depth and triangle per pixel
DIM SHARED rImg&, rW, rH, rMem AS _MEM
DIM SHARED rZ(R_MAX) AS SINGLE, rId(R_MAX) AS LONG
DIM SHARED rPart(R_MAX) AS INTEGER ' (the outlines' work: each pixel's part)
DIM SHARED rOrtho, rSpan ' (rOrtho: a model's picture - flat, rSpan cells across)
DIM SHARED rLX, rLY, rLZ ' (the light: which way it comes from)
DIM SHARED rShadeLo, rShadeK ' (shade = lo + k x lit)
DIM SHARED rCull ' (faces turned away left out)
DIM SHARED rGhost ' (drawing the ghost: see-through, and not in rId)

DIM SHARED viewImg&, ovImg&, viewDirty, ovDirty
DIM SHARED hoverPart, hoverTri AS LONG
