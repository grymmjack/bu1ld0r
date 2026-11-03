#!/usr/bin/python3
"""c0-map: a level map standing on edge - worn parchment with fold lines, rivers, roads, green
woods, room outlines and a blue crystal marking you, a blue gem pin stuck in it. The game's is
0.28 x 0.28 x 0.02 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, glow  # noqa: E402

PAPER, BLUE = (214, 176, 112), (60, 170, 255)
m = Model('map', HERE, seed=141)
m.material('main', 'paint')
sheet = m.box('sheet', (0, 0, 0.004), (0.284, 0.284, 0.008), 'D6B070')
m.cyl('pin', (0.0, 0.15, -0.012), (0.034, 0.05, 0.034), '3CAAFF', seg=8, amt=0.25, kind='diamond',
      paint={'side': 'gem', 'top': 'gem', 'bottom': 'gem'})


def parchment(a, w, h, seed=3):
    from scipy.ndimage import gaussian_filter
    r = np.random.default_rng(seed)
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array(PAPER, np.float32)
    n = gaussian_filter(r.normal(0, 1, img.shape[:2]), 4 * a.K)
    img = img * (1 + 0.6 * n[..., None] / (np.abs(n).max() + 1e-6) * 0.25)
    return a.edge_dark(np.clip(img, 0, 255).astype(np.float32), 3, 0.65)


def front(a, w, h):
    img = parchment(a, w, h)
    r = np.random.default_rng(8)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    river = np.abs(yy - (h * 0.75 + np.sin(xx / w * 7) * h * 0.06)) < 1.2      # a river
    img[river] = (70, 140, 200)
    for _ in range(9):                                                 # woods
        cx, cy, rr = r.uniform(0, w), r.uniform(h * 0.05, h * 0.6), r.uniform(3, 7)
        img[np.hypot(xx - cx, yy - cy) < rr] = (70, 140, 60)
    for (x0, y0, x1, y1) in ((0.15, 0.2, 0.45, 0.42), (0.55, 0.15, 0.82, 0.35), (0.6, 0.45, 0.88, 0.62)):
        for t in (0, 0.6):                                             # room outlines
            a.rect(img, (w * x0, h * y0 + t, w * x1, h * y0 + t + 0.6), (90, 60, 40))
        a.rect(img, (w * x0, h * y1, w * x1, h * y1 + 0.6), (90, 60, 40))
        a.rect(img, (w * x0, h * y0, w * x0 + 0.6, h * y1), (90, 60, 40))
        a.rect(img, (w * x1, h * y0, w * x1 + 0.6, h * y1 + 0.6), (90, 60, 40))
    for k in range(40):                                                # a dotted road
        x = w * (0.05 + k * 0.023)
        a.rect(img, (x, h * 0.5 + np.sin(k / 4) * 3, x + 0.8, h * 0.5 + np.sin(k / 4) * 3 + 0.8), (120, 80, 50))
    for u in (1 / 3, 2 / 3):                                           # fold lines
        a.rect(img, (w * u, 0, w * u + 0.5, h), (170, 130, 80))
        a.rect(img, (0, h * u, w, h * u + 0.5), (170, 130, 80))
    a.rect(img, (w * 0.08, h * 0.86, w * 0.18, h * 0.93), (150, 40, 30))   # an X
    return img


def gem(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array(BLUE, np.float32)
    col = w / 8
    for k in range(8):
        a.rect(img, (k * col, 0, k * col + col * 0.4, h), (150, 220, 255), 0.6)
    return glow(img, a, (0, 0, w, h), (150, 220, 255), 0.15, 1)


sheet.paint = {'-z': front, '+z': lambda a, w, h: parchment(a, w, h, 5), '*': 'edge'}
m.swatch('edge', paint(PAPER, 0.2))
m.swatch('gem', gem)

if __name__ == '__main__':
    m.build()
