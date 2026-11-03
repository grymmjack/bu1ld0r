#!/usr/bin/python3
"""c0-repairkit: an open tool case - a dark case with steel corners and latches, its well full of
tools (wrench, screwdrivers, a meter glowing cyan), the lid standing open behind with tools held in
its foam and a cyan diagnostic strip. The game's is 0.25 x 0.25 x 0.11 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow, front_box  # noqa: E402

CASE, CYAN = '2A2D32', (60, 220, 240)
m = Model('repairkit', HERE, seed=143)
m.material('main', 'paint')
base = m.box('base', (0, 0, 0.0), (0.25, 0.07, 0.1), CASE, walls='foam')
base.cut('+y', (-0.115, 0.115, -0.04, 0.04), 0.05)
tools = m.box('tools', (0, 0.035, 0.0), (0.228, 0.012, 0.078), '404448', paint={'+y': 'tooltray', '*': 'foam'})
lid = m.box('lid', (0, 0.07, 0.042), (0.25, 0.175, 0.016), CASE)
for i, x in enumerate((0.07, -0.07)):
    m.box(f'latch-{i}', (x, 0.035, -0.054), (0.03, 0.03, 0.008), 'B0B6BE', paint='steel')


def foam_tools(a, w, h, seed):
    r = np.random.default_rng(seed)
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((40, 44, 50), np.float32)
    for k in range(int(w * h / 3)):
        x, y = r.uniform(0, w), r.uniform(0, h)
        a.rect(img, (x, y, x + 0.5, y + 0.5), (30, 33, 38))
    return img


def tray(a, w, h):
    img = foam_tools(a, w, h, 2)
    # a wrench, two screwdrivers, a meter
    a.rect(img, (w * 0.05, h * 0.4, w * 0.4, h * 0.55), (180, 186, 194))
    a.rect(img, (w * 0.02, h * 0.3, w * 0.08, h * 0.65), (180, 186, 194))
    a.rect(img, (w * 0.035, h * 0.42, w * 0.065, h * 0.53), (40, 44, 50))
    for k, c in enumerate(((220, 50, 40), (240, 190, 40))):
        y = h * (0.15 + k * 0.6)
        a.rect(img, (w * 0.45, y, w * 0.6, y + h * 0.15), c)
        a.rect(img, (w * 0.6, y + h * 0.05, w * 0.78, y + h * 0.1), (190, 196, 204))
    a.rect(img, (w * 0.8, h * 0.15, w * 0.96, h * 0.85), (240, 180, 30))
    a.rect(img, (w * 0.83, h * 0.22, w * 0.93, h * 0.45), (20, 40, 46))
    a.rect(img, (w * 0.84, h * 0.25, w * 0.92, h * 0.42), CYAN)
    return glow(img, a, (w * 0.83, h * 0.22, w * 0.93, h * 0.45), CYAN, 0.15, 1)


def lid_inside(a, w, h):
    img = foam_tools(a, w, h, 4)
    a.rect(img, (w * 0.06, h * 0.08, w * 0.94, h * 0.2), (20, 40, 46))     # diagnostic strip
    for k in range(10):
        x = w * (0.08 + k * 0.085)
        a.rect(img, (x, h * 0.1, x + w * 0.05, h * 0.18 - (k % 4) * h * 0.015), CYAN)
    img = glow(img, a, (w * 0.06, h * 0.08, w * 0.94, h * 0.2), CYAN, 0.15, 1)
    for k in range(6):                                                 # tools in loops
        x = w * (0.1 + k * 0.14)
        c = [(180, 186, 194), (220, 50, 40), (180, 186, 194), (240, 190, 40), (90, 200, 90), (180, 186, 194)][k]
        a.rect(img, (x, h * 0.3, x + w * 0.05, h * 0.85), c)
        a.rect(img, (x - w * 0.01, h * 0.55, x + w * 0.06, h * 0.6), (20, 22, 26))
    return img


def case_front(a, w, h):
    img = paint(CASE, 0.5)(a, w, h)
    for x in (2, w - 6):                                               # steel corners
        a.rect(img, (x, 0, x + 4, 4), (150, 156, 164))
        a.rect(img, (x, h - 4, x + 4, h), (150, 156, 164))
    a.rect(img, (w * 0.4, h * 0.4, w * 0.6, h * 0.6), (60, 64, 70))       # a badge
    a.rect(img, (w * 0.47, h * 0.43, w * 0.53, h * 0.57), (230, 60, 50))
    a.rect(img, (w * 0.43, h * 0.47, w * 0.57, h * 0.53), (230, 60, 50))
    return img


base.paint = {'-z': case_front, '+z': case_front, '*': 'case'}
lid.paint = {'-z': lid_inside, '*': 'case'}
m.swatch('case', paint(CASE, 0.5))
m.swatch('foam', paint('282B30', 0.2, 1))
m.swatch('tooltray', tray)
m.swatch('steel', steel((176, 182, 190)))

if __name__ == '__main__':
    m.build()
