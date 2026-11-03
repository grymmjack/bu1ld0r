#!/usr/bin/python3
"""c0-specimen: a specimen tank - a dark steel base with a status light, a round tank of glowing
green fluid (a spiny creature floating at the front, bubbles rising, light strips down the glass),
a bolted cap and a filler ring. The game's is 0.53 x 0.83 x 0.53 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow  # noqa: E402

DARK, GREEN = '33373D', (60, 200, 70)
m = Model('specimen', HERE, seed=101)
m.material('main', 'plastic')
m.cyl('base', (0, 0, 0), (0.53, 0.1, 0.53), DARK, seg=12, paint={'side': 'baseside', 'top': 'dark', 'bottom': 'dark'})
m.cyl('tank', (0, 0.1, 0), (0.46, 0.62, 0.46), '3CC846', seg=12, paint={'side': 'fluid', 'top': 'dark', 'bottom': 'dark'})
m.cyl('cap', (0, 0.72, 0), (0.5, 0.08, 0.5), '5A6068', seg=12, paint={'side': 'capside', 'top': 'captop', 'bottom': 'dark'})
m.cyl('filler', (0, 0.8, 0), (0.3, 0.033, 0.3), DARK, seg=12, paint={'side': 'dark', 'top': 'fillertop', 'bottom': 'dark'})


def fluid(a, w, h):
    H, W = int(a.px(h)), int(a.px(w))
    yy, xx = np.mgrid[0:H, 0:W] / a.K
    v = yy / h
    img = (np.array((10, 50, 16)) * v[..., None] + np.array((60, 170, 60)) * (1 - v[..., None])).astype(np.float32)
    col = w / 12
    u = np.minimum(xx, w - xx)                                         # distance round from the front (u = 0)
    s = np.where(xx < w / 2, 1, -1)
    ux = u * s                                                         # signed: + to the right of the front
    # the creature: a long body leaning, a head, spines, legs, all within 2 columns of the front
    body = ((ux / (col * 0.55)) ** 2 + ((v - 0.42) / 0.28) ** 2) < 1
    head = ((ux - col * 0.1) / (col * 0.35)) ** 2 + ((v - 0.12) / 0.09) ** 2 < 1
    legs = np.zeros_like(body)
    for lx, ly in ((-0.5, 0.62), (0.5, 0.62), (-0.35, 0.78), (0.35, 0.78)):
        legs |= (np.abs(ux - col * lx * (1 + (v - ly) * 2)) < col * 0.07) & (v > ly) & (v < ly + 0.2)
    spines = np.zeros_like(body)
    for k in range(7):
        sy = 0.25 + k * 0.05
        for side in (-1, 1):
            tip = col * (0.55 + 0.35 * (1 - abs(k - 3) / 4)) * side
            t = (ux - col * 0.4 * side) / (tip - col * 0.4 * side)
            spines |= (t > 0) & (t < 1) & (np.abs(v - sy - t * 0.03) < 0.006 * (1.2 - t))
    shape = body | head | legs | spines
    img[shape] = img[shape] * 0.2 + np.array((8, 22, 10)) * 0.8
    r = np.random.default_rng(4)
    for _ in range(int(w * 0.8)):                                      # bubbles
        bx, by = r.uniform(0, w), r.uniform(0, h)
        a.rect(img, (bx, by, bx + 0.8, by + 0.8), (190, 255, 190), 0.75)
    for k in range(12):                                                # light strips at every other column edge
        if k % 3 == 1:
            x = k * col
            a.rect(img, (x - 0.8, h * 0.04, x + 0.8, h * 0.96), (150, 255, 140))
            img = glow(img, a, (x - 0.8, h * 0.04, x + 0.8, h * 0.96), GREEN, 0.18, 1)
    a.rect(img, (0, 0, w, 1.2), (30, 34, 38))
    a.rect(img, (0, h - 1.2, w, h), (30, 34, 38))
    return img


def base_side(a, w, h):
    img = paint(DARK, 0.6)(a, w, h)
    col = w / 12
    for k in range(13):
        a.rect(img, (k * col - 0.5, 0, k * col + 0.5, h), (20, 22, 26))
    a.rect(img, (0, h * 0.15, w, h * 0.22), (90, 96, 104))
    for cx in (0, w):                                                  # the status light at the front
        yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
        d = np.hypot(xx - cx, yy - h * 0.55)
        img[d < h * 0.16] = (140, 150, 160)
        img[d < h * 0.1] = (120, 240, 255)
    return img


def cap_side(a, w, h):
    img = paint((90, 96, 104), 0.6)(a, w, h)
    col = w / 12
    for k in range(12):
        a.rect(img, (k * col + col / 2 - 1, h * 0.35, k * col + col / 2 + 1, h * 0.35 + 2), (40, 44, 50))
    a.rect(img, (0, h - 1.5, w, h), (40, 44, 50))
    return img


def filler_top(a, w, h):
    img = steel((150, 156, 164))(a, w, h)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    img[d < 0.6] = (40, 44, 50)
    img[d < 0.4] = (60, 200, 70)
    return img


m.swatch('fluid', fluid)
m.swatch('baseside', base_side)
m.swatch('dark', paint(DARK, 0.5))
m.swatch('capside', cap_side)
m.swatch('captop', paint((90, 96, 104), 0.6))
m.swatch('fillertop', filler_top)

if __name__ == '__main__':
    m.build()
