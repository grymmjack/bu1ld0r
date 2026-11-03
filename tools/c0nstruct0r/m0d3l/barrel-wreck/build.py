#!/usr/bin/python3
"""c0-barrel-wreck: c0-barrel broken - the game shows barrel-wreck.obj when a barrel is shot apart
(DecoWreckName$: NAME-wreck). The barrel's base and bottom hoop still whole, its red staves snapped
off at every height (most split in two, so the tops are ragged), two blown out to stubs, pale raw
wood at the breaks, soot running down from them, a dark sooty inside.

c0-barrel's own pictures (barrel/wood.png, iron.png) so it matches: radius 0.145 at the foot,
0.160 at 0.07, 0.172 at 0.17; hoop 0.059..0.081 r 0.166."""
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402

SRC = os.path.join(HERE, '..', 'barrel')
WOOD = np.asarray(Image.open(os.path.join(SRC, 'wood.png')).convert('RGB').resize((320, 640), Image.LANCZOS), np.float32)
IRON = np.asarray(Image.open(os.path.join(SRC, 'iron.png')).convert('RGB'), np.float32)
RED = 'B8402C'
m = Model('barrel-wreck', HERE, seed=191)
m.material('main', 'wood')


def wood_cut(a, w, h, seed, k=1.0):
    """A piece of the barrel's red wood, image-sized (px(h) x px(w))."""
    r = np.random.default_rng(seed)
    W, H = a.px(w), a.px(h)
    src = Image.fromarray(WOOD.astype(np.uint8))
    sw, sh = max(8, min(320, int(W * 0.8))), max(8, min(640, int(H * 0.8)))
    x0, y0 = int(r.integers(0, 320 - sw + 1)), int(r.integers(0, 640 - sh + 1))
    img = np.asarray(src.crop((x0, y0, x0 + sw, y0 + sh)).resize((W, H), Image.LANCZOS), np.float32)
    return img * k


def soot(img, frac=0.35, k=0.25):
    """Darker towards the top (the break), streaky."""
    H, W = img.shape[:2]
    r = np.random.default_rng(W * 7 + H)
    yy = np.arange(H)[:, None] / max(1, H - 1)
    reach = frac * (0.6 + 0.8 * r.random(W))[None, :]
    t = np.clip(1 - yy / reach, 0, 1) ** 1.5
    return img * (1 - (1 - k) * t[..., None])


def stave(a, w, h):
    img = wood_cut(a, w, h, 3, 0.95)
    img[:, :max(1, a.px(0.6))] *= 0.5                       # seams on its two edges
    img[:, -max(1, a.px(0.6)):] *= 0.5
    return soot(img, 0.22, 0.5)


def splinter(a, w, h):
    """The broken end: pale raw wood, charred round the edge."""
    r = np.random.default_rng(9)
    H, W = a.px(h), a.px(w)
    img = np.ones((H, W, 3), np.float32) * np.array((214, 168, 118), np.float32)
    img *= (0.85 + 0.3 * r.random((1, W)))[..., None]       # end grain
    img[:2] *= 0.45
    img[-2:] *= 0.45
    img[:, :2] *= 0.6
    img[:, -2:] *= 0.6
    return img


def drum_side(a, w, h):
    """The base's 16 staves, as c0-barrel's side: each its own slice, seams at the column edges."""
    img = np.zeros((a.px(h), a.px(w), 3), np.float32)
    cw = a.px(w) / 16
    r = np.random.default_rng(5)
    for j in range(16):
        x0, x1 = int(round(j * cw)), int(round((j + 1) * cw))
        img[:, x0:x1] = wood_cut(a, (x1 - x0) / a.K, h, 20 + j, r.uniform(0.86, 1.06))
        img[:, x0] *= 0.42
        img[:, x1 - 1] *= 0.42
    img[-a.px(1.5):] *= 0.6                                 # the chime
    return img


