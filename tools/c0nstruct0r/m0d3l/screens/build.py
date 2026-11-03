#!/usr/bin/python3
"""c0-screens: a monitor wall on a stand - a dark bezel round six sunk displays (green radar, blue
grid scope, cyan target lock, purple waveform, orange core readout, red graphs), a housing behind,
a post and foot. The game's is 0.79 x 0.79 x 0.11 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, glow, front_box  # noqa: E402

BEZEL = '1A1D22'
m = Model('screens', HERE, seed=91)
m.material('main', 'plastic')
m.box('foot', (0, 0, 0.0), (0.24, 0.02, 0.108), '202328', paint='dark')
m.box('post', (0, 0.02, 0.025), (0.07, 0.11, 0.04), '2A2D32', paint='post')
frame = m.box('frame', (0, 0.12, -0.012), (0.79, 0.67, 0.05), BEZEL, walls='bezelin')
frame.cut('-z', (-0.375, 0.375, 0.135, 0.775), 0.008)
m.box('housing', (0, 0.26, 0.033), (0.5, 0.4, 0.04), '24272C', paint={'+z': 'housingback', '*': 'dark'})

G, B, C, P, O, R = (70, 230, 110), (60, 150, 255), (40, 230, 255), (190, 90, 230), (255, 120, 40), (255, 70, 80)


def panel(a, img, box, kind, r):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W] / a.K
    ins = (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)
    base = {'radar': (8, 30, 16), 'grid': (8, 18, 40), 'target': (6, 26, 34), 'wave': (24, 10, 36),
            'core': (30, 14, 8), 'graph': (32, 10, 14)}[kind]
    img[ins] = base
    col = {'radar': G, 'grid': B, 'target': C, 'wave': P, 'core': O, 'graph': R}[kind]
    d = np.hypot(xx - cx, yy - cy)
    rad = min(w, h) * 0.36
    if kind in ('radar', 'target', 'core', 'grid'):
        for k in (0.35, 0.7, 1.0):
            ring = ins & (np.abs(d - rad * k) < 0.45)
            img[ring] = col
        img[ins & (np.abs(xx - cx) < 0.3) & (d < rad)] = col
        img[ins & (np.abs(yy - cy) < 0.3) & (d < rad)] = col
    if kind == 'radar':                                                # a sweep and blips
        ang = np.arctan2(yy - cy, xx - cx)
        sw = ins & (d < rad) & (ang > -0.9) & (ang < 0)
        img[sw] = img[sw] * 0.4 + np.array(G) * 0.6
        for _ in range(4):
            bx, by = cx + r.uniform(-rad, rad) * 0.7, cy + r.uniform(-rad, rad) * 0.7
            a.rect(img, (bx - 0.8, by - 0.8, bx + 0.8, by + 0.8), (200, 255, 200))
    if kind == 'grid':
        for t in np.arange(x0 + 2, x1, w / 8):
            img[ins & (np.abs(xx - t) < 0.2)] = np.array(B) * 0.5
        for t in np.arange(y0 + 2, y1, h / 6):
            img[ins & (np.abs(yy - t) < 0.2)] = np.array(B) * 0.5
        img[ins & (d < rad * 0.15)] = (200, 230, 255)
    if kind == 'target':
        img[ins & (np.abs(d - rad * 0.55) < 1.2)] = col
        img[ins & (d < rad * 0.12)] = (220, 255, 255)
    if kind == 'core':
        img[ins & (d < rad * 0.5)] = (255, 90, 30)
        img[ins & (d < rad * 0.3)] = (255, 200, 120)
    if kind == 'wave':
        t = (xx - x0) / w
        yv = cy + np.sin(t * 9) * h * 0.18 * np.exp(-((t - 0.5) ** 2) * 6)
        fill = ins & (yy > yv) & (yy < cy + h * 0.25)
        img[fill] = img[fill] * 0.4 + np.array(P) * 0.6
        img[ins & (np.abs(yy - yv) < 0.6)] = (240, 180, 255)
    if kind == 'graph':
        for k in range(10):
            bh = r.uniform(0.15, 0.7) * h
            bx = x0 + w * (0.08 + k * 0.088)
            a.rect(img, (bx, y1 - h * 0.1 - bh, bx + w * 0.06, y1 - h * 0.1), R if k % 3 else O)
        pts = np.cumsum(r.uniform(-1, 1, 30)) * h * 0.03
        for k in range(29):
            px = x0 + w * (0.05 + k * 0.03)
            a.rect(img, (px, y0 + h * 0.3 + pts[k], px + w * 0.03, y0 + h * 0.3 + pts[k] + 0.6), (255, 200, 120))
    a.rect(img, (x0 + 1, y0 + 1, x0 + w * 0.4, y0 + 2), col, 0.8)       # a title bar
    a.rect(img, (x1 - w * 0.2, y0 + 1, x1 - 1, y0 + 2), col, 0.5)
    for yv in np.arange(y0, y1, 1.0):                                  # scan lines
        a.rect(img, (x0, yv, x1, yv + 0.25), (0, 0, 0), 0.25)
    return glow(img, a, box, col, 0.12, 1)


def front(a, w, h):
    img = paint(BEZEL, 0.4)(a, w, h)
    s = front_box(frame, w, h, -0.375, 0.375, 0.135, 0.775)
    x0, y0, x1, y1 = s
    r = np.random.default_rng(2)
    a.rect(img, s, (8, 9, 11))
    kinds = [['radar', 'grid', 'target'], ['wave', 'core', 'graph']]
    gw, gh = (x1 - x0) / 3, (y1 - y0) / 2
    for j in range(2):
        for i in range(3):
            box = (x0 + i * gw + 1.2, y0 + j * gh + 1.2, x0 + (i + 1) * gw - 1.2, y0 + (j + 1) * gh - 1.2)
            img = panel(a, img, box, kinds[j][i], r)
    a.rect(img, (w * 0.47, h - 2.6, w * 0.53, h - 1.4), (90, 240, 120))   # power light
    return img


def housing_back(a, w, h):
    img = paint('24272C', 0.4)(a, w, h)
    for k in range(10):
        y = h * (0.15 + k * 0.07)
        a.rect(img, (w * 0.15, y, w * 0.85, y + h * 0.03), (14, 15, 17))
    return img


frame.paint = {'-z': front, '*': 'bezel'}
m.swatch('bezel', paint(BEZEL, 0.4))
m.swatch('bezelin', paint('101114', 0.2, 1))
m.swatch('dark', paint('202328', 0.4))
m.swatch('post', paint('2A2D32', 0.4))
m.swatch('housingback', housing_back)

if __name__ == '__main__':
    m.build()
