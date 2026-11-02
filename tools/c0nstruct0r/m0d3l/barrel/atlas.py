#!/usr/bin/python3
"""c0-barrel's one picture (pictures/c0nstruct0r/c0-barrel.png), from pixelmon's renders here.

  /usr/bin/python3 tools/c0nstruct0r/m0d3l/barrel/atlas.py [OUT.png]

About 300 pixels a cell everywhere (the export keeps one picture pixel for pixel):
  side    0,0     320 x 134  16 staves of 20 px (the drum: 1.07 cells round, 0.45 tall)
  lid     330,0   102 x 102  the lid's circle 86 px across (0.29 cells) in the middle
  iron    0,140   336 x 7    16 hoop faces of 21 px, a rivet on each
  can     340,140 48 x 39    the canister: 8 faces of 6 px
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'pictures', 'c0nstruct0r', 'c0-barrel.png')
rng = np.random.default_rng(7)

atlas = np.zeros((256, 512, 3), np.float32)
atlas[:] = (58, 30, 24)                                   # (the unused room: dark red-brown)

# side: each stave its own slice of the wood (so neighbours differ), a little lighter or
# darker, dark seams on its two edges, the ends darkened (the chime)
wood = np.asarray(Image.open(os.path.join(HERE, 'wood.png')).convert('RGB').resize((320, 640), Image.LANCZOS), np.float32)
W, H, N = 320, 134, 16
cw = W // N
for j in range(N):
    oy = int(rng.integers(0, 640 - H))
    ox = int(rng.integers(0, 320 - cw))
    col = wood[oy:oy + H, ox:ox + cw] * rng.uniform(0.86, 1.06)
    col[:, 0] *= 0.42
    col[:, -1] *= 0.42
    col[:, 1] *= 0.85
    atlas[0:H, j * cw:(j + 1) * cw] = col
for y in range(5):                                        # the ends: darker toward the rim
    k = 0.55 + 0.09 * y
    atlas[y, 0:W] *= k
    atlas[H - 1 - y, 0:W] *= k

# lid: the circle scaled to 86 px, padded so the rect's corners are the background
lid = Image.open(os.path.join(HERE, 'lid.png')).convert('RGB')
x0, x1, y0, y1 = 23, 493, 24, 495                         # the circle's box in the render
d = max(x1 - x0, y1 - y0) + 1
k = 86 / d
pad = Image.new('RGB', (1200, 1200), (40, 22, 18))
pad.paste(lid, (600 - (x0 + x1) // 2, 600 - (y0 + y1) // 2))
big = pad.resize((round(1200 * k), round(1200 * k)), Image.LANCZOS)
c = big.width // 2
atlas[0:102, 330:432] = np.asarray(big.crop((c - 51, c - 51, c + 51, c + 51)), np.float32)

# iron: the render's plain band, darkened, a rivet in each face's middle
iron = np.asarray(Image.open(os.path.join(HERE, 'iron.png')).convert('RGB'), np.float32)
band = Image.fromarray(iron[78:112].astype(np.uint8)).resize((336, 7), Image.LANCZOS)
ib = np.asarray(band, np.float32) * 0.62 + np.array((8, 4, 0), np.float32)
ib[0] *= 0.6
ib[-1] *= 0.6
for j in range(16):
    x = j * 21 + 10
    ib[2:5, x - 1:x + 2] = (92, 84, 78)
    ib[3, x] = (150, 140, 128)
    ib[5, x - 1:x + 2] *= 0.5
atlas[140:147, 0:336] = ib

# canister: the render's scuffed grey, a little darker, seams on its 8 faces
can = Image.fromarray(iron[130:200, 0:300].astype(np.uint8)).resize((48, 39), Image.LANCZOS)
cb = np.asarray(can, np.float32) * 0.8
for j in range(8):
    cb[:, j * 6] *= 0.7
cb[0:2] *= 0.6
cb[-2:] *= 0.6
atlas[140:179, 340:388] = cb

Image.fromarray(np.clip(atlas, 0, 255).astype(np.uint8)).save(OUT)
print(OUT)
