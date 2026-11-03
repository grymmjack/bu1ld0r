#!/usr/bin/python3
"""c0-tank: a round pressure tank - grey riveted armour plates round the drum on four dark feet, a
badge with an orange arrow at the front, an orange shoulder up to a dark neck, a glowing orange
filler lid. The game's is 0.45 x 0.52 x 0.45 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow  # noqa: E402

GREY, ORANGE, DARK = (112, 120, 130), (236, 120, 30), '24272C'
m = Model('tank', HERE, seed=85)
m.material('main', 'paint')
for i, (x, z) in enumerate(((0.13, 0.13), (-0.13, 0.13), (0.13, -0.13), (-0.13, -0.13))):
    m.box(f'foot-{i}', (x, 0, z), (0.06, 0.05, 0.06), DARK, paint='dark')
m.cyl('base', (0, 0.05, 0), (0.40, 0.03, 0.40), '30343A', seg=12, paint={'side': 'dark', 'top': 'dark', 'bottom': 'dark'})
m.cyl('drum', (0, 0.08, 0), (0.445, 0.28, 0.445), '707882', seg=12, paint={'side': 'drum', 'top': 'dark', 'bottom': 'dark'})
m.cyl('shoulder', (0, 0.36, 0), (0.43, 0.09, 0.43), 'EC781E', seg=12, amt=0.62, kind='cone',
      paint={'side': 'shoulder', 'top': 'dark', 'bottom': 'dark'})
m.cyl('neck', (0, 0.45, 0), (0.22, 0.035, 0.22), DARK, seg=12, paint={'side': 'neck', 'top': 'dark', 'bottom': 'dark'})
m.cyl('lid', (0, 0.485, 0), (0.25, 0.031, 0.25), '50565E', seg=12, paint={'side': 'lidside', 'top': 'lidtop', 'bottom': 'dark'})


def drum(a, w, h):
    img = paint(GREY, 0.7)(a, w, h)
    col = w / 12
    for k in range(0, 13, 2):                                          # a plate every two columns
        a.rect(img, (k * col - 0.6, 0, k * col + 0.6, h), (40, 44, 50))
        for y in np.arange(4, h - 2, 10):
            for x in (k * col - 2.6, k * col + 2.6):
                a.rect(img, (x - 0.8, y - 0.8, x + 0.8, y + 0.8), (160, 168, 176))
    a.rect(img, (0, h * 0.5 - 0.5, w, h * 0.5 + 0.5), (60, 64, 70))
    a.rect(img, (0, 0, w, 1.5), (50, 54, 60))
    a.rect(img, (0, h - 1.5, w, h), (50, 54, 60))
    for cx in (0, w):                                                  # the badge at the front (u = 0)
        yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
        d = np.hypot(xx - cx, yy - h * 0.5)
        r = h * 0.2
        img[d < r] = (60, 66, 74)
        img[d < r * 0.82] = (150, 158, 168)
        tri = (np.abs(xx - cx) < (yy - (h * 0.5 - r * 0.5)) * 0.8) & (yy < h * 0.5 + r * 0.25)
        img[tri & (d < r * 0.82)] = ORANGE
        stem = (np.abs(xx - cx) < r * 0.15) & (yy > h * 0.5) & (yy < h * 0.5 + r * 0.55)
        img[stem] = ORANGE
    return img


def shoulder(a, w, h):
    img = paint(ORANGE, 0.6)(a, w, h)
    col = w / 12
    for k in range(13):
        a.rect(img, (k * col - 0.4, 0, k * col + 0.4, h), (150, 70, 14))
    for k in range(12):
        a.rect(img, (k * col + col / 2 - 1.2, h * 0.65, k * col + col / 2 + 1.2, h * 0.65 + 2.4), (50, 54, 60))
    return img


def neck(a, w, h):
    img = paint(DARK, 0.4)(a, w, h)
    for k in range(12):
        a.rect(img, (k * w / 12, h * 0.3, k * w / 12 + 0.8, h * 0.7), (90, 96, 104))
    return img


def lid_top(a, w, h):
    img = steel((150, 156, 164))(a, w, h)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2)
    img[d < w * 0.42] = (60, 64, 70)
    img[d < w * 0.36] = ORANGE
    img[d < w * 0.28] = (255, 190, 90)
    return glow(img, a, (w * 0.14, h * 0.14, w * 0.86, h * 0.86), (255, 150, 50), 0.15, 2)


m.swatch('dark', paint(DARK, 0.4))
m.swatch('drum', drum)
m.swatch('shoulder', shoulder)
m.swatch('neck', neck)
m.swatch('lidside', lambda a, w, h: a.edge_dark(steel((120, 126, 134))(a, w, h), 1, 0.6))
m.swatch('lidtop', lid_top)

if __name__ == '__main__':
    m.build()
