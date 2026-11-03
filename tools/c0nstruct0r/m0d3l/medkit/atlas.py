#!/usr/bin/python3
"""c0-medkit's one picture (pictures/c0nstruct0r/c0-medkit.png): the small, white crew medical kit.

  /usr/bin/python3 tools/c0nstruct0r/m0d3l/medkit/atlas.py [K] [OUT.png]

Laid out at 256 x 256, 700 pixels a cell (the kit is small: 16 x 11 x 6.5 cm); drawn at K = 2
(512, the default). Regions (x0, y0, x1, y1) at K = 1 - `texture.py` maps the faces onto them:
  front   0,0,112,77        body -z: white frame, the recessed red panel (the middle half), cross
  back    116,0,228,77      body +z
  sidex   0,81,45.5,158     body +x: inventory label, barcode
  sidenx  50,81,95.5,158    body -x: velcro patch
  top     100,81,212,126.5  body top
  bottom  100,131,212,176.5 body bottom
  alu     216,81,256,176    aluminium swatch (rails, posts, latch sides)
  latch   230,0,244,16.8    a latch's face
  rubber  0,180,120,232     rubber swatch (seam, feet, handle sides)
  grip    124,180,180,191.2 the handle's top: ridges
  wswatch 184,180,256,256   white paint swatch (the raised crosses)
Renders (pixelmon, juggernautXL / heun / karras): red.png (glossy red paint), alu.png (brushed
aluminium), rubber.png (its background strip is clean rubber). The white paint is made here:
off-white with the red render's fine paint texture.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
K = int(sys.argv[1]) if len(sys.argv) > 1 else 2
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(REPO, 'pictures', 'c0nstruct0r', 'c0-medkit.png')
FONT = os.path.expanduser('~/.local/share/fonts/d/DINNeuzeitGroteskStd_BdCond.otf')
if not os.path.exists(FONT):
    FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
rng = np.random.default_rng(11)


def load(name):
    return np.asarray(Image.open(os.path.join(HERE, name)).convert('RGB'), np.float32)


RED = load('red.png')
ALU = load('alu.png')
RUB = load('rubber.png')[0:120]                           # (the washer sits below)


def lum(a):
    return a @ np.array([0.299, 0.587, 0.114], np.float32)


def detail(src, w, h, amt):
    """A w x h patch of src's fine texture: its luminance less a blur of it, x amt."""
    y = int(rng.integers(0, src.shape[0] - h)) if src.shape[0] > h else 0
    x = int(rng.integers(0, src.shape[1] - w)) if src.shape[1] > w else 0
    p = Image.fromarray(np.clip(lum(src[y:y + h, x:x + w]), 0, 255).astype(np.uint8))
    hp = np.asarray(p, np.float32) - np.asarray(p.filter(ImageFilter.GaussianBlur(6 * K)), np.float32)
    return hp * amt


def white(w, h):
    """White powder-coated aluminium: off-white, the paint's texture, a few faint scuffs."""
    w, h = round(w * K), round(h * K)
    out = np.ones((h, w, 3), np.float32) * np.array((234, 234, 229), np.float32)
    out += detail(RED, w, h, 1.6)[..., None]
    for _ in range(int(w * h / (900 * K * K)) + 1):           # scuffs: short grey strokes
        x, y = rng.integers(0, w), rng.integers(0, h)
        L = rng.integers(3 * K, 12 * K)
        a = rng.uniform(0, np.pi)
        for t in range(int(L)):
            xx, yy = int(x + np.cos(a) * t), int(y + np.sin(a) * t)
            if 0 <= xx < w and 0 <= yy < h:
                out[yy, xx] *= rng.uniform(0.88, 0.95)
    return out


def edge_dark(img, px=3, k=0.86):
    """Faces a little darker toward their edges (dirt where hands don't reach)."""
    h, w = img.shape[:2]
    px *= K
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy)).astype(np.float32)
    f = k + (1 - k) * np.clip(d / px, 0, 1)
    return img * f[..., None]


def tinted(src, w, h, rgb, amt=1.0):
    """src's light and shade on colour rgb (the red render's orange made a true red)."""
    w, h = round(w * K), round(h * K)
    y = int(rng.integers(0, src.shape[0] - h))
    x = int(rng.integers(0, src.shape[1] - w))
    l = lum(src[y:y + h, x:x + w])
    l = 1 + (l / l.mean() - 1) * amt
    return np.array(rgb, np.float32) * l[..., None]


