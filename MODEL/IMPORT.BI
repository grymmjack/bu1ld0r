''
' bu1ld0r - MODEL/IMPORT.BI
' =============================================================================
' A NEON-CASTER prop (or any OBJ) opened as a model: its triangles become
' mesh parts - one for each piece that doesn't touch the others, all one
' group - with its texture on them (copied into pictures/neon/), so its
' faces and points can be edited and it can be exported again.
'
DIM SHARED neonIn$ ' (where OPEN finds NEON-CASTER's props: neon_dir=, else ~/git/neon-caster/neon-caster/ if it's there)
CONST IM_PIECES = 64 ' (more pieces than this: the prop is one part)
REDIM SHARED imX(0) AS SINGLE, imY(0) AS SINGLE, imZ(0) AS SINGLE, imU(0) AS SINGLE, imV(0) AS SINGLE
REDIM SHARED imCV(0) AS LONG, imCT(0) AS LONG ' (each triangle's 3 corners: point, spot)
REDIM SHARED imUp(0) AS LONG, imPc(0) AS LONG, imW(0) AS LONG ' (pieces: each welded point's parent, each triangle's piece, each corner's welded point)
