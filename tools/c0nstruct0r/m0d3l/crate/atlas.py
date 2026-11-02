#!/usr/bin/python3
"""c0-crate's one picture (pictures/c0nstruct0r/c0-crate.png), from pixelmon's pine here.

  /usr/bin/python3 tools/c0nstruct0r/m0d3l/crate/atlas.py [K] [OUT.png]

K = 2 (default): 512 x 512, 400 pixels a cell - sharp in bu1ld0r; the export writes the game's
256 x 256 from it. K = 1: 256 x 256, 200 a cell. The layout is the same either way (regions
below at K = 1, times K), so the model's mapping - spots are 0..1 of the picture - fits both.
Regions (x0, y0, x1, y1) - each the size of the faces it goes on:
  front  0,0,116,66      body -z (0.58 x 0.33): boards, TOP SECRET stencil
  back   120,0,236,66    body +z: FRAGILE / THIS SIDE UP
  end1   0,70,80,136     body +x (0.40 x 0.33): serial stencil
  end2   84,70,164,136   body -x
  vcleat 168,70,177,136  corner posts' sides (0.045 x 0.33), grain up and down
  lcleat 181,70,190,156  lid cleats' tops (0.045 x 0.432)
  endg   194,70,203,79   end grain (posts' tops, 0.045 x 0.045)
  lid    0,160,122,246   the top band's top (0.612 x 0.432): boards along x
  frame  126,160,248,246 the lips round the body (band tops / undersides): grain along each side
  bandh  0,247,122,256   bands' front / back (0.612 x 0.045); its top 3 rows the cleats' long sides
  bande  124,247,210,256 bands' ends (0.432 x 0.045)
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
K = int(sys.argv[1]) if len(sys.argv) > 1 else 2
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(REPO, 'pictures', 'c0nstruct0r', 'c0-crate.png')
FONT = os.path.expanduser('~/.local/share/fonts/d/DINNeuzeitGroteskStd_BdCond.otf')
if not os.path.exists(FONT):
    FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
rng = np.random.default_rng(42)

# the pine at a third of its size (knots ~25 px), with the bands that hold no seam
SRC = []
for name, clean in (('pine-a.png', [(0, 39)]), ('pine-b.png', [(0, 25), (30, 51), (57, 85)])):
    im = np.asarray(Image.open(os.path.join(HERE, name)).convert('RGB').resize((170 * K, 85 * K), Image.LANCZOS), np.float32)
    if name == 'pine-a.png':
        im = im[:, :150 * K]                              # (its bottom right corner holds a watermark)
    SRC.append((im, [(a * K, b * K) for a, b in clean]))


def board(w, h, dark=1.0):
    """A board w x h: a seam-free slice of the pine, flipped at random, a little lighter or darker."""
    for _ in range(50):
        im, clean = SRC[int(rng.integers(len(SRC)))]
        y0, y1 = clean[int(rng.integers(len(clean)))]
        if y1 - y0 >= h and im.shape[1] >= w:
            break
    oy = int(rng.integers(y0, y1 - h + 1))
    ox = int(rng.integers(0, im.shape[1] - w + 1))
    b = im[oy:oy + h, ox:ox + w].copy()
    if rng.random() < 0.5:
        b = b[:, ::-1]
    return b * rng.uniform(0.9, 1.05) * dark


def planks(w, h, n, dark=1.0, nails=()):
    """n boards stacked (running along w), seams between, nail heads at the x's given (all at K = 1)."""
    w, h = w * K, h * K
    out = np.zeros((h, w, 3), np.float32)
    edges = [round(i * h / n) for i in range(n + 1)]
    for i in range(n):
        y0, y1 = edges[i], edges[i + 1]
        out[y0:y1] = board(w, y1 - y0, dark)
        out[y0:y0 + K] *= 0.45                             # the seam, and its shadow below
        if y1 - y0 > 2 * K:
            out[y0 + K:y0 + 2 * K] *= 0.78
        for x in nails:
            x, yc = x * K, (y0 + y1) // 2
            out[yc - K:yc + K, x - K:x + K] = (52, 46, 40)
            out[yc + K:yc + 2 * K, x - K:x + K] *= 0.6
    return out


def stencil(img, lines, box):
    """Black spray stencil: lines of (text, height px) centred in box (x0, y0, x1, y1)."""
    h, w = img.shape[:2]
    big = 6                                               # drawn 6x, then shrunk: soft spray edges
    ink = Image.new('L', (w * big, h * big), 0)
    d = ImageDraw.Draw(ink)
    x0, y0, x1, y1 = [v * K for v in box]
    lines = [(t, px * K) for t, px in lines]
    total = sum(px for _, px in lines) + 2 * K * (len(lines) - 1)
    y = (y0 + y1) / 2 - total / 2
    for text, px in lines:
        f = ImageFont.truetype(FONT, px * big)
        l, t, r, b = d.textbbox((0, 0), text, font=f)
        d.text(((x0 + x1) / 2 * big - (r - l) / 2 - l, y * big - t), text, font=f, fill=255)
        y += px + 2 * K
    halo = np.asarray(ink.filter(ImageFilter.GaussianBlur(big * 1.5)).resize((w, h), Image.LANCZOS), np.float32) / 255
    ink = ink.filter(ImageFilter.GaussianBlur(big * 0.12)).resize((w, h), Image.LANCZOS)
    a = np.asarray(ink, np.float32) / 255
    a *= rng.uniform(0.8, 1.0, a.shape)                    # sprayed: a little uneven
    a = np.maximum(a, (rng.random(a.shape) < 0.05) * halo * 0.6)  # overspray just round the letters
    a = np.clip(a, 0, 0.95)[..., None]
    return img * (1 - a) + np.array((22, 18, 14), np.float32) * a


