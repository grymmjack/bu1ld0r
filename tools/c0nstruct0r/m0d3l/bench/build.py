#!/usr/bin/python3
"""c0-bench: a padded crew bench - red stitched leather slab with brass studs, dark legs, a grey
headrest pad, a red toolbox with a steel handle on it. The game's is 0.32 x 0.18 x 0.12 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, rubber  # noqa: E402

RED, DARK = (150, 28, 32), '26282C'
m = Model('bench', HERE, seed=37)
m.material('main', 'plastic')
for i, x in enumerate((0.12, -0.12)):
    m.box(f'leg-{i}', (x, 0, 0), (0.025, 0.09, 0.08), DARK, paint='leg')
slab = m.box('slab', (0, 0.09, 0), (0.315, 0.032, 0.115), '96201C')
m.box('pad', (0.075, 0.122, 0), (0.11, 0.016, 0.09), '6A6E74', paint='padgrey')
box = m.box('toolbox', (-0.075, 0.122, 0), (0.075, 0.046, 0.05), 'B01E1E')
for i, x in enumerate((-0.058, -0.092)):
    m.box(f'tb-post-{i}', (x, 0.168, 0), (0.006, 0.012, 0.008), 'A0A4AA', paint='steel')
m.box('tb-handle', (-0.075, 0.18, 0), (0.042, 0.006, 0.008), 'A0A4AA', paint='steel')


def leather(studs=False):
    def f(a, w, h):
        img = a.tinted(a.load(os.path.join(HERE, '..', 'medkit', 'red.png')), w, h, RED, 1.2)
        img = a.edge_dark(img, 2, 0.7)
        for t in np.arange(1.5, w - 1.5, 1.3):              # stitching
            a.rect(img, (t, 1.2, t + 0.6, 1.5), (200, 160, 150), 0.7)
            a.rect(img, (t, h - 1.5, t + 0.6, h - 1.2), (200, 160, 150), 0.7)
        if studs:
            for k in range(7):
                x = w * (0.08 + k * 0.14)
                a.rect(img, (x - 0.8, h * 0.45, x + 0.8, h * 0.45 + 1.6), (210, 170, 80))
                a.rect(img, (x - 0.4, h * 0.45 + 0.2, x + 0.1, h * 0.45 + 0.6), (255, 230, 160))
        return img
    return f


def toolbox_front(a, w, h):
    img = paint((176, 30, 30), 0.4)(a, w, h)
    a.rect(img, (0, h * 0.3, w, h * 0.34), (90, 14, 14))               # the lid's seam
    a.rect(img, (w * 0.4, h * 0.36, w * 0.6, h * 0.52), (200, 204, 210))  # name plate
    a.rect(img, (w * 0.08, h * 0.2, w * 0.16, h * 0.44), (190, 194, 200))  # latches
    a.rect(img, (w * 0.84, h * 0.2, w * 0.92, h * 0.44), (190, 194, 200))
    return img


slab.paint = {'+y': leather(), '-z': leather(True), '+z': leather(True), '*': 'leatherplain'}
box.paint = {'-z': toolbox_front, '+z': toolbox_front, '*': 'tbred'}
m.swatch('leatherplain', leather())
m.swatch('leg', paint(DARK, 0.4))
m.swatch('padgrey', rubber((96, 100, 106)))
m.swatch('tbred', paint((176, 30, 30), 0.4))
m.swatch('steel', steel())

if __name__ == '__main__':
    m.build()
