#!/usr/bin/python3
"""c0-pickup-repeater: the repeater lying in wait - a green SMG (the muzzle to +x), black barrel
and flash hider, a top rail with a sight, a wooden ribbed magazine, a green stock and grip. The
game's is 0.38 x 0.24 x 0.05 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, wood, glow  # noqa: E402

GREEN, DARKG, BLACK, LENS = (60, 160, 50), (40, 110, 36), '1C1E20', (120, 255, 140)
m = Model('pickup-repeater', HERE, seed=153)
m.material('main', 'paint')
rec = m.box('receiver', (-0.02, 0.12, 0), (0.22, 0.07, 0.04), '3CA032')
m.box('barrel', (0.13, 0.145, 0), (0.08, 0.022, 0.02), BLACK, paint='black')
m.box('hider', (0.18, 0.139, 0), (0.02, 0.034, 0.026), BLACK, paint={'+x': 'bore', '*': 'black'})
m.box('rail', (0.0, 0.19, 0), (0.14, 0.012, 0.022), BLACK, paint={'-z': 'notch', '+z': 'notch', '*': 'black'})
m.box('sight', (0.02, 0.202, 0), (0.04, 0.035, 0.018), BLACK, paint={'-x': 'lens', '+x': 'lens', '*': 'black'})
m.box('stock', (-0.16, 0.112, 0), (0.06, 0.07, 0.034), '3CA032', paint={'-z': 'stock', '+z': 'stock', '*': 'green'})
mag = m.box('mag', (0.045, 0.0, 0), (0.045, 0.125, 0.03), 'B07838')
m.box('grip', (-0.055, 0.055, 0), (0.03, 0.068, 0.03), '286E24', paint='darkg')
m.box('guard', (-0.012, 0.072, 0), (0.05, 0.008, 0.014), BLACK, paint='black')


def side(a, w, h):
    img = paint(GREEN, 0.4)(a, w, h)
    a.rect(img, (0, h * 0.7, w, h), DARKG)                            # the lower half darker
    a.rect(img, (w * 0.1, h * 0.25, w * 0.45, h * 0.5), (34, 36, 38))     # the ejection port
    for u in (0.55, 0.6, 0.65, 0.7, 0.75):                            # vent slots
        a.rect(img, (w * u, h * 0.3, w * u + 1, h * 0.55), DARKG)
    return img


def stock(a, w, h):
    img = paint(GREEN, 0.4)(a, w, h)
    a.rect(img, (w * 0.2, h * 0.3, w * 0.8, h * 0.6), (34, 36, 38))      # the stock's hole
    return img


def magazine(a, w, h):
    img = wood((180, 122, 60))(a, w, h)
    for v in np.arange(3, h, 4.5):                                    # ribs
        a.rect(img, (0, v, w, v + 1.2), (110, 70, 34))
    return a.edge_dark(img, 1.5, 0.7)


def notch(a, w, h):
    img = paint(BLACK, 0.2)(a, w, h)
    for k in np.arange(1, w, 2.5):
        a.rect(img, (k, 0, k + 1, h * 0.6), (60, 64, 68))
    return img


def lens(a, w, h):
    img = paint(BLACK, 0.2)(a, w, h)
    a.rect(img, (w * 0.2, h * 0.2, w * 0.8, h * 0.8), LENS)
    return glow(img, a, (w * 0.2, h * 0.2, w * 0.8, h * 0.8), LENS, 0.2, 1)


def bore(a, w, h):
    img = paint(BLACK, 0.2)(a, w, h)
    a.rect(img, (w * 0.3, h * 0.3, w * 0.7, h * 0.7), (6, 6, 8))
    return img


rec.paint = {'-z': side, '+z': side, '*': 'green'}
mag.paint = {'-z': magazine, '+z': magazine, '*': 'magedge'}
m.swatch('green', paint(GREEN, 0.4))
m.swatch('darkg', paint(DARKG, 0.3, 1))
m.swatch('black', paint(BLACK, 0.3))
m.swatch('stock', stock)
m.swatch('magedge', wood((160, 108, 52)))
m.swatch('notch', notch)
m.swatch('lens', lens)
m.swatch('bore', bore)

if __name__ == '__main__':
    m.build()
