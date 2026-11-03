#!/usr/bin/python3
"""c0-bigmed's picture: a red tackle-box trauma kit. Laid out at 256 (K = 1, 340 px a cell), drawn at K.

  /usr/bin/python3 tools/c0nstruct0r/m0d3l/bigmed/atlas.py [K]   -> pictures/c0nstruct0r/c0-bigmed.png

Regions (K = 1; a face's region is its part's box side: the lid's sides count its raised panel):
  tray  front 0,0  back 0,47 (122.4 x 44.2)   +x 128,0  -x 128,47 (68 x 44.2)   bottom 128,144 (122.4 x 68)
  lid   front 0,94 back 0,119 (123.76 x 22.1) +x 128,94 -x 128,119 (69.36 x 22.1) top 0,144 (123.76 x 69.36)
  alu 200,0..256,60   latch 200,64 (13.6 square)   white 200,80..256,140   rubber 0,216..124,256
Hidden faces reuse them: the tray's top takes the bottom's, the lid's underside the top's.
Renders: ../medkit (red.png glossy red paint, alu.png brushed aluminium, rubber.png).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paint import Atlas  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
K = int(sys.argv[1]) if len(sys.argv) > 1 else 2
OUT = os.path.join(HERE, '../../../../pictures/c0nstruct0r/c0-bigmed.png')
a = Atlas(K=K, seed=23, here=os.path.join(HERE, '../medkit'))
RED_SRC, ALU, RUB = a.load('red.png'), a.load('alu.png'), a.load('rubber.png', (0, 120))
RED, WHITE, INK = (196, 28, 34), (244, 244, 240), (246, 246, 242)


def red(w, h):
    return a.tinted(RED_SRC, w, h, RED, 1.4)


def stripe(img, y, w, t=1.0):
    return a.rect(img, (0, y, w, y + t), INK, 0.95)


# -- tray: front with words either side of the raised cross; white pinstripes ------------
W, H = 122.4, 44.2
s = red(W, H)
stripe(s, 4.5, W); stripe(s, 39, W)
s = a.text(s, 'FIRST', 6.2, (6, 14, 44, 22), INK)          # +x side (screen left)
s = a.text(s, 'AID', 6.2, (6, 23, 44, 31), INK)
s = a.text(s, 'CREW', 6.2, (78, 14, 116, 22), INK)
s = a.text(s, 'MEDICAL', 6.2, (78, 23, 116, 31), INK)
a.put((0, 0), a.edge_dark(s, 3, 0.8))
# back: an inventory sticker and the stripes
s = red(W, H)
stripe(s, 4.5, W); stripe(s, 39, W)
s = a.label(s, (40, 10, 82, 34), [('ISS CHeCS  MED-02', 3.2), ('S/N 0417-BT', 2.6)], seed=7)
a.put((0, 47), a.edge_dark(s, 3, 0.8))
# ends (the raised crosses sit on them)
for x0, y0, seed in ((128, 0, 1), (128, 47, 2)):
    s = red(68, H)
    stripe(s, 4.5, 68); stripe(s, 39, 68)
    a.put((x0, y0), a.edge_dark(s, 3, 0.8))
# bottom: darker, worn
s = red(122.4, 68) * 0.78
s = a.text(s, 'NASA  JSC  SEG46117', 4, (0, 30, 122.4, 38), (225, 225, 222), alpha=0.6)
a.put((128, 144), a.edge_dark(s, 6, 0.7))

# -- lid: words on its front, sticker band on its back, the top's raised panel -----------
W, H = 123.76, 22.1
s = red(W, H)
stripe(s, 2.0, W, 0.8)                                           # the raised panel's edge
s = a.text(s, 'EMERGENCY  TRAUMA  KIT', 8.5, (0, 5, W, 19), INK)
a.put((0, 94), a.edge_dark(s, 2, 0.82))
s = red(W, H)
stripe(s, 2.0, W, 0.8)
s = a.text(s, 'CREW MEDICAL SYSTEM  -  RETURN TO MED BAY', 4.5, (0, 8, W, 16), INK, alpha=0.8)
a.put((0, 119), a.edge_dark(s, 2, 0.82))
for x0, y0 in ((128, 94), (128, 119)):
    s = red(69.36, H)
    stripe(s, 2.0, 69.36, 0.8)
    a.put((x0, y0), a.edge_dark(s, 2, 0.82))
# top (right is -x, far side up): the panel is the middle 75%; the handle crosses its middle
W, H = 123.76, 69.36
s = red(W, H)
px0, py0, px1, py1 = W * 0.125, H * 0.125, W * 0.875, H * 0.875
for b in ((px0, py0, px1, py0 + 0.9), (px0, py1 - 0.9, px1, py1), (px0, py0, px0 + 0.9, py1), (px1 - 0.9, py0, px1, py1)):
    a.rect(s, b, INK, 0.95)                                      # a pinstripe round the panel
a.cross(s, px0 + 11, H / 2, 15, 5, INK)
a.cross(s, px1 - 11, H / 2, 15, 5, INK)
s = a.text(s, 'TRAUMA KIT', 8, (px0 + 20, py0 + 3, px1 - 20, py0 + 15), INK)
s = a.text(s, 'CREW MEDICAL', 6, (px0 + 20, py1 - 14, px1 - 20, py1 - 4), INK)
a.put((0, 144), a.edge_dark(s, 3, 0.8))

# -- swatches ---------------------------------------------------------------------------
st = a.tinted(ALU, 56, 60, (218, 222, 228), 0.6)              # polished steel: brushed, no scratches
from scipy.ndimage import gaussian_filter1d                      # noqa: E402
sm = gaussian_filter1d(st, 4 * K, axis=0)                        # each pixel kept within 3% of its column's
st = np.clip(st, sm * 0.97, sm * 1.03)                           # neighbours above and below: no scratch lines
a.put((200, 0), st)
a.put((200, 64), a.latch(13.6, 13.6, ALU, (214, 218, 224)))
a.put((200, 80), a.painted(RED_SRC, 56, 60, WHITE, 1.4, 0.4))
a.put((0, 216), a.tinted(RUB, 124, 40, (56, 56, 59), 1.0))
a.save(os.path.normpath(OUT))
