''
' bu1ld0r - MODEL/FONT.BI
' =============================================================================
' TrueType outlines, read from the file itself (QB64's _LOADFONT gives only
' pixels): the TEXT tool's letters. head / maxp / hhea / hmtx for sizes and
' advances, cmap (format 4 or 12) for which glyph a character is, loca + glyf
' for its outline - simple glyphs and composites (an accent on a letter),
' quadratic curves flattened. A font with PostScript outlines (an .otf with
' CFF, no glyf) isn't read. The outlines go into SVG's rings (svPX/svPY,
' svR0/svRN, svRE the character), made solid as an SVG's are.
'
CONST FT_MAX = 2000 ' (fonts listed at most)
DIM SHARED ftD$, ftOk, ftPath$ ' (the font file read; whether it's usable; which)
DIM SHARED ftUpem AS LONG, ftLocLong, ftNG AS LONG, ftNHM AS LONG, ftAsc AS LONG, ftDsc AS LONG
DIM SHARED ftHmtx AS LONG, ftLoca AS LONG, ftGlyf AS LONG, ftCm AS LONG, ftCmF, ftSym
DIM SHARED ftN, ftName$(FT_MAX), ftFile$(FT_MAX) ' (the fonts found: FontScan)
REDIM SHARED fgF(0) AS LONG, fgX#(0), fgY#(0) ' (the glyph being read: each point's flags, place)
