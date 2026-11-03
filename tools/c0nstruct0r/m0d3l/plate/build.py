#!/usr/bin/python3
"""c0-plate: the PLATE trap's pressure plate - a low steel slab with a diamond tread top inside a
hazard-striped border, a slit light in the middle textured from the muzzle corner (the game lights it
as the plate counts down), a red sensor strip and two buttons on each edge, rubber corner feet. The
game's is 0.94 x 0.04 x 0.94 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, rubber, glow  # noqa: E402

GREY, YEL, RED = (124, 130, 138), (230, 180, 30), (255, 40, 40)
m = Model('plate', HERE, seed=105)
m.material('main', 'paint')
slab = m.box('slab', (0, 0.003, 0), (0.86, 0.028, 0.86), '7C828A')
m.corner = (120, 26, 32)                                               # the slit light, unlit: dim red
m.box('light', (0, 0.031, 0), (0.22, 0.006, 0.032), '781A20', paint='CORNER')  # the game lights it (drawCap)
for i, (x, z) in enumerate(((0.425, 0.425), (-0.425, 0.425), (0.425, -0.425), (-0.425, -0.425))):
    m.box(f'foot-{i}', (x, 0, z), (0.09, 0.036, 0.09), '1C1C1E', paint={'+y': 'foottop', '*': 'rubber'})


def top(a, w, h):
    img = steel((150, 156, 164))(a, w, h)
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W] / a.K
    p = 7.0                                                            # diamond tread
    u, v = (xx + yy) % p, (xx - yy) % p
    bump = (np.abs(u - p / 2) < 0.7) & (np.abs(v - p / 2) < 2.2)
    img[bump] = img[bump] * 1.18
    sh = (np.abs(u - p / 2 - 0.7) < 0.35) & (np.abs(v - p / 2) < 2.2)
    img[sh] = img[sh] * 0.6
    b = w * 0.08                                                       # the hazard border
    ring = (xx < b) | (xx > w - b) | (yy < b) | (yy > h - b)
    stripe = ((xx + yy) / 5).astype(int) % 2 == 0
    img[ring & stripe] = YEL
    img[ring & ~stripe] = (30, 30, 32)
    a.rect(img, (b, b, w - b, b + 0.8), (60, 64, 70))
    a.rect(img, (b, h - b - 0.8, w - b, h - b), (200, 206, 214))
    img = np.clip(img, 0, 255)
    return a.edge_dark(img, 1.5, 0.7)


def edge(a, w, h):
    img = paint(GREY, 0.5)(a, w, h)
    box = (w * 0.38, h * 0.2, w * 0.58, h * 0.8)
    a.rect(img, box, (180, 20, 20))
    a.rect(img, (box[0] + 0.6, box[1] + 0.6, box[2] - 0.6, box[3] - 0.6), RED)
    img = glow(img, a, box, RED, 0.2, 1)
    for x in (0.64, 0.7):
        a.rect(img, (w * x, h * 0.3, w * x + h * 0.4, h * 0.7), (60, 64, 70))
        a.rect(img, (w * x + 0.4, h * 0.36, w * x + h * 0.32, h * 0.62), (110, 116, 124))
    return img


slab.paint = {'+y': top, '-y': 'under', '*': 'edge'}
m.swatch('edge', edge)
m.swatch('under', paint('3A3D42', 0.3))
m.swatch('rubber', rubber((30, 30, 32)))
m.swatch('foottop', rubber((40, 40, 43)))

if __name__ == '__main__':
    m.build()
