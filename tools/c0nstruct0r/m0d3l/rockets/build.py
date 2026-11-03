#!/usr/bin/python3
"""c0-rockets: a dark steel crate of four rockets, their red warheads standing out of the top -
stencilled, banded, riveted. The game's is 0.13 x 0.14 x 0.08 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel  # noqa: E402

DARK, RED = '34383E', (220, 50, 40)
m = Model('rockets', HERE, seed=119)
m.material('main', 'paint')
crate = m.box('crate', (0, 0, 0), (0.132, 0.085, 0.079), DARK)
for i, x in enumerate((0.045, 0.015, -0.015, -0.045)):
    m.cyl(f'body-{i}', (x, 0.085, 0), (0.024, 0.02, 0.024), 'A0A6AE', seg=8, paint={'side': 'band', 'top': 'steel', 'bottom': 'steel'})
    m.cyl(f'head-{i}', (x, 0.105, 0), (0.024, 0.036, 0.024), 'DC3228', seg=8, amt=0.15, kind='cone', paint={'side': 'warhead', 'top': 'warhead', 'bottom': 'warhead'})


def side(a, w, h):
    img = paint(DARK, 0.7)(a, w, h)
    for y in (h * 0.1, h * 0.88):
        a.rect(img, (0, y, w, y + h * 0.06), (90, 96, 104))
        for x in np.arange(3, w, 8):
            a.rect(img, (x - 0.7, y + h * 0.01, x + 0.7, y + h * 0.05), (170, 176, 184))
    a.rect(img, (w * 0.1, h * 0.3, w * 0.9, h * 0.7), (200, 170, 40))
    img = a.text(img, 'HE-RKT', h * 0.3, (w * 0.12, h * 0.32, w * 0.88, h * 0.68), (30, 30, 30))
    return img


def warhead(a, w, h):
    img = paint(RED, 0.2, 1)(a, w, h)
    for k in range(8):
        a.rect(img, (k * w / 8 + w / 32, 0, k * w / 8 + w / 16, h), (255, 150, 140), 0.45)
    return img


def band(a, w, h):
    img = steel((170, 176, 184))(a, w, h)
    a.rect(img, (0, h * 0.3, w, h * 0.7), (255, 150, 30))
    return img


crate.paint = {'-z': side, '+z': side, '*': 'darkside'}
m.swatch('darkside', paint(DARK, 0.7))
m.swatch('warhead', warhead)
m.swatch('band', band)
m.swatch('steel', steel((170, 176, 184)))

if __name__ == '__main__':
    m.build()