def inside(a, w, h):
    """The barrel's bottom seen from inside: dark boards, soot, a few splinters lying on it."""
    yy, xx = np.mgrid[0:a.px(h), 0:a.px(w)] / a.K
    img = wood_cut(a, w, h, 41, 0.45)
    for k in range(1, 5):                                   # boards across
        img[np.abs(yy - k * h / 5) < 0.5] *= 0.5
    d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    img *= (1 - 0.55 * np.clip(1 - d, 0, 1) ** 0.7)[..., None]   # a scorch in the middle
    r = np.random.default_rng(13)
    for _ in range(7):
        cx, cy, ln, ang = r.uniform(0.25, 0.75) * w, r.uniform(0.25, 0.75) * h, r.uniform(3, 7), r.uniform(0, np.pi)
        t = (xx - cx) * np.cos(ang) + (yy - cy) * np.sin(ang)
        n = -(xx - cx) * np.sin(ang) + (yy - cy) * np.cos(ang)
        img[(np.abs(t) < ln / 2) & (np.abs(n) < 0.55)] = (196, 150, 104)
    return img


def under(a, w, h):
    return wood_cut(a, w, h, 57, 0.5)


def hoop(a, w, h):
    band = Image.fromarray(IRON[78:112].astype(np.uint8)).resize((a.px(w), a.px(h)), Image.LANCZOS)
    img = np.asarray(band, np.float32) * 0.62 + np.array((8, 4, 0), np.float32)
    img[:a.K] *= 0.6
    img[-a.K:] *= 0.6
    cw = a.px(w) / 16
    for j in range(16):                                     # a rivet a face
        x, y = int((j + 0.5) * cw), a.px(h) // 2
        img[y - a.K:y + a.K, x - a.K:x + a.K] = (92, 84, 78)
    return img


def hoop_cap(a, w, h):
    return np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((44, 38, 34), np.float32)


# the base: the barrel's bottom, still whole, and its hoop
m.cyl('base', (0, 0, 0), (0.300, 0.07, 0.300), RED, seg=16,
      paint={'side': drum_side, 'top': 'inside', 'bottom': 'under'})
m.cyl('hoop', (0, 0.045, 0), (0.336, 0.022, 0.336), '3A3634', seg=16,
      paint={'side': hoop, 'top': 'hoopcap', 'bottom': 'hoopcap'})

# the staves: leaning out as the barrel's bulge does, snapped off
r = np.random.default_rng(191)
LEAN, TH, Y0 = 8.0, 0.014, 0.03
R0 = 0.152 - TH / 2                                         # the stave's middle at its foot
W = 2 * 0.16 * math.sin(math.pi / 16) + 0.004
blown, gone, tall = {5, 6}, {4}, {10, 14}                     # blown out to stubs / missing / survivors
for k in range(16):
    if k in gone:
        continue
    a = k * 22.5 + 11.25
    ar = math.radians(a)
    cx, cz = R0 * math.sin(ar), R0 * math.cos(ar)            # the foot's middle
    tx, tz = math.cos(ar), -math.sin(ar)                    # along the barrel's round (local x)
    if k in blown:
        hs = [float(r.uniform(0.055, 0.075))]
    else:
        base = float(r.uniform(0.22, 0.27)) if k in tall else float(r.uniform(0.08, 0.2))
        hs = [base] if r.random() < 0.35 else [base + float(r.uniform(-0.06, -0.02)), base + float(r.uniform(0.0, 0.05))]
    n = len(hs)
    f = float(r.uniform(0.38, 0.62)) if n == 2 else 1.0
    widths = [W] if n == 1 else [W * f, W * (1 - f)]
    offs = [0.0] if n == 1 else [-W / 2 + widths[0] / 2, W / 2 - widths[1] / 2]
    for s, (hh, ww, off) in enumerate(zip(hs, widths, offs)):
        m.box(f'stave-{k}{"ab"[s] if n == 2 else ""}', (round(cx + tx * off, 4), Y0, round(cz + tz * off, 4)),
              (round(ww, 4), round(hh, 4), TH), RED, paint={'+y': 'splinter', '*': 'stave'}, rot=(LEAN, a, 0))

# a broken piece of stave lying inside, on the floor
m.box('piece', (0.03, 0.07, -0.01), (0.05, 0.012, 0.15), RED, paint={'+y': 'plank', '*': 'splinter'}, rot=(0, 32, 0))

m.swatch('stave', stave)
m.swatch('plank', lambda a, w, h: soot(wood_cut(a, w, h, 77, 0.9), 0.3, 0.6))
m.swatch('splinter', splinter)
m.swatch('inside', inside)
m.swatch('under', under)
m.swatch('hoopcap', hoop_cap)

if __name__ == '__main__':
    m.build()
