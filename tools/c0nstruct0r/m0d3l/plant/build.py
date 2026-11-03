#!/usr/bin/python3
"""c0-plant: a potted office tree - a terracotta pot with a rolled rim and dark soil, a forked brown
trunk, four low-poly leaf clumps (glossy greens). The game's is 0.28 x 0.56 x 0.28 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, wood  # noqa: E402

CLAY, SOIL, BARK = (176, 92, 56), (52, 36, 28), (100, 64, 40)
m = Model('plant', HERE, seed=89)
m.material('main', 'plastic')
m.cyl('pot', (0, 0, 0), (0.2, 0.17, 0.2), 'B05C38', seg=12, paint={'side': 'pot', 'top': 'soil', 'bottom': 'clay'})
m.cyl('rim', (0, 0.17, 0), (0.25, 0.04, 0.25), 'B85F3A', seg=12, paint={'side': 'rim', 'top': 'soiltop', 'bottom': 'clay'})
m.box('trunk', (0, 0.21, 0), (0.024, 0.13, 0.024), '644028', paint='bark')
m.box('branch-0', (0.025, 0.3, 0), (0.05, 0.016, 0.016), '644028', paint='bark')
m.box('branch-1', (-0.022, 0.33, 0.01), (0.044, 0.014, 0.014), '644028', paint='bark')
for i, (x, y, z, d, h) in enumerate(((0.045, 0.28, 0.0, 0.2, 0.15), (-0.045, 0.31, 0.02, 0.19, 0.15),
                                     (0.0, 0.36, -0.03, 0.2, 0.15), (0.0, 0.43, 0.01, 0.15, 0.13))):
    m.cyl(f'leaves-{i}', (x, y, z), (d, h, d), '3C9040', seg=8, kind='sphere',
          paint={'side': f'leaves{i % 2}', 'top': f'leaves{i % 2}', 'bottom': f'leaves{i % 2}'})


def leaves(seed):
    def f(a, w, h):
        r = np.random.default_rng(seed)
        img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((24, 70, 34), np.float32)
        H, W = img.shape[:2]
        yy, xx = np.mgrid[0:H, 0:W] / a.K
        for _ in range(int(w * h / 6)):                                # leaves: little pointed ovals
            cx, cy = r.uniform(0, w), r.uniform(0, h)
            L, t = r.uniform(3, 6), r.uniform(0, np.pi)
            g = r.uniform(0.7, 1.25)
            c = np.array((60 * g, 150 * g, 64 * g))
            u = (xx - cx) * np.cos(t) + (yy - cy) * np.sin(t)
            v = -(xx - cx) * np.sin(t) + (yy - cy) * np.cos(t)
            leaf = (u / L) ** 2 + (v / (L * 0.42)) ** 2 < 1
            img[leaf] = c
            vein = leaf & (np.abs(v) < 0.25)
            img[vein] = c * 0.75
            hi = leaf & (v < -L * 0.18) & (u < 0)
            img[hi] = np.minimum(c * 1.25, 255)
        return img
    return f


def pot(a, w, h):
    img = paint(CLAY, 0.5, 1.5)(a, w, h)
    H = img.shape[0]
    v = (np.arange(H) / a.K / h)[:, None, None]
    img = img * (1.05 - 0.25 * v)                                      # darker towards the foot
    a.rect(img, (0, h - 2, w, h), (120, 60, 36))
    return np.clip(img, 0, 255)


def soil_top(a, w, h):
    img = paint(CLAY, 0.4)(a, w, h)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    soil = d < 0.8
    r = np.random.default_rng(3)
    noise = r.uniform(0.75, 1.2, img.shape[:2])
    img[soil] = np.array(SOIL) * noise[soil][:, None]
    img[(d > 0.8) & (d < 0.84)] = (110, 56, 34)
    return img


m.swatch('leaves0', leaves(5))
m.swatch('leaves1', leaves(6))
m.swatch('pot', pot)
m.swatch('rim', lambda a, w, h: a.edge_dark(paint((190, 100, 62), 0.4)(a, w, h), 1.5, 0.75))
m.swatch('soil', paint(SOIL, 0.2, 1))
m.swatch('soiltop', soil_top)
m.swatch('clay', paint(CLAY, 0.4))
m.swatch('bark', wood(BARK))

if __name__ == '__main__':
    m.build()
