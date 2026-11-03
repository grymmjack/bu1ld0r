#!/usr/bin/python3
"""c0-shells: an orange shell box, open at the front - a dark well of red shotgun shells lying in two
rows (brass heads out), a label on top. The game's is 0.13 x 0.13 x 0.07 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, glow, front_box  # noqa: E402

ORANGE = (230, 110, 30)
m = Model('shells', HERE, seed=113)
m.material('main', 'plastic')
box = m.box('box', (0, 0, 0), (0.13, 0.13, 0.066), 'E66E1E', walls='well')
box.cut('-z', (-0.055, 0.055, 0.012, 0.118), 0.05)
shells = m.box('shells', (0, 0.012, -0.006), (0.11, 0.106, 0.03), 'C02020')


def shell_ends(a, w, h):
    """The shells seen end on: two columns of four, red hulls, brass heads with a primer."""
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((30, 16, 12), np.float32)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    for i in range(2):
        for j in range(4):
            cx, cy = w * (0.27 + i * 0.46), h * (0.13 + j * 0.245)
            d = np.hypot(xx - cx, yy - cy)
            r = min(w * 0.22, h * 0.12)
            img[d < r] = (200, 160, 70)
            img[d < r * 0.85] = (230, 190, 90)
            img[d < r * 0.3] = (150, 110, 50)
            hi = np.hypot(xx - cx + r * 0.3, yy - cy + r * 0.3) < r * 0.2
            img[hi] = (255, 240, 180)
    return img


def shell_side(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((190, 30, 30), np.float32)
    for j in range(4):
        y = h * (0.02 + j * 0.245)
        a.rect(img, (0, y, w, y + h * 0.21), (200, 36, 36))
        a.rect(img, (0, y, w * 0.3, y + h * 0.21), (220, 180, 80))         # the brass head
        a.rect(img, (0, y + h * 0.03, w, y + h * 0.05), (240, 90, 90))
    return img


def front(a, w, h):
    img = paint(ORANGE, 0.6)(a, w, h)
    s = front_box(box, w, h, -0.055, 0.055, 0.012, 0.118)
    a.rect(img, (s[0] - 1, s[1] - 1, s[2] + 1, s[3] + 1), (120, 50, 14))
    return img


def top(a, w, h):
    img = paint(ORANGE, 0.6)(a, w, h)
    a.rect(img, (w * 0.12, h * 0.25, w * 0.88, h * 0.75), (240, 230, 210))
    img = a.text(img, '12 GA', h * 0.3, (w * 0.14, h * 0.3, w * 0.86, h * 0.7), (40, 30, 30))
    return img


box.paint = {'-z': front, '+y': top, '*': 'orange'}
shells.paint = {'-z': shell_ends, '*': 'shellside'}
m.swatch('orange', paint(ORANGE, 0.6))
m.swatch('well', paint((40, 20, 14), 0.2, 1))
m.swatch('shellside', shell_side)

if __name__ == '__main__':
    m.build()
