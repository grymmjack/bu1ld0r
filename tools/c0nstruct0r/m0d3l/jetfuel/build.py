#!/usr/bin/python3
"""c0-jetfuel: a jetpack fuel canister - orange with black hazard bands, a gauge reading 31, a steel
filler cap and a carry handle on top. The game's is 0.15 x 0.27 x 0.08 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow  # noqa: E402

ORANGE = (240, 120, 30)
m = Model('jetfuel', HERE, seed=137)
m.material('main', 'paint')
can = m.box('can', (0, 0, 0), (0.14, 0.22, 0.08), 'F0781E')
m.cyl('cap', (0.035, 0.22, 0), (0.036, 0.022, 0.036), 'B0B6BE', seg=12, paint={'side': 'steel', 'top': 'steel', 'bottom': 'steel'})
for i, x in enumerate((-0.005, -0.055)):
    m.box(f'post-{i}', (x, 0.22, 0), (0.012, 0.035, 0.016), '202124', paint='dark')
m.box('handle', (-0.03, 0.255, 0), (0.066, 0.014, 0.018), '202124', paint='dark')


def face(a, w, h):
    img = paint(ORANGE, 0.6)(a, w, h)
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W] / a.K
    for y0, y1 in ((0.04, 0.2), (0.78, 0.95)):
        stripe = (((xx + yy) / 5).astype(int) % 2 == 0) & (yy > h * y0) & (yy < h * y1)
        img[stripe] = (30, 30, 32)
    a.rect(img, (w * 0.22, h * 0.3, w * 0.78, h * 0.5), (24, 26, 30))
    img = a.text(img, '31', h * 0.14, (w * 0.25, h * 0.31, w * 0.75, h * 0.49), (120, 255, 140))
    img = glow(img, a, (w * 0.22, h * 0.3, w * 0.78, h * 0.5), (120, 255, 140), 0.1, 1)
    a.rect(img, (w * 0.3, h * 0.58, w * 0.7, h * 0.66), (40, 40, 44))
    return img


can.paint = {'-z': face, '+z': face, '*': 'side'}
m.swatch('side', lambda a, w, h: a.edge_dark(paint(ORANGE, 0.6)(a, w, h), 1.5, 0.7))
m.swatch('steel', steel((176, 182, 190)))
m.swatch('dark', paint('202124', 0.3))

if __name__ == '__main__':
    m.build()
