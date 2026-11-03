#!/usr/bin/python3
"""c0-pickup-rocket: the rocket launcher lying in wait - a fat grey tube banded orange and black,
its muzzle a magenta ring round a glowing orange core (to +x), a glowing magenta back cap, twin
tubes and a sight on top, a dark mount with orange trim, a grip and two wheels. The game's is
0.44 x 0.38 x 0.11 cells (the tube a little deeper here: 0.13)."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, rubber, glow  # noqa: E402

GREY, ORANGE, MAG, CORE = (120, 124, 134), (240, 120, 30), (220, 60, 210), (255, 170, 40)
m = Model('pickup-rocket', HERE, seed=155)
m.material('main', 'paint')
tube = m.cyl('tube', (-0.17, 0.2, 0), (0.17, 0.33, 0.125), '787C86', seg=16, rot=(0, 0, -90))
ring = m.cyl('muzzle', (0.16, 0.2, 0), (0.2, 0.05, 0.135), 'DC3CD2', seg=16, rot=(0, 0, -90))
cap = m.cyl('backcap', (-0.2, 0.2, 0), (0.12, 0.03, 0.09), 'DC3CD2', seg=12, rot=(0, 0, -90))
for i, z in enumerate((-0.026, 0.026)):
    t = m.cyl(f'top-{i}', (-0.13, 0.315, z), (0.05, 0.2, 0.05), '505460', seg=8, rot=(0, 0, -90))
    t.paint = {'+x': 'bore', '-x': 'dark', '*': 'darkgrey'}
m.box('sight', (-0.05, 0.338, 0), (0.05, 0.043, 0.02), '303238', paint={'+x': 'lens', '*': 'dark'})
mount = m.box('mount', (-0.01, 0.07, 0), (0.2, 0.06, 0.08), '34363C')
m.box('grip', (-0.06, 0.02, 0), (0.035, 0.06, 0.04), '222428', paint='dark')
for i, x in enumerate((-0.085, 0.07)):
    w = m.cyl(f'wheel-{i}', (x, 0.03, -0.04), (0.06, 0.08, 0.06), '1C1C1E', seg=10, rot=(90, 0, 0))
    w.paint = {'-z': 'hub', '+z': 'hub', '*': 'rubber'}


def bands(a, w, h, flip):
    """The tube's side: grey, an orange band with black bars, a red stripe low down."""
    img = paint(GREY, 0.4)(a, w, h)
    a.rect(img, (w * 0.18, 0, w * 0.82, h), ORANGE)
    for k in range(5):
        u = w * (0.26 + k * 0.11)
        a.rect(img, (u, h * 0.15, u + w * 0.05, h * 0.85), (30, 30, 34))
    a.rect(img, (0, h * 0.86 if not flip else 0, w, h * 0.92 if not flip else h * 0.06), (200, 40, 40))
    for u in (0.18, 0.82):
        a.rect(img, (w * u, 0, w * u + 0.8, h), (90, 92, 100))
    return img


def tube_y(a, w, h):                       # from above / below: x across, z down
    img = paint(GREY, 0.4)(a, w, h)
    a.rect(img, (w * 0.18, 0, w * 0.82, h), ORANGE)
    for k in range(5):
        u = w * (0.26 + k * 0.11)
        a.rect(img, (u, 0, u + w * 0.05, h), (30, 30, 34))
    return img


def core(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array(MAG, np.float32)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2))
    img[d < 0.82] = (90, 30, 20)
    img[d < 0.72] = CORE
    img[d < 0.4] = (255, 236, 150)
    return glow(img, a, (w * 0.1, h * 0.1, w * 0.9, h * 0.9), CORE, 0.2, 2)


def magglow(a, w, h):
    img = paint(MAG, 0.15, 1)(a, w, h)
    return glow(img, a, (0, 0, w, h), (255, 140, 250), 0.15, 1)


def mount_side(a, w, h):
    img = paint((52, 54, 60), 0.4)(a, w, h)
    a.rect(img, (0, h * 0.8, w, h * 0.92), ORANGE)                    # orange trim
    a.rect(img, (w * 0.1, h * 0.2, w * 0.9, h * 0.25), (30, 30, 34))
    a.rect(img, (w * 0.42, h * 0.38, w * 0.58, h * 0.62), MAG)          # a magenta light
    return glow(img, a, (w * 0.42, h * 0.38, w * 0.58, h * 0.62), MAG, 0.2, 1)


def lens(a, w, h):
    img = paint('303238', 0.2)(a, w, h)
    a.rect(img, (w * 0.2, h * 0.2, w * 0.8, h * 0.8), (255, 120, 240))
    return glow(img, a, (w * 0.2, h * 0.2, w * 0.8, h * 0.8), (255, 120, 240), 0.2, 1)


def hub(a, w, h):
    img = rubber((28, 28, 30))(a, w, h)
    a.rect(img, (w * 0.3, h * 0.3, w * 0.7, h * 0.7), (130, 134, 142))
    return img


tube.paint = {'-z': lambda a, w, h: bands(a, w, h, 0), '+z': lambda a, w, h: bands(a, w, h, 0),
              '+y': tube_y, '-y': tube_y, '*': 'grey'}
ring.paint = {'+x': core, '*': 'mag'}
cap.paint = {'-x': magglow, '*': 'mag'}
mount.paint = {'-z': mount_side, '+z': mount_side, '*': 'dark'}
m.swatch('grey', paint(GREY, 0.4))
m.swatch('mag', paint(MAG, 0.3))
m.swatch('dark', paint('303238', 0.3))
m.swatch('darkgrey', paint((80, 84, 96), 0.3))
m.swatch('bore', lambda a, w, h: a.edge_dark(paint((12, 12, 14), 0.1)(a, w, h), 1.5, 0.3))
m.swatch('lens', lens)
m.swatch('hub', hub)
m.swatch('rubber', rubber((28, 28, 30)))

if __name__ == '__main__':
    m.build()