def text(img, s, px, box, rgb=(30, 30, 32), align='c'):
    """Stencil-crisp text s, px tall (K = 1 pixels), in box (x0, y0, x1, y1)."""
    h, w = img.shape[:2]
    big = 6
    m = Image.new('L', (w * big, h * big), 0)
    d = ImageDraw.Draw(m)
    f = ImageFont.truetype(FONT, int(px * K * big))
    x0, y0, x1, y1 = [v * K * big for v in box]
    l, t, r, b = d.textbbox((0, 0), s, font=f)
    tx = {'c': (x0 + x1) / 2 - (r - l) / 2, 'l': x0, 'r': x1 - (r - l)}[align] - l
    d.text((tx, (y0 + y1) / 2 - (b - t) / 2 - t), s, font=f, fill=255)
    a = np.asarray(m.resize((w, h), Image.LANCZOS), np.float32)[..., None] / 255 * 0.92
    return img * (1 - a) + np.array(rgb, np.float32) * a


def rect(img, box, rgb, a=1.0):
    x0, y0, x1, y1 = [round(v * K) for v in box]
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a) + np.array(rgb, np.float32) * a
    return img


def cross(img, cx, cy, size, arm, rgb):
    rect(img, (cx - arm / 2, cy - size / 2, cx + arm / 2, cy + size / 2), rgb)
    rect(img, (cx - size / 2, cy - arm / 2, cx + size / 2, cy + arm / 2), rgb)
    return img


def panel_face(w, h, top_line, small_line):
    """A front / back: white frame, red panel in the middle half (the inset 0.25), white cross."""
    img = white(w, h)
    px0, py0, px1, py1 = w * 0.25, h * 0.25, w * 0.75, h * 0.75
    red = tinted(RED, px1 - px0, py1 - py0, (196, 28, 34), 1.4)
    X0, Y0 = round(px0 * K), round(py0 * K)
    img[Y0:Y0 + red.shape[0], X0:X0 + red.shape[1]] = red
    # the recess: a shadow line along the panel's top and left, a light one bottom and right
    rect(img, (px0, py0, px1, py0 + 0.8), (90, 10, 14), 0.7)
    rect(img, (px0, py0, px0 + 0.8, py1), (90, 10, 14), 0.7)
    rect(img, (px0, py1 - 0.6, px1, py1), (240, 120, 120), 0.4)
    cross(img, w / 2, h / 2, (py1 - py0) * 0.7, (py1 - py0) * 0.22, (246, 246, 242))
    img = text(img, top_line, 6.5, (0, 2, w, py0 - 1))
    if small_line:
        img = text(img, small_line, 3.6, (px0, py1 + 0.6, px1, py1 + 4.4), (60, 60, 64))
    return edge_dark(img)


def barcode(img, box, seed):
    r = np.random.default_rng(seed)
    x0, y0, x1, y1 = box
    x = x0
    while x < x1:
        bw = r.choice([0.35, 0.35, 0.7, 1.05])
        if r.random() < 0.55:
            rect(img, (x, y0, min(x + bw, x1), y1), (20, 20, 22))
        x += bw
    return img


atlas = np.zeros((256 * K, 256 * K, 3), np.float32)
atlas[:] = (225, 225, 220)


def put(region, img):
    x0, y0 = round(region[0] * K), round(region[1] * K)
    atlas[y0:y0 + img.shape[0], x0:x0 + img.shape[1]] = img


put((0, 0), panel_face(112, 77, 'CREW MEDICAL KIT', ''))
put((116, 0), panel_face(112, 77, 'MEDICAL  EMERGENCY', ''))

