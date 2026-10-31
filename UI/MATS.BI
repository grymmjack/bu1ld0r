''
' bu1ld0r - UI/MATS.BI
' =============================================================================
' MATERIAL (Q, or the MATERIAL button): a mode, as BEVEL is. In E it sets the
' picked faces' material (all the part's faces if none are picked), else
' the selected parts' (pMat: on each of their faces with none of its own).
' Shown as it would be while the sliders move; APPLY (Enter / Q) makes it,
' one undo step; Esc puts it back. MODEL/MAT holds the values.

DIM SHARED maOn, maDrag, maInE, maHot, maN AS LONG
DIM SHARED maM AS _UNSIGNED LONG ' (the material being set)
DIM SHARED maBase AS LONG, maPrev AS LONG ' (in E: the mesh as it was, and the one shown)
REDIM SHARED maOld(0) AS _UNSIGNED LONG ' (outside E: each part's material as it was)
REDIM SHARED maT(0) AS _BYTE ' (in E: the faces it's for, from 0)
REDIM SHARED maSelF(0) AS _BYTE ' (in E: the faces picked, as they were)
