#!/usr/bin/python3
"""c0-camera: a security camera - a round dark foot, a post, a knuckle, a charcoal housing with red
trim and a sun hood, a red-eyed lens looking out the front (-z). The game's is 0.14 x 0.27 x 0.22
cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, glow  # noqa: E402

BODY, RED = '2C2F35', (255, 40, 50)
m = Model('camera', HERE, seed=93)
m.material('main', 'plastic')
m.cyl('foot', (0, 0, 0.03), (0.09, 0.025, 0.09), '1E2024', seg=8, paint={'side': 'dark', 'top': 'dark', 'bottom': 'dark'})
m.cyl('post', (0, 0.025, 0.03), (0.032, 0.1, 0.032), '33363C', seg=8, paint={'side': 'post', 'top': 'dark', 'bottom': 'dark'})
m.box('knuckle', (0, 0.125, 0.03), (0.05, 0.04, 0.05), '1E2024', paint='dark')
house = m.box('housing', (0, 0.165, -0.01), (0.1, 0.085, 0.2), BODY)
m.box('hood', (0, 0.25, -0.016), (0.124, 0.012, 0.216), '24272C', paint={'+y': 'hoodtop', '*': 'hood'})


def lens(a, w, h):
    img = paint(BODY, 0.3)(a, w, h)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    cx, cy = w / 2, h * 0.5
    d = np.hypot(xx - cx, yy - cy)
    r = min(w, h) * 0.44
    img[d < r] = (16, 17, 20)
    img[(d > r * 0.86) & (d < r)] = (120, 126, 134)
    img[d < r * 0.7] = (110, 10, 16)
    img[d < r * 0.5] = RED
    img[d < r * 0.22] = (255, 170, 160)
    hi = (np.hypot(xx - cx + r * 0.25, yy - cy + r * 0.25) < r * 0.12)
    img[hi] = (255, 230, 230)
    return glow(img, a, (cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7), RED, 0.2, 1)


def side(a, w, h):
    img = paint(BODY, 0.4)(a, w, h)
    a.rect(img, (0, h * 0.12, w, h * 0.18), (190, 30, 40))              # red trim
    for k in range(4):                                                 # cooling fins drawn
        y = h * (0.35 + k * 0.13)
        a.rect(img, (w * 0.55, y, w * 0.95, y + h * 0.05), (18, 19, 22))
    a.rect(img, (w * 0.06, h * 0.7, w * 0.12, h * 0.78), RED)           # recording light
    return img


def back(a, w, h):
    img = paint(BODY, 0.4)(a, w, h)
    a.rect(img, (w * 0.3, h * 0.35, w * 0.7, h * 0.65), (18, 19, 22))
    a.rect(img, (w * 0.42, h * 0.45, w * 0.58, h * 0.55), (90, 96, 104))  # cable gland
    return img


house.paint = {'-z': lens, '+z': back, '+x': side, '-x': side, '*': 'bodyplain'}
m.swatch('dark', paint('1E2024', 0.3))
m.swatch('post', paint('33363C', 0.3, 1))
m.swatch('bodyplain', paint(BODY, 0.4))
m.swatch('hood', lambda a, w, h: a.edge_dark(paint('24272C', 0.3)(a, w, h), 0.8, 0.7))
m.swatch('hoodtop', lambda a, w, h: paint('24272C', 0.5)(a, w, h))

if __name__ == '__main__':
    m.build()
