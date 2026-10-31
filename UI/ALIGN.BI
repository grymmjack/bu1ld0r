''
' bu1ld0r - UI/ALIGN.BI
' =============================================================================
' ALIGN, as the view shows it (a paint program's): left, centre, right, top,
' middle, bottom. Points picked: lined up on the line. Faces picked: each
' connected piece of them moved whole. Parts selected: each (a group as
' one) moved whole. One thing alone lines up with what it's in: a piece
' with its part, a part with the model.
'
CONST AL_LEFT = 1, AL_CENTRE = 2, AL_RIGHT = 3, AL_TOP = 4, AL_MIDDLE = 5, AL_BOTTOM = 6
DIM SHARED samFirst, smAx(3) ' (SAME: the part picked first - the one the others are made like; its X Y Z toggles)
