#!/usr/bin/python3
"""c0-rounds: a squat olive ammo can of rifle rounds - stencilled sides, a lid with a handle, a
belt of brass rounds with yellow tips lying on top. The game's is 0.14 x 0.13 x 0.09 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel  # noqa: E402

OLIVE, LIME = (70, 90, 40), (190, 230, 40)
m = Model('rounds', HERE, seed=115)
m.material('main', 'paint')
can = m.box('can', (0, 0, 0), (0.13, 0.09, 0.08), '465A28')
m.box('lid', (0, 0.09, 0), (0.136, 0.014, 0.086), '3C4E22', paint='lid')
m.box('handle', (0, 0.104, 0), (0.06, 0.008, 0.014), '202020', paint='dark')
for i in range(5):                                                     # a belt of rounds on top
    x = -0.05 + i * 0.025
    m.cyl(f'round-{i}', (x, 0.104, 0.024), (0.014, 0.022, 0.014), 'D8B048', seg=6, paint={'side': 'brass', 'top': 'tip', 'bottom': 'brass'})
    m.cyl(f'tip-{i}', (x, 0.126, 0.024), (0.014, 0.008, 0.014), 'BEE628', seg=6, amt=0.3, kind='cone', paint={'side': 'tip', 'top': 'tip', 'bottom': 'tip'})


def side(a, w, h):
    img = paint(OLIVE, 0.7)(a, w, h)
    a.rect(img, (0, h * 0.1, w, h * 0.16), (50, 66, 28))
    img = a.text(img, '7.62 MM', h * 0.22, (w * 0.1, h * 0.35, w * 0.9, h * 0.7), (220, 210, 120), alpha=0.85)
    a.rect(img, (w * 0.08, h * 0.78, w * 0.92, h * 0.84), LIME)
    return img


def brass(a, w, h):
    img = steel((220, 180, 80))(a, w, h)
    a.rect(img, (0, h * 0.8, w, h), (160, 120, 50))
    return img


can.paint = {'-z': side, '+z': side, '*': 'olive'}
m.swatch('olive', paint(OLIVE, 0.7))
m.swatch('lid', lambda a, w, h: a.edge_dark(paint((60, 78, 34), 0.6)(a, w, h), 1, 0.7))
m.swatch('dark', paint('202020', 0.2))
m.swatch('brass', brass)
m.swatch('tip', paint(LIME, 0.2, 1))

if __name__ == '__main__':
    m.build()
