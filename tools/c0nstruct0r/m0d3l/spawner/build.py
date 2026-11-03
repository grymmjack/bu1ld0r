#!/usr/bin/python3
"""c0-spawner: a monster spawn portal standing on edge - a worn sandstone frame (rounded corners
drawn), a sunk well with a pink energy ring and its brackets, a raised cyan core, four cyan arrow
lights round the frame, a dark back plate. The game's is 0.65 x 0.65 x 0.09 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, glow, front_box  # noqa: E402

SAND, PINK, CYAN = (170, 130, 92), (240, 80, 170), (50, 230, 240)
m = Model('spawner', HERE, seed=103)
m.material('main', 'paint')
frame = m.box('frame', (0, 0, -0.004), (0.645, 0.645, 0.06), 'AA825C', walls='well')
frame.cut('-z', (-0.24, 0.24, 0.0825, 0.5625), 0.018)
m.box('back', (0, 0.07, 0.038), (0.5, 0.5, 0.02), '2A2028', paint='backdark')
core = m.box('core', (0, 0.235, -0.03), (0.175, 0.175, 0.024), '32E6F0')
for i, (x, y, way) in enumerate(((0, 0.6, 'up'), (0, 0.01, 'down'), (0.29, 0.3, 'left'), (-0.29, 0.3, 'right'))):
    m.box(f'marker-{i}', (x, y, -0.036), (0.04, 0.035, 0.008), '32E6F0', paint={'-z': 'marker' + way, '*': 'markerside'})


def stone(a, w, h):
    from scipy.ndimage import gaussian_filter
    img = paint(SAND, 0.8, 0)(a, w, h)
    r = np.random.default_rng(7)
    n = gaussian_filter(r.normal(0, 1, img.shape[:2]), 3 * a.K)
    n = n / (np.abs(n).max() + 1e-6)
    img = img * (1 + 0.18 * n[..., None])                              # blotchy sandstone
    fine = r.uniform(0.9, 1.08, img.shape[:2])
    img = np.clip(img * fine[..., None], 0, 255).astype(np.float32)
    for _ in range(int(w * h / 40)):                                   # pits and chips
        x, y = r.uniform(0, w), r.uniform(0, h)
        a.rect(img, (x, y, x + r.uniform(0.6, 2), y + r.uniform(0.6, 1.5)), (120, 88, 60), 0.6)
    return a.edge_dark(img, 2, 0.75)


def front(a, w, h):
    img = stone(a, w, h)
    for cx, cy in ((0, 0), (w, 0), (0, h), (w, h)):                     # rounded corners: dark behind
        yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
        d = np.hypot(xx - cx, yy - cy)
        img[d < w * 0.07] = (40, 30, 34)
    s = front_box(frame, w, h, -0.24, 0.24, 0.0825, 0.5625)
    x0, y0, x1, y1 = s
    a.rect(img, (x0 - 2.5, y0 - 2.5, x1 + 2.5, y1 + 2.5), (110, 40, 50))
    a.rect(img, s, (60, 20, 40))
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d = np.hypot(xx - cx, yy - cy)
    R = (x1 - x0) * 0.45
    ring = (d > R * 0.78) & (d < R)
    img[ring] = PINK
    img[(d > R * 0.86) & (d < R * 0.9)] = (255, 190, 230)
    for t in np.linspace(0, 2 * np.pi, 16, endpoint=False):           # cracks of energy in the ring
        px, py = cx + np.cos(t) * R * 0.89, cy + np.sin(t) * R * 0.89
        a.rect(img, (px - 0.6, py - 0.6, px + 0.6, py + 0.6), (120, 30, 80))
    for ang in (0, 90, 180, 270):                                      # brackets over the ring
        t = np.radians(ang)
        px, py = cx + np.cos(t) * R * 0.89, cy + np.sin(t) * R * 0.89
        a.rect(img, (px - 3, py - 3, px + 3, py + 3), (90, 86, 92))
        a.rect(img, (px - 2, py - 2, px + 2, py + 2), (140, 136, 146))
    img = glow(img, a, (cx - R, cy - R, cx + R, cy + R), PINK, 0.18, 2)
    return img


def core_face(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((30, 34, 40), np.float32)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    img[d < 0.95] = (90, 96, 104)
    img[d < 0.85] = (20, 120, 140)
    t = np.clip(1 - d / 0.8, 0, 1)[..., None]
    inner = d < 0.8
    img[inner] = (np.array(CYAN) * (1 - t) + np.array((220, 255, 255)) * t)[inner]
    return glow(img, a, (w * 0.1, h * 0.1, w * 0.9, h * 0.9), CYAN, 0.2, 2)


def marker(way):
    def f(a, w, h):
        img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((30, 40, 46), np.float32)
        yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
        u, v = (xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2)          # -1..1
        t, s = {'up': (v, u), 'down': (-v, u), 'left': (u, v), 'right': (-u, v)}[way]
        img[(np.abs(s) < (t + 0.7) * 0.75) & (t < 0.7)] = CYAN          # an arrow pointing outward
        return img
    return f


frame.paint = {'-z': front, '+z': 'backstone', '*': 'stone'}
core.paint = {'-z': core_face, '*': 'coreside'}
m.swatch('stone', stone)
m.swatch('backstone', stone)
m.swatch('well', paint((60, 20, 40), 0.3, 1))
m.swatch('backdark', paint('2A2028', 0.4))
m.swatch('coreside', paint((90, 96, 104), 0.4))
for way in ('up', 'down', 'left', 'right'):
    m.swatch('marker' + way, marker(way))
m.swatch('markerside', paint((30, 40, 46), 0.2))

if __name__ == '__main__':
    m.build()
