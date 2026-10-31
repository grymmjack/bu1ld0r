''
' bu1ld0r - UI/TEXT.BI
' =============================================================================
' TEXT (X, or the tile after the pen): type, pick a font (the list in the
' view, PgUp / PgDn), click the ground where it starts; Enter lays it down -
' each character a flat mesh part (MODEL/FONT's outlines, made solid as an
' SVG's), all one group: a click picks the word, Alt+click one letter to move
' it. Up / Down its size, Left / Right how thick, Tab lying or standing up.
'
DIM SHARED txOn, txBuf$, txFont, txSize#, txTh#, txUp, txScroll, txScanned
DIM SHARED txHave, txAX#, txAZ#, txHOk, txHX#, txHZ# ' (where it starts: clicked; where the pointer's on the ground)
DIM SHARED txRk$, txW# ' (what the rings were made for; the text's width)
