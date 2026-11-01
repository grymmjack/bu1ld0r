''
' bu1ld0r - UI/FIX.BI
' =============================================================================
' FIX THIS (F2, or FIX in the top bar): the report card's checks
' (tools/c0nstruct0r/report.py - the same numbers) run on the model as EXPORT
' makes it - hidden parts too, tidied if it's to be. Each finding says what
' it means; SHOW selects the parts carrying it; a fix where bu1ld0r can make
' one alone: MAKE PLAIN (smeared faces their pixels' colour), SQUARE UP (faces
' a few degrees off square or 45 made true), KEEP L / KEEP R (one half, as
' seen from the front, mirrored over the other), TIDY (the export cut to the
' budget). LEAVE: meant as it is - out of the score, kept in the .bld
' (fixleave ...). Checked again a moment after each change. A fix works on
' the selected parts, or the whole model with none selected.

CONST FX_N = 7 ' (1 SMEAR, 2 PIXEL SIZE, 3 ANGLES, 4 SYMMETRY, 5 TRIANGLES, 6 PICTURES, 7 REPEATS)
DIM SHARED fxOn, fxHot, fxSig$, fxSigAt$, fxDue#, fxHave
DIM SHARED fxV(FX_N) AS SINGLE ' (each finding: a % - TRIANGLES the count, PICTURES how many)
DIM SHARED fxScore AS SINGLE, fxTris AS LONG, fxBudget AS LONG, fxPxc AS SINGLE, fxPlain AS SINGLE, fxColour AS SINGLE, fxOver AS SINGLE
DIM SHARED fxMidX AS DOUBLE, fxSpan AS DOUBLE ' (where SYMMETRY's mirror stands - x 0 if the model's across it, else its middle - and the model's size)
DIM SHARED fxTwinless AS LONG ' (parts with no mirror twin)
REDIM SHARED fxPF(0) AS _BYTE ' (part x 8 + finding: that part carries it - SHOW)
REDIM SHARED fxTF(0) AS _BYTE ' (each triangle the check saw: 1 smeared)
REDIM SHARED fxBL(0) AS V3, fxBH(0) AS V3, fxBK(0) AS _BYTE ' (each part's box in the world, from its triangles; fxBK: it has some)
DIM SHARED fxG(1, 63, 63) AS _BYTE, fxGW(1), fxGH(1), fxGA(1) AS SINGLE ' (the outlines from the front and above: 1 filled, 2 not mirrored; fxGA each one's %)
DIM SHARED fxQX(25) AS DOUBLE, fxQY(25) AS DOUBLE, fxQZ(25) AS DOUBLE, fxQN ' (the 26 nice ways: square and 45)
DIM SHARED fxNewId AS LONG, fxRoundN AS LONG ' (FxSquareMesh&: the mesh made, faces left as round things' facets)
DIM SHARED mdlLeave$ ' (the findings left as they are, words between spaces: " smear asym ")
