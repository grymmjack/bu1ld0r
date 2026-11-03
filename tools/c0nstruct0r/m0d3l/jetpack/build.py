#!/usr/bin/python3
"""c0-jetpack: two orange-and-black fuel tanks on a dark harness plate - striped tanks with gauges,
steel caps, dark nozzles below glowing at their mouths, shoulder straps in front. The game's is
0.22 x 0.27 x 0.10 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, rubber, glow  # noqa: E402

ORANGE, DARK = (240, 120, 30), '24262A'
m = Model('jetpack', HERE, seed=135)
m.material('main', 'paint')
plate = m.box('plate', (0, 0.05, 0.03), (0.12, 0.2, 0.03), DARK)
for i, x in enumerate((0.07, -0.07)):
    m.cyl(f'tank-{i}', (x, 0.05, 0), (0.072, 0.19, 0.072), 'F0781E', seg=12, paint={'side': 'tank', 'top': 'dark', 'bottom': 'dark'})
    m.cyl(f'cap-{i}', (x, 0.24, 0), (0.05, 0.03, 0.05), 'B0B6BE', seg=12, paint={'side': 'steel', 'top': 'steel', 'bottom': 'steel'})
    m.cyl(f'nozzle-{i}', (x, 0.0, 0), (0.05, 0.05, 0.05), '1A1A1C', seg=12, amt=0.7, kind='cone', paint={'side': 'nozzle', 'top': 'dark', 'bottom': 'flame'})
    m.box(f'strap-{i}', (x * 0.5, 0.06, -0.04), (0.022, 0.18, 0.01), '141516', paint='strap')


def tank(a, w, h):
    img = paint(ORANGE, 0.5)(a, w, h)
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W] / a.K
    stripe = (((xx + yy) / 5).astype(int) % 2 == 0) & (yy > h * 0.62) & (yy < h * 0.82)
    img[stripe] = (30, 30, 32)
    col = w / 12
    for cx in (0, w):                                                  # a gauge at the front (u = 0: both edges)
        d = np.hypot(xx - cx, yy - h * 0.3)
        img[d < col * 0.8] = (40, 42, 46)
        img[d < col * 0.6] = (230, 240, 230)
        needle = (np.abs((yy - h * 0.3) + (xx - cx) * 0.6) < 0.35) & (d < col * 0.5)
        img[needle] = (200, 30, 30)
    for k in range(1, 12):                                             # seams, not across the gauge
        a.rect(img, (k * col - 0.3, 0, k * col + 0.3, h), (180, 80, 20))
    return img


def plate_front(a, w, h):
    img = paint(DARK, 0.5)(a, w, h)
    for k in range(5):
        y = h * (0.15 + k * 0.15)
        a.rect(img, (w * 0.3, y, w * 0.7, y + h * 0.05), (14, 15, 17))
    a.rect(img, (w * 0.42, h * 0.88, w * 0.58, h * 0.94), (90, 240, 120))
    return img


def flame(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((26, 26, 28), np.float32)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    img[d < 0.6] = (255, 140, 40)
    img[d < 0.3] = (255, 230, 160)
    return img


plate.paint = {'-z': plate_front, '+z': plate_front, '*': 'dark'}
m.swatch('tank', tank)
m.swatch('dark', paint(DARK, 0.4))
m.swatch('steel', steel((176, 182, 190)))
m.swatch('nozzle', lambda a, w, h: a.edge_dark(steel((70, 72, 78))(a, w, h), 0.6, 0.7))
m.swatch('flame', flame)
m.swatch('strap', rubber((24, 24, 26)))

if __name__ == '__main__':
    m.build()
