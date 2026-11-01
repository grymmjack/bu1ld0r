''
' bu1ld0r - UI/REMOTE.BI
' =============================================================================
' c0nstruct0r's port (C0NSTRUCT0R.md): with --port (or port= in the cfg)
' bu1ld0r listens on a local TCP port, and a program on this computer -
' c0nstruct0r - drives it a line at a time: "add box 0 0 0", "edit 3",
' "pick facing 0 0 -1", "extrude 0.05"... each answered with a line, "ok"
' or "err why" (queries: "ok" and JSON). Only 127.0.0.1, and only after
' "hello TOKEN" (the token, and the port, in c0nstruct0r.port beside the
' program). While it has control ("take") bu1ld0r takes no keys, clicks or
' wheel but Esc, which hands the model back to Rick (F9: let it go on). A
' strip over the view's foot says what it's doing ("say"). Every change is
' one undo step, and it waits a moment after each (pace) so it can be seen.
'
CONST RC_PORT0 = 47800 ' (the first port tried: the next nine if it's taken)
DIM SHARED rcHostH AS LONG, rcConnH AS LONG, rcPort, rcToken$, rcBuf$, rcAuth
DIM SHARED rcLock, rcStopped ' (it has the model; Rick took it back with Esc - F9 lets it go on)
DIM SHARED rcStrip$, rcPace, rcNextT# ' (what it says it's doing; ms waited after each change)
DIM SHARED rcShotF$, rcShotN, rcShotHow, rcGuides ' (a picture being taken, frames to go; 1 the window, 2 clean - no guides)
DIM SHARED argPort, cfgPort
DIM SHARED rcA$(64), rcAN ' (the command's words)
