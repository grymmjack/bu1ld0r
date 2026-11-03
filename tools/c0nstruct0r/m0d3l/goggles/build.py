#!/usr/bin/python3
"""c0-goggles: night-vision goggles - a dark rubber housing, three lens tubes (two below, one
above) glowing green, a head strap behind. The game's is 0.23 x 0.19 x 0.09 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, rubber, glow  # noqa: E402

GREEN = (90, 255, 90)
m = Model('goggles', HERE, seed=131)
m.material('main', 'plastic')
house = m.box('housing', (0, 0.01, 0.02), (0.19, 0.175, 0.04), '1E2024')
m.box('strap', (0, 0.07, 0.048), (0.228, 0.03, 0.016), '141516', paint='strap')
for i, (x, y) in enumerate(((0.045, 0.058), (-0.045, 0.058), (0, 0.135))):
    m.cyl(f'tube-{i}', (x, y, 0), (0.072, 0.04, 0.072), '1A1C1F', seg=12, rot=(-90, 0, 0), paint={'-z': 'lens', '*': 'tube'})


def lens(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((26, 28, 31), np.float32)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    img[d < 0.82] = (20, 60, 20)
    t = np.clip(1 - d / 0.72, 0, 1)[..., None]
    inner = d < 0.72
    img[inner] = (np.array((30, 140, 30)) * (1 - t) + np.array(GREEN) * t)[inner]
    hi = np.hypot(xx - w * 0.38, yy - h * 0.36) / (w / 2) < 0.16
    img[hi] = (220, 255, 220)
    return glow(img, a, (w * 0.15, h * 0.15, w * 0.85, h * 0.85), GREEN, 0.2, 1)


def house_front(a, w, h):
    img = rubber((34, 36, 40))(a, w, h)
    a.rect(img, (w * 0.05, h * 0.9, w * 0.25, h * 0.96), (90, 240, 90))    # power light
    return img


house.paint = {'-z': house_front, '*': 'house'}
m.swatch('house', rubber((34, 36, 40)))
m.swatch('strap', rubber((24, 24, 26)))
m.swatch('lens', lens)
m.swatch('tube', lambda a, w, h: a.edge_dark(paint('1A1C1F', 0.3)(a, w, h), 0.6, 0.7))

if __name__ == '__main__':
    m.build()
