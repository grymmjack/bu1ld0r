#!/usr/bin/python3
"""c0-overcharge: a bronze medallion standing on edge - an engraved rim, four studs, a raised cyan
crystal face of glowing facets. The game's is 0.26 x 0.27 x 0.03 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import steel, glow  # noqa: E402

BRONZE, CYAN = (190, 130, 60), (60, 210, 240)
m = Model('overcharge', HERE, seed=127)
m.material('main', 'steel')
rim = m.cyl('rim', (0, 0.1275, -0.01), (0.255, 0.022, 0.255), 'BE823C', seg=16, rot=(90, 0, 0))
face = m.cyl('face', (0, 0.1275, -0.022), (0.17, 0.012, 0.17), '3CD2F0', seg=16, rot=(90, 0, 0))
for i, (x, y) in enumerate(((0, 0.226), (0, 0.007), (0.1, 0.1155), (-0.1, 0.1155))):
    m.box(f'stud-{i}', (x, y, -0.016), (0.024, 0.024, 0.008), 'D8A050', paint='bronze')


def bronze(a, w, h):
    img = steel(BRONZE)(a, w, h)
    return a.edge_dark(img, 1, 0.75)


def rim_front(a, w, h):
    img = bronze(a, w, h)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    for r in (0.92, 0.72):
        img[np.abs(d - r) < 0.015] = (110, 70, 30)                     # engraved rings
    ang = np.arctan2(yy - h / 2, xx - w / 2)
    ticks = (np.abs(((ang / (2 * np.pi) * 24) % 1) - 0.5) > 0.44) & (d > 0.75) & (d < 0.9)
    img[ticks] = (240, 190, 110)
    return img


def crystal(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((20, 90, 130), np.float32)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    cx, cy = w / 2, h / 2
    ang = (np.arctan2(yy - cy, xx - cx) + np.pi) / (2 * np.pi)
    d = np.hypot(xx - cx, yy - cy) / (w / 2)
    fac = (ang * 8).astype(int) % 2
    img = img * (0.8 + 0.4 * fac[..., None]) + np.array(CYAN) * np.clip(1 - d, 0, 1)[..., None] * 0.8
    img[d < 0.25] = (210, 250, 255)
    img[(d > 0.9)] = (180, 120, 50)
    return glow(np.clip(img, 0, 255).astype(np.float32), a, (w * 0.2, h * 0.2, w * 0.8, h * 0.8), CYAN, 0.15, 2)


rim.paint = {'-z': rim_front, '+z': rim_front, '*': 'bronze'}
face.paint = {'-z': crystal, '*': 'bronze'}
m.swatch('bronze', bronze)

if __name__ == '__main__':
    m.build()
