#!/usr/bin/python3
"""c0-slugs: a clip of five blue slugs standing in a row - steel clip, blue-glowing slug bodies,
pointed steel heads. The game's is 0.14 x 0.10 x 0.03 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow  # noqa: E402

BLUE = (50, 120, 255)
m = Model('slugs', HERE, seed=117)
m.material('main', 'plastic')
m.box('clip', (0, 0, 0), (0.137, 0.018, 0.034), '50565E', paint={'-z': 'clipface', '+z': 'clipface', '*': 'clip'})
for i in range(5):
    x = -0.052 + i * 0.026
    m.cyl(f'slug-{i}', (x, 0.018, 0), (0.02, 0.055, 0.02), '3278FF', seg=6, paint={'side': 'slug', 'top': 'slug', 'bottom': 'slug'})
    m.cyl(f'head-{i}', (x, 0.073, 0), (0.02, 0.03, 0.02), 'C0C6CE', seg=6, amt=0.2, kind='cone', paint={'side': 'steel', 'top': 'steel', 'bottom': 'steel'})


def slug(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array(BLUE, np.float32)
    for k in range(6):
        a.rect(img, (k * w / 6 + w / 30, h * 0.1, k * w / 6 + w / 15, h * 0.9), (200, 230, 255), 0.55)
    a.rect(img, (0, h * 0.8, w, h), (30, 50, 110))
    return glow(img, a, (0, 0, w, h * 0.8), (140, 190, 255), 0.15, 1)


def clip_face(a, w, h):
    img = steel((120, 126, 134))(a, w, h)
    for k in range(5):
        x = w * (0.12 + k * 0.19)
        a.rect(img, (x, h * 0.3, x + w * 0.04, h * 0.7), (50, 54, 60))
    return img


m.swatch('slug', slug)
m.swatch('steel', steel((196, 202, 210)))
m.swatch('clip', steel((110, 116, 124)))
m.swatch('clipface', clip_face)

if __name__ == '__main__':
    m.build()