def arrow_up(img, cx, y0, y1, wpx):
    """A stencilled up arrow."""
    h, w = img.shape[:2]
    cx, y0, y1, wpx = cx * K, y0 * K, y1 * K, wpx * K
    m = Image.new('L', (w * 4, h * 4), 0)
    d = ImageDraw.Draw(m)
    s = 4
    head = (y1 - y0) * 0.45
    d.polygon([(cx * s, y0 * s), ((cx + wpx) * s, (y0 + head) * s), ((cx + wpx * 0.35) * s, (y0 + head) * s),
               ((cx + wpx * 0.35) * s, y1 * s), ((cx - wpx * 0.35) * s, y1 * s), ((cx - wpx * 0.35) * s, (y0 + head) * s),
               ((cx - wpx) * s, (y0 + head) * s)], fill=255)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(0.5 * K)).resize((w, h), Image.LANCZOS), np.float32) / 255
    a = np.clip(a * rng.uniform(0.8, 1.0, a.shape), 0, 0.95)[..., None]
    return img * (1 - a) + np.array((22, 18, 14), np.float32) * a


atlas = np.zeros((256 * K, 256 * K, 3), np.float32)
atlas[:] = (150, 120, 84)                                 # (unused room: pine-coloured)


def put(region, img):
    x0, y0, x1, y1 = [v * K for v in region]
    atlas[y0:y1, x0:x1] = img


# body faces: six boards a face, nailed near the posts (posts cover ~6 px each end)
front = planks(116, 66, 6, nails=(8, 108))
front = stencil(front, [('TOP SECRET', 14), ('ARMY INTEL', 8), ('No. 4471-208', 7), ('DO NOT OPEN!', 8)], (7, 2, 109, 64))
back = planks(116, 66, 6, nails=(8, 108))
back = stencil(back, [('FRAGILE', 13), ('THIS SIDE UP', 8)], (30, 10, 86, 56))
back = arrow_up(back, 17, 17, 49, 7)
back = arrow_up(back, 99, 17, 49, 7)
end1 = planks(80, 66, 6, nails=(8, 72))
end1 = stencil(end1, [('U.S. ARMY', 11), ('4471-208', 8)], (7, 10, 73, 56))
end2 = planks(80, 66, 6, nails=(8, 72))
end2 = stencil(end2, [('KEEP DRY', 10), ('HANDLE WITH CARE', 6)], (7, 15, 73, 51))
put((0, 0, 116, 66), front)
put((120, 0, 236, 66), back)
put((0, 70, 80, 136), end1)
put((84, 70, 164, 136), end2)

# cleats: darker pine, grain along their length; posts and lid cleats turned up and down
put((168, 70, 177, 136), np.rot90(planks(66, 9, 1, dark=0.82, nails=(5, 33, 61)), 1))
put((181, 70, 190, 156), np.rot90(planks(86, 9, 1, dark=0.82, nails=(5, 43, 81)), 1))
eg = board(9 * K, 9 * K, 0.7)                             # end grain: darker, rings
yy, xx = np.mgrid[0:9 * K, 0:9 * K] / K
eg *= (0.85 + 0.15 * np.cos(np.hypot(xx - 4, yy - 9) * 1.6))[..., None]
put((194, 70, 203, 79), eg)

# lid: eight boards along x
put((0, 160, 122, 246), planks(122, 86, 8))

# frame: the lips round the body, seen from above - a board along each side (the front /
# back ones along x, the ends' along z), 8 px wide (the lip is 3), the middle hidden
fr = planks(122, 86, 8, dark=0.9)
fr[0:8 * K] = planks(122, 8, 1, dark=0.85)
fr[78 * K:86 * K] = planks(122, 8, 1, dark=0.85)
fr[:, 0:8 * K] = np.rot90(planks(86, 8, 1, dark=0.85), 1)
fr[:, 114 * K:122 * K] = np.rot90(planks(86, 8, 1, dark=0.85), 1)
put((126, 160, 248, 246), fr)

# bands: one board each, nailed
put((0, 247, 122, 256), planks(122, 9, 1, dark=0.82, nails=(5, 61, 117)))
put((124, 247, 210, 256), planks(86, 9, 1, dark=0.82, nails=(5, 43, 81)))

Image.fromarray(np.clip(atlas, 0, 255).astype(np.uint8)).save(OUT)
print(OUT)
