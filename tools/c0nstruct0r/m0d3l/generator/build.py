#!/usr/bin/python3
"""c0-generator: a riveted grey power unit on a hazard-striped skid - a sunk furnace window, bars
over a glowing orange core, an amber lamp, side vents, three insulator coils (orange and blue
windings) with dark caps on top. The game's is 0.61 x 0.67 x 0.43 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow, front_box  # noqa: E402

GREY, ORANGE, BLUE, YEL = '5C636C', (255, 140, 30), (70, 130, 230), (240, 190, 30)
m = Model('generator', HERE, seed=83)
m.material('main', 'paint')
skid = m.box('skid', (0, 0, 0), (0.607, 0.045, 0.425), '202226')
body = m.box('body', (0, 0.045, 0), (0.56, 0.46, 0.38), GREY, walls='furnace')
body.cut('-z', (-0.17, 0.17, 0.12, 0.42), 0.035)
m.box('lamp', (0, 0.43, -0.195), (0.07, 0.025, 0.012), 'FF8C1E', paint='lamp')
for i, x in enumerate((0.17, 0, -0.17)):
    m.cyl(f'coil-{i}', (x, 0.505, 0), (0.1, 0.135, 0.1), '4682E6', seg=8, paint={'side': 'coil', 'top': 'capdark', 'bottom': 'capdark'})
    m.cyl(f'coilcap-{i}', (x, 0.64, 0), (0.055, 0.027, 0.055), '2A2D32', seg=8, paint={'side': 'capside', 'top': 'capdark', 'bottom': 'capdark'})


def riveted(a, w, h, img=None):
    img = paint(GREY, 0.6)(a, w, h) if img is None else img
    for x in (2.5, w - 2.5):
        for y in np.arange(3, h - 1, 9):
            a.rect(img, (x - 0.9, y - 0.9, x + 0.9, y + 0.9), (130, 138, 148))
            a.rect(img, (x - 0.9, y + 0.4, x + 0.9, y + 0.9), (40, 44, 50))
    return img


def front(a, w, h):
    img = riveted(a, w, h)
    s = front_box(body, w, h, -0.17, 0.17, 0.12, 0.42)
    x0, y0, x1, y1 = s
    a.rect(img, (x0 - 2, y0 - 2, x1 + 2, y1 + 2), (36, 39, 44))
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    cx, cy = (x0 + x1) / 2, y0 + (y1 - y0) * 0.6
    d = np.hypot((xx - cx) / (x1 - x0), (yy - cy) / (y1 - y0))
    inside = (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)
    heat = np.clip(1 - d * 1.6, 0, 1)[..., None]
    core = np.array((150, 40, 10)) * (1 - heat) + np.array((255, 230, 120)) * heat
    img[inside] = core[inside]
    for k in range(9):                                                 # the bars
        bx = x0 + (x1 - x0) * (k + 0.5) / 9
        a.rect(img, (bx - 1, y0, bx + 1, y1), (30, 32, 36))
        a.rect(img, (bx - 1, y0, bx - 0.4, y1), (90, 96, 104))
    img = glow(img, a, s, ORANGE, 0.22, 2)
    return img


def side(a, w, h):
    img = riveted(a, w, h)
    for k in range(8):
        y = h * (0.2 + k * 0.07)
        a.rect(img, (w * 0.25, y, w * 0.75, y + h * 0.03), (26, 28, 32))
    a.rect(img, (w * 0.1, h * 0.85, w * 0.9, h * 0.88), (40, 44, 50))   # a conduit
    return img


def hazard(a, w, h):
    img = paint('202226', 0.4)(a, w, h)
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W] / a.K
    band = (((xx + yy) / 6).astype(int) % 2 == 0) & (yy > h * 0.18) & (yy < h * 0.82)
    img[band] = img[band] * 0.25 + np.array(YEL) * 0.75
    return img


def coil(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((40, 44, 50), np.float32)
    n = 6
    for k in range(n):                                                 # windings, alternating
        y0 = h * (0.05 + k * 0.9 / n)
        c = ORANGE if k % 2 == 0 else BLUE
        a.rect(img, (0, y0, w, y0 + h * 0.9 / n * 0.8), c)
        a.rect(img, (0, y0, w, y0 + 0.7), tuple(min(255, v + 70) for v in c))
    return a.edge_dark(img, 1, 0.8)


def lamp(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((255, 170, 60), np.float32)
    a.rect(img, (w * 0.1, h * 0.2, w * 0.9, h * 0.5), (255, 230, 170))
    return img


body.paint = {'-z': front, '+y': 'top', '*': 'side'}
skid.paint = {'-z': 'hazard', '+z': 'hazard', '+x': 'hazard', '-x': 'hazard', '*': 'skidtop'}
m.swatch('side', side)
m.swatch('top', lambda a, w, h: riveted(a, w, h, paint(GREY, 0.5)(a, w, h)))
m.swatch('furnace', paint('302A26', 0.3, 1))
m.swatch('hazard', hazard)
m.swatch('skidtop', paint('202226', 0.4))
m.swatch('lamp', lamp)
m.swatch('coil', coil)
m.swatch('capdark', paint('2A2D32', 0.3))
m.swatch('capside', lambda a, w, h: a.edge_dark(steel((110, 116, 124))(a, w, h), 1, 0.6))

if __name__ == '__main__':
    m.build()
