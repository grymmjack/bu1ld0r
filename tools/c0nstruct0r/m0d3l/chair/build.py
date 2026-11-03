#!/usr/bin/python3
"""c0-chair: an office chair - black leather seat and back (stitched cushions), armrests on posts,
a steel gas lift, a four-arm base on casters. The game's is 0.35 x 0.43 x 0.27 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, rubber  # noqa: E402

LEATHER = (34, 34, 38)
m = Model('chair', HERE, seed=29)
m.material('main', 'plastic')
m.box('base-x', (0, 0.03, 0), (0.30, 0.025, 0.035), '202024', paint='base')
m.box('base-z', (0, 0.031, 0), (0.033, 0.023, 0.26), '202024', paint='base')
for i, (x, z) in enumerate(((0.135, 0), (-0.135, 0), (0, 0.115), (0, -0.115))):
    m.box(f'caster-{i}', (x, 0, z), (0.03, 0.03, 0.03), '111114', paint='rubber')
m.cyl('column', (0, 0.055, 0), (0.035, 0.14, 0.035), 'A0A4AA', seg=8,
      paint={'side': 'steel', 'top': 'steel', 'bottom': 'steel'})
seat = m.box('seat', (0, 0.195, -0.005), (0.29, 0.055, 0.26), '222226')
seat.cut('+y', (-0.13, 0.13, -0.12, 0.11), -0.012)
back = m.box('back', (0, 0.25, 0.118), (0.26, 0.18, 0.045), '222226')
back.cut('-z', (-0.115, 0.115, 0.265, 0.415), -0.01)
for i, x in enumerate((0.158, -0.158)):
    m.box(f'arm-post-{i}', (x, 0.235, 0.0), (0.022, 0.08, 0.022), '202024', paint='base')
    m.box(f'arm-pad-{i}', (x, 0.315, 0.0), (0.036, 0.018, 0.15), '1A1A1E', paint='pad')


def leather(stitch=True, quilt=0):
    def f(a, w, h):
        img = a.tinted(a.load(os.path.join(HERE, '..', 'medkit', 'rubber.png'), (0, 120)), w, h, LEATHER, 1.6)
        img = a.edge_dark(img, 3, 0.7)
        if stitch:
            for t in np.arange(2, w - 2, 1.4):
                a.rect(img, (t, 1.6, t + 0.7, 1.9), (70, 70, 76))
                a.rect(img, (t, h - 1.9, t + 0.7, h - 1.6), (70, 70, 76))
        for q in range(1, quilt):
            y = h * q / quilt
            a.rect(img, (2, y - 0.4, w - 2, y + 0.4), (14, 14, 16))
            a.rect(img, (2, y + 0.4, w - 2, y + 0.9), (60, 60, 66), 0.6)
        return img
    return f


seat.paint = {'+y': leather(True, 3), '*': 'leatherplain'}
seat.walls = 'leatherplain'
back.paint = {'-z': leather(True, 4), '+z': 'backshell', '*': 'leatherplain'}
back.walls = 'leatherplain'
m.swatch('leatherplain', leather(False))
m.swatch('backshell', paint('1C1C20', 0.4))
m.swatch('base', paint('26262A', 0.5))
m.swatch('pad', leather(False))
m.swatch('rubber', rubber((30, 30, 32)))
m.swatch('steel', steel((190, 194, 200)))

if __name__ == '__main__':
    m.build()
