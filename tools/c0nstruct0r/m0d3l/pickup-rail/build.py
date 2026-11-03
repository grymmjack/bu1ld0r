#!/usr/bin/python3
"""c0-pickup-rail: the railgun lying in wait - a long dark green body with a white stripe and a
black underside, a black barrel out front (the muzzle to -x), a top rail and a scope with a green
lens, a skeleton stock. The game's is 0.44 x 0.14 x 0.03 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, glow  # noqa: E402

GREEN, BLACK, LENS = (30, 96, 60), '1C1E20', (110, 255, 150)
m = Model('pickup-rail', HERE, seed=151)
m.material('main', 'paint')
body = m.box('body', (-0.02, 0.045, 0), (0.28, 0.05, 0.03), '1E603C')
m.box('barrel', (-0.19, 0.058, 0), (0.06, 0.022, 0.018), BLACK, paint='black')
m.box('muzzle', (-0.212, 0.053, 0), (0.014, 0.032, 0.024), '1E603C', paint='green')
m.box('under', (-0.12, 0.03, 0), (0.08, 0.016, 0.024), '1E603C', paint='green')
m.box('rail', (-0.02, 0.095, 0), (0.18, 0.012, 0.02), BLACK, paint={'-z': 'notch', '+z': 'notch', '*': 'black'})
m.box('scope', (0.03, 0.107, 0), (0.05, 0.029, 0.018), BLACK, paint={'-x': 'lens', '+x': 'lens', '*': 'black'})
m.box('sight', (-0.1, 0.107, 0), (0.012, 0.018, 0.012), BLACK, paint='black')
m.box('stock-bar', (0.155, 0.07, 0), (0.11, 0.02, 0.022), '1E603C', paint='green')
m.box('stock-strut', (0.16, 0.02, 0), (0.09, 0.012, 0.016), BLACK, paint='black')
m.box('butt', (0.209, 0.0, 0), (0.018, 0.09, 0.026), BLACK, paint='rubber')
m.box('grip', (0.07, 0.0, 0), (0.026, 0.045, 0.022), BLACK, paint='rubber')


def side(a, w, h):
    img = paint(GREEN, 0.4)(a, w, h)
    a.rect(img, (0, h * 0.62, w, h), (28, 30, 32))                  # the black underside
    a.rect(img, (w * 0.04, h * 0.3, w * 0.96, h * 0.42), (225, 232, 228))   # the stripe
    for u in (0.3, 0.7):                                              # panel lines
        a.rect(img, (w * u, 0, w * u + 0.5, h * 0.62), (16, 50, 32))
    a.rect(img, (w * 0.45, h * 0.12, w * 0.55, h * 0.24), (200, 210, 205))   # the badge
    return img


def notch(a, w, h):
    img = paint(BLACK, 0.2)(a, w, h)
    for k in np.arange(1, w, 2.5):
        a.rect(img, (k, 0, k + 1, h * 0.6), (60, 64, 68))
    return img


def lens(a, w, h):
    img = paint(BLACK, 0.2)(a, w, h)
    a.rect(img, (w * 0.2, h * 0.2, w * 0.8, h * 0.8), LENS)
    return glow(img, a, (w * 0.2, h * 0.2, w * 0.8, h * 0.8), LENS, 0.2, 1)


body.paint = {'-z': side, '+z': side, '*': 'green'}
m.swatch('green', paint(GREEN, 0.4))
m.swatch('black', paint(BLACK, 0.3))
m.swatch('rubber', paint('141516', 0.2, 1))
m.swatch('notch', notch)
m.swatch('lens', lens)

if __name__ == '__main__':
    m.build()