# +x side: an inventory label - off-white sticker, thin border, part number, barcode
s = white(45.5, 77)
rect(s, (5, 14, 40.5, 50), (247, 247, 240))
rect(s, (5, 14, 40.5, 14.5), (120, 120, 120)); rect(s, (5, 49.5, 40.5, 50), (120, 120, 120))
rect(s, (5, 14, 5.5, 50), (120, 120, 120)); rect(s, (40, 14, 40.5, 50), (120, 120, 120))
s = text(s, 'CREW HEALTH CARE', 4.2, (6, 15.5, 39.5, 20.5))
s = text(s, 'P/N 683-14552-2', 3.4, (6, 21, 39.5, 25))
s = text(s, 'S/N 0047  LOT 26-11', 3.4, (6, 25.5, 39.5, 29.5))
s = barcode(s, (8, 31.5, 37.5, 43), 5)
s = text(s, 'CMK-02', 3.6, (6, 44, 39.5, 48.5))
s = rect(s, (0, 54, 45.5, 55.5), (196, 28, 34))           # a red pinstripe above the seam
put((0, 81), edge_dark(s))

# -x side: a grey velcro patch, stitched, and a small label under it
s = white(45.5, 77)
v = tinted(RUB, 29, 22, (128, 128, 130), 1.2)
v += (rng.random(v.shape[:2]) * 18 - 9)[..., None]       # the hook side's fuzz
X0, Y0 = round(8.25 * K), round(14 * K)
s[Y0:Y0 + v.shape[0], X0:X0 + v.shape[1]] = v
for t in np.arange(9, 37, 1.2):                           # stitches round it
    rect(s, (t, 14.6, t + 0.6, 15.0), (70, 70, 72)); rect(s, (t, 35.0, t + 0.6, 35.4), (70, 70, 72))
s = text(s, 'STOW ON VELCRO', 3.6, (4, 38, 41.5, 42.5))
s = text(s, 'DO NOT SPLIT LATCHES', 3.0, (4, 43, 41.5, 47))
s = rect(s, (0, 54, 45.5, 55.5), (196, 28, 34))
put((50, 81), edge_dark(s))

# top: white, a small red label 'MEDICAL' toward the front, the handle sits in the middle
s = white(112, 45.5)
s = rect(s, (8, 34, 30, 41), (196, 28, 34))
s = text(s, 'MEDICAL', 4.8, (8, 34, 30, 41), (246, 246, 242))
s = rect(s, (82, 34, 104, 41), (196, 28, 34))
s = text(s, 'CMK-02', 4.8, (82, 34, 104, 41), (246, 246, 242))
put((100, 81), edge_dark(s))

# bottom: white, grubbier
put((100, 131), edge_dark(white(112, 45.5) * 0.9, 5, 0.8))

# aluminium swatch: brushed lines along y (the rails run up and down)
a = np.rot90(tinted(ALU, 95, 40, (176, 180, 186), 0.9), 1)
put((216, 81), a)

# a latch's face: an over-centre lever - a hinge barrel across the top, the lever plate below
# it with a raised edge, a pull lip at the bottom (no dots: two rivets over a slot read as a face)
l = tinted(ALU, 14, 16.8, (176, 180, 186), 0.9)
l = rect(l, (0, 0, 14, 3.2), (120, 124, 130))                # hinge barrel
l = rect(l, (0, 0.6, 14, 1.4), (222, 225, 230), 0.8)         # its highlight
l = rect(l, (0, 3.2, 14, 3.8), (60, 62, 66))                 # its shadow
l = rect(l, (1.2, 3.8, 1.8, 15.2), (225, 228, 232), 0.7)     # lever's raised edges
l = rect(l, (12.2, 3.8, 12.8, 15.2), (90, 92, 98), 0.7)
l = rect(l, (2.5, 14.0, 11.5, 16.8), (140, 144, 150))        # pull lip
l = rect(l, (2.5, 14.0, 11.5, 14.6), (230, 232, 236), 0.7)
put((230, 0), edge_dark(l, 1.2, 0.8))

# rubber swatch, and the handle's grip with ridges across
put((0, 180), tinted(RUB, 120, 52, (58, 58, 61), 1.0))
g = tinted(RUB, 56, 11.2, (52, 52, 55), 1.0)
for x in np.arange(2, 56, 3.0):
    rect(g, (x, 0, x + 0.9, 11.2), (30, 30, 32))
put((124, 180), g)

# white swatch: the raised crosses, a little brighter than the case
put((184, 180), white(72, 76) * 1.02)

Image.fromarray(np.clip(atlas, 0, 255).astype(np.uint8)).save(OUT)
print(OUT)
