#!/usr/bin/python3
"""c0-labbench: a lab bench - steel cabinet of three drawers, a dark resin worktop, a microscope,
a round flask of red, a conical flask of green, a rack with a small orange flask. The game's is
0.44 x 0.38 x 0.22 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow  # noqa: E402

STEEL, TOP = '8E959E', '23262B'
m = Model('labbench', HERE, seed=41)
m.material('main', 'paint')
cab = m.box('cabinet', (0, 0, 0), (0.42, 0.22, 0.20), STEEL)
top = m.box('worktop', (0, 0.22, 0), (0.436, 0.02, 0.218), TOP, paint='resin')
# microscope
m.box('scope-base', (0.17, 0.24, 0.0), (0.055, 0.01, 0.045), '303338', paint='dark')
m.box('scope-pillar', (0.185, 0.25, 0.012), (0.012, 0.10, 0.012), 'B0B4BA', paint='steel')
m.box('scope-arm', (0.165, 0.33, 0.012), (0.035, 0.012, 0.012), 'B0B4BA', paint='steel')
m.box('scope-head', (0.15, 0.31, 0.012), (0.022, 0.05, 0.022), '40D060', paint='green')
# flasks
m.cyl('flask-round', (0.07, 0.24, -0.01), (0.075, 0.065, 0.075), 'D02020', seg=10,
      paint={'side': 'redflask', 'top': 'glass', 'bottom': 'glass'})
m.cyl('flask-round-neck', (0.07, 0.305, -0.01), (0.022, 0.05, 0.022), 'C0D8E0', seg=8,
      paint={'side': 'glass', 'top': 'glass', 'bottom': 'glass'})
m.cyl('flask-cone', (-0.045, 0.24, -0.01), (0.095, 0.085, 0.095), '30C040', seg=10, amt=0.3, kind='cone',
      paint={'side': 'greenflask', 'top': 'glass', 'bottom': 'glass'})
m.cyl('flask-cone-neck', (-0.045, 0.325, -0.01), (0.026, 0.035, 0.026), 'C0D8E0', seg=8,
      paint={'side': 'glass', 'top': 'glass', 'bottom': 'glass'})
m.box('rack-shelf', (-0.165, 0.29, 0.0), (0.07, 0.008, 0.045), 'B0B4BA', paint='steel')
for i, x in enumerate((-0.196, -0.134)):
    m.box(f'rack-post-{i}', (x, 0.24, 0.0), (0.008, 0.075, 0.008), 'B0B4BA', paint='steel')
m.cyl('flask-small', (-0.165, 0.24, 0.0), (0.035, 0.045, 0.035), 'E06020', seg=8,
      paint={'side': 'orangeflask', 'top': 'glass', 'bottom': 'glass'})


def cab_front(a, w, h):
    img = paint(STEEL)(a, w, h)
    a.rect(img, (0, h * 0.9, w, h), (40, 42, 46))                          # kick
    for k in range(3):
        x0, x1 = w * (0.03 + k * 0.325), w * (0.33 + k * 0.325) - w * 0.02
        a.rect(img, (x0, h * 0.06, x1, h * 0.86), (150, 158, 168))
        a.rect(img, (x0, h * 0.84, x1, h * 0.86), (70, 74, 80))
        a.rect(img, (x0 + (x1 - x0) * 0.3, h * 0.14, x1 - (x1 - x0) * 0.3, h * 0.2), (60, 62, 66))
        img = a.text(img, 'ABC'[k], h * 0.1, (x0, h * 0.3, x1, h * 0.42), (70, 74, 80), alpha=0.6)
    return img


def liquid(rgb, fill):
    """Glass with liquid up to `fill` of the height, a highlight streak."""
    def f(a, w, h):
        img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((196, 214, 222), np.float32)
        a.rect(img, (0, h * (1 - fill), w, h), rgb)
        a.rect(img, (0, h * (1 - fill), w, h * (1 - fill) + 0.8), tuple(min(255, v + 70) for v in rgb))
        for k in range(0, int(w), max(1, int(w / 5))):
            a.rect(img, (k + w * 0.05, h * 0.1, k + w * 0.05 + 0.8, h * 0.85), (255, 255, 255), 0.45)
        return img
    return f


cab.paint = {'-z': cab_front, '*': 'steelpaint'}
m.swatch('steelpaint', paint(STEEL))
m.swatch('resin', paint(TOP, 0.6))
m.swatch('dark', paint('303338', 0.3))
m.swatch('steel', steel())
m.swatch('green', lambda a, w, h: glow(paint((50, 200, 90), 0.1, 1)(a, w, h), a, (0, 0, w, h * 0.3), (150, 255, 170), 0.25, 1))
m.swatch('glass', liquid((196, 214, 222), 0))
m.swatch('redflask', liquid((210, 30, 40), 0.6))
m.swatch('greenflask', liquid((40, 200, 70), 0.7))
m.swatch('orangeflask', liquid((230, 100, 30), 0.55))

if __name__ == '__main__':
    m.build()
