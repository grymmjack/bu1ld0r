''
' bu1ld0r - MODEL/MAT.BI
' =============================================================================
' MATERIALS (as Blender's Principled BSDF, what a game can show): each face
' can have eight values beside its colour and picture, 0-100% in 16 steps -
' SEE (see-through, blended), GLOW (lights itself, blooms), SHINE (how strong
' the light's highlight is), ROUGH (how wide it spreads), METAL (the
' highlight in the face's own colour, the face darker), BUMP (relief from its
' picture's light and dark), COAT (a sharp glossy layer over the rest, as car
' paint), SHEEN (soft light along its edges, as velvet). Packed in one
' _UNSIGNED LONG (mfMat / sfMat / tMat / cgMat), 4 bits each from the top in
' that order. 0 is a plain face, as before. Later, in a second file:
' REFRACT, SUBSURFACE, FILM, ANISO.
' The .bld writes it on a face's f line as m=SEE:GLOW:...:SHEEN (%), after its
' colour and picture (an older bu1ld0r skips the word). The export writes
' NAME_mat.png beside NAME_tex.png (PLAN.md stage 10: the file NEON-CASTER
' reads) and a .mtl material for each.
'
CONST MAT_PRESETS = 12
DIM SHARED matPreName$(MAT_PRESETS), matPre(MAT_PRESETS) AS _UNSIGNED LONG
