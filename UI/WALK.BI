''
' bu1ld0r - UI/WALK.BI
' =============================================================================
' WALK and FLY (the buttons at the view's bottom left; V, Shift+V): the
' camera taken through the model as a game's. The mouse looks (its pointer
' hidden), WASD / the arrows move, Shift faster. FLY (as kaleidotron's free
' fly, neon-caster's editor): straight through anything, E / Space up,
' Q / C down, the wheel how fast. WALK: on the ground and the model's tops,
' gravity, Space jumps (`fpJN` grid steps high), walls stop you, a ledge
' under a fifth of your eye height is stepped up; the wheel makes you taller
' or shorter (your eye's height), [ ] the jump. Tab: the other one; Esc,
' V or a right click: back to orbiting, round a point in front of you.
'
DIM SHARED fpOn ' (0, 1 WALK, 2 FLY)
DIM SHARED fpX#, fpY#, fpZ# ' (WALK: your feet; FLY: your eye)
DIM SHARED fpVY#, fpGround, fpH#, fpJN, fpSpd#, fpT#, fpWarp, fpDist0
DIM SHARED fpLX, fpLY, fpCX, fpCY, fpWX, fpWY ' (the pointer last frame; where it landed after the last recentring; fpWarp: waiting for that, fpWX its first reading after)
DIM SHARED fpJump ' (Space pressed: a jump wanted)
DIM SHARED fpR#, fpBodyN ' (how wide you are - half; how many parts are your body)
DIM SHARED fpKd(255) AS _BYTE ' (letters held, by our own count of presses and releases, either case: Shift let go before W sends W's release as w, and _KEYDOWN(87) stayed held)
REDIM SHARED fpBody(0) AS _BYTE ' (the parts that are your body: not drawn, not bumped into)
