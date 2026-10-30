''
' bu1ld0r - CORE/APP.BI
' =============================================================================
' The window, its layout, the colours, the mouse and keys as this frame saw
' them, and the messages along the bottom.
'
CONST APP_NAME$ = "bu1ld0r"
CONST APP_VERSION$ = "0.2.0"
CONST MIN_SW = 800, MIN_SH = 700 ' (the smallest our screen is laid out at)
CONST BIN_W = 150 ' (the bin, down the left)
CONST PANEL_W = 250 ' (the panel, down the right)
CONST TOP_H = 28, BAR_H = 26 ' (the bar along the top, the message line along the bottom)

TYPE V3
    x AS SINGLE
    y AS SINGLE
    z AS SINGLE
END TYPE

' The window, as DRAW's: our screen is scrW x scrH, drawn uiK times bigger
' (a whole number: square pixels) to fill it. Drag the window and, once
' it's let go, the screen is made again at the window's size / uiK and
' everything laid out again on it - the 3D view takes the room. The size
' and uiK are remembered in bu1ld0r.cfg (window=WxH, ui_scale=). winsize.h
' sets the window's size: QB64PE can't.
DECLARE LIBRARY "winsize"
    SUB winsize_set (BYVAL w AS LONG, BYVAL h AS LONG)
    FUNCTION winsize_w& ()
    FUNCTION winsize_h& ()
END DECLARE
DIM SHARED scrW, scrH, scrImg&, uiK ' (our screen, and how many times bigger the window shows it)
DIM SHARED winW, winH ' (the window's size, as we last set it)
DIM SHARED cfgWinW, cfgWinH, cfgUiK ' (bu1ld0r.cfg's window= and ui_scale=)
DIM SHARED preFullW, preFullH ' (our screen's size before full screen)

DIM SHARED appDir$ ' (where the program is: models/, export/ and bu1ld0r.cfg are beside it)
DIM SHARED neonDir$ ' (NEON-CASTER's asset folder, neon-caster/neon-caster: its export goes there - bu1ld0r.cfg's neon_dir=)
DIM SHARED quitWant
DIM SHARED vX0, vY0, vW, vH ' (the 3D view's rectangle on the screen)

' The mouse, this frame: where, which buttons are down, which went down
' (P) or up (R) since the last - read from _MOUSEINPUT's queue, so a quick
' click inside one frame still counts
DIM SHARED mX, mY, mB1, mB2, mB3, mP1, mP2, mP3, mR1, mR2, mR3, mWheel
DIM SHARED kShift, kCtrl, kAlt

DIM SHARED msgText$, msgT AS DOUBLE ' (the message line's words, and when they were put there)

DIM SHARED cBg AS _UNSIGNED LONG, cPanel AS _UNSIGNED LONG, cLine AS _UNSIGNED LONG, cText AS _UNSIGNED LONG
DIM SHARED cDim AS _UNSIGNED LONG, cHi AS _UNSIGNED LONG, cSel AS _UNSIGNED LONG, cBtn AS _UNSIGNED LONG
DIM SHARED cHover AS _UNSIGNED LONG, cWarn AS _UNSIGNED LONG

' The command line's (tests): --open FILE, --export, --shot FILE, --quit, --neon DIR
DIM SHARED argOpen$, argExport, argShot$, argQuit, argFrames

' Words of a line split at spaces (Words): wd$(1 to wdN)
DIM SHARED wd$(40), wdN
