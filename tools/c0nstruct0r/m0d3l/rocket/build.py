#!/usr/bin/python3
"""c0-rocket: a rocket in flight (yours and a missile turret's) - centred on (0, 0, 0), its nose
towards -z as the game's: a grey tube with an orange band, a red nose cone, four dark fins, a nozzle
glowing orange. The game's is 0.12 x 0.12 x 0.38 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow  # noqa: E402

GREY, ORANGE, RED = (150, 154, 165), (255, 140, 30), (225, 40, 40)
m = Model('rocket', HERE, seed=121)
m.material('main', 'paint')
body = m.cyl('body', (0, 0, -0.1), (0.064, 0.25, 0.064), '969AA5', seg=10, rot=(90, 0, 0))
nose = m.cyl('nose', (0, 0, -0.1), (0.064, 0.1, 0.064), 'E12828', seg=10, amt=0.08, kind='cone', rot=(-90, 0, 0))
noz = m.cyl('nozzle', (0, 0, 0.15), (0.05, 0.03, 0.05), '1E1C1E', seg=10, rot=(90, 0, 0))
m.box('fin-v', (0, -0.058, 0.125), (0.006, 0.116, 0.07), '3C3E48', paint='fin')
m.box('fin-h', (0, -0.003, 0.125), (0.116, 0.006, 0.07), '3C3E48', paint='fin')


def body_x(a, w, h):                                                   # seen from the side: z across
    img = paint(GREY, 0.3)(a, w, h)
    a.rect(img, (w * 0.42, 0, w * 0.56, h), ORANGE)
    for u in (0.12, 0.88):
        a.rect(img, (w * u, 0, w * u + 0.6, h), (110, 112, 122))
    return img


def body_y(a, w, h):                                                   # seen from above: z down the picture
    img = paint(GREY, 0.3)(a, w, h)
    a.rect(img, (0, h * 0.42, w, h * 0.56), ORANGE)
    for v in (0.12, 0.88):
        a.rect(img, (0, h * v, w, h * v + 0.6), (110, 112, 122))
    return img


def flame(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((30, 28, 30), np.float32)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    img[d < 0.8] = ORANGE
    img[d < 0.45] = (255, 230, 150)
    return img


body.paint = {'+x': body_x, '-x': body_x, '+y': body_y, '-y': body_y, '*': 'grey'}
nose.paint = {'*': 'red'}
noz.paint = {'+z': flame, '*': 'dark'}
m.swatch('grey', paint(GREY, 0.3))
m.swatch('red', paint(RED, 0.2, 1))
m.swatch('dark', paint('1E1C1E', 0.2))
m.swatch('fin', lambda a, w, h: a.edge_dark(paint((60, 62, 72), 0.3)(a, w, h), 0.8, 0.7))

if __name__ == '__main__':
    m.build()
