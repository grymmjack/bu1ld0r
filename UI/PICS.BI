''
' bu1ld0r - UI/PICS.BI
' =============================================================================
' Pictures on faces: the bin's PICTURES (the PNGs in pictures/, in folders),
' one dragged or clicked onto a face puts it there, fitted to the face (a
' shape becomes a mesh part to carry it); a PNG dropped on the window from
' the desktop is copied into pictures/ and put where it lands. With faces
' picked (E), the panel fits, spreads, turns, flips, repeats, slides or
' takes off their picture.
'
CONST BI_PIC = 4
DIM SHARED binTab ' (the bin's lower half: 0 the prefabs, 1 the pictures)
DIM SHARED binPicDir$ ' (the folder open in pictures/: "" or "walls/")
DIM SHARED pmRef$, pmDrag ' (the picture being put on a face; dragged from the bin)
DIM SHARED pcThumb&(MAX_PIC) ' (each picture's tile in the bin, BinTS square)
DIM SHARED dropFile$, dropWait ' (a file dropped on the window: dealt with a few frames on, once the pointer's where it landed)
CONST PT_FIT = 1, PT_ACROSS = 2, PT_TURN = 3, PT_FLIP = 4, PT_MORE = 5, PT_FEWER = 6, PT_LEFT = 7, PT_RIGHT = 8, PT_UP = 9, PT_DOWN = 10, PT_NONE = 11
CONST PT_DEFORM = 12, PT_MOVE = 13, PT_DRAW = 14 ' (DRAW: the picture opened in DRAW - a new one if the face has none) ' (DEFORM: its corners pinned to the face's; MOVE: the mode below)
' The picture moved by hand (P, or MOVE PICTURE, in E with faces picked): a drag on a
' picked face slides it under the pointer, the wheel sizes it, Shift + wheel turns it
DIM SHARED pvOn, pvArm, pvDrag, pvF AS LONG, pvH AS V3, pvN AS V3, pvP0x#, pvP0y#, pvP0z#
DIM SHARED pvRx#, pvRy#, pvRz#, pvUx#, pvUy#, pvUz#, pvDuA#, pvDvA#, pvDuB#, pvDvB#, pvWheelT#
REDIM SHARED pvU0(0) AS SINGLE, pvV0(0) AS SINGLE ' (the spots when the drag began)

' Pictures being edited in DRAW: watched, and loaded again each time it saves them
CONST PW_MAX = 16
DIM SHARED pwN, pwRef$(PW_MAX), pwSig$(PW_MAX), pwNext#
DIM SHARED cfgDraw$ ' (DRAW's program: draw= in bu1ld0r.cfg, else ~/git/DRAW/DRAW.run)

' A folder outside pictures/ open in the bin (typed or pasted in its path box, or dropped
' on the window): its PNGs are copied into pictures/ when one's put on a face
CONST F_PICPATH = 25 ' (the bin's path box, under the tabs)
DIM SHARED binPicExt$ ' (that folder, from /, ending in /: "" - pictures/ is open)
DIM SHARED pmSrc$ ' (the outside picture pmRef$ was copied from: its tile shows it picked)
CONST XT_MAX = 96
DIM SHARED xtRef$(XT_MAX), xtImg&(XT_MAX), xtNext, xtLoads ' (outside pictures' tiles: a ring; loads this frame)
DIM SHARED picTS ' (the PICTURES tab's tiles, in pixels: Shift + wheel, pic_size= in bu1ld0r.cfg)
CONST PIC_TS_MIN = 40, PIC_TS_MAX = 256
DIM SHARED cfgKaleido$ ' (kaleidotron's program: kaleidotron= in bu1ld0r.cfg)
