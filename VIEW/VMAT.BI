''
' bu1ld0r - VIEW/VMAT.BI
' =============================================================================
' Faces with a material (MODEL/MAT), drawn in the view: see VMAT.BM.

DIM SHARED rMatOn ' (the view: materials drawn - bin icons and the export's own pictures leave it 0)
DIM SHARED rSeePass ' (drawing the see-through ones, far to near, after the rest)
DIM SHARED rSeeN AS LONG
REDIM SHARED rSeeT(0) AS LONG, rSeeD(0) AS SINGLE ' (each see-through triangle, and how far)
DIM SHARED rGlowN AS LONG ' (glowing triangles drawn: the halo's wanted)
DIM SHARED rGlX0 AS LONG, rGlY0 AS LONG, rGlX1 AS LONG, rGlY1 AS LONG ' (the box they cover on the view)
' The triangle being drawn's material, worked out once (0-1 each)
DIM SHARED rmSee, rmGlow, rmShine, rmRough, rmMetal, rmBump, rmCoat, rmSheen
DIM SHARED rmNX, rmNY, rmNZ, rmLit, rmDif, rmA, rmEx, rmSpk, rmEnv ' (its normal, light, diffuse, see-through 0-1 solid, highlight, the sky it reflects)
DIM SHARED rmBR, rmBG, rmBB ' (its colour)
DIM SHARED rmTx AS LONG, rmId AS LONG
DIM SHARED rmR(2), rmG(2), rmB(2) ' (a piece's corners: light added on top, 0-255)
REDIM SHARED glR(0) AS SINGLE, glG(0) AS SINGLE, glB(0) AS SINGLE, glT(0) AS SINGLE ' (the glow, a quarter size)
