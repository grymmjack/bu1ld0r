#!/usr/bin/python3
"""c0-suit: a yellow hazmat suit standing - hood and gas mask with a green visor and filter, black
gloves and boots, a belt, seams and reflective tape. The game's is 0.13 x 0.29 x 0.04 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, rubber, glow  # noqa: E402

YEL, BLACK = (235, 200, 30), (26, 26, 28)
m = Model('suit', HERE, seed=133)
m.material('main', 'plastic')
for i, x in enumerate((0.021, -0.021)):
    m.box(f'boot-{i}', (x, 0, -0.002), (0.034, 0.03, 0.036), '1A1A1C', paint='rubber')
    m.box(f'leg-{i}', (x, 0.03, 0), (0.032, 0.095, 0.03), 'EBC81E', paint={'-z': 'legfront', '*': 'yellow'})
    m.box(f'arm-{i}', (x * 2.6, 0.12, 0), (0.022, 0.085, 0.026), 'EBC81E', paint='yellow')
    m.box(f'glove-{i}', (x * 2.6, 0.098, 0), (0.024, 0.024, 0.028), '1A1A1C', paint='rubber')
torso = m.box('torso', (0, 0.125, 0), (0.078, 0.095, 0.034), 'EBC81E')
m.box('belt', (0, 0.125, 0), (0.08, 0.012, 0.036), '1A1A1C', paint='rubber')
hood = m.box('hood', (0, 0.22, 0), (0.052, 0.068, 0.036), 'EBC81E')
m.box('filter', (0, 0.226, -0.024), (0.022, 0.022, 0.012), '1A1A1C', paint='rubber')


def suit_plain(a, w, h):
    img = paint(YEL, 0.4, 1.2)(a, w, h)
    for k in range(3):                                                 # creases
        y = h * (0.25 + k * 0.25)
        a.rect(img, (w * 0.1, y, w * 0.9, y + 0.4), (190, 150, 20), 0.6)
    return img


def chest(a, w, h):
    img = suit_plain(a, w, h)
    a.rect(img, (w * 0.48, h * 0.1, w * 0.52, h), (180, 150, 20))      # the zip
    a.rect(img, (0, h * 0.3, w, h * 0.36), (200, 210, 220))            # reflective tape
    a.rect(img, (w * 0.6, h * 0.45, w * 0.85, h * 0.6), (30, 30, 30))   # a radiation badge
    a.rect(img, (w * 0.65, h * 0.48, w * 0.8, h * 0.57), (235, 200, 30))
    return img


def mask(a, w, h):
    img = suit_plain(a, w, h)
    a.rect(img, (w * 0.12, h * 0.2, w * 0.88, h * 0.72), (30, 30, 32))
    a.rect(img, (w * 0.18, h * 0.26, w * 0.82, h * 0.5), (60, 200, 90))
    a.rect(img, (w * 0.22, h * 0.28, w * 0.45, h * 0.36), (180, 255, 190))
    return glow(img, a, (w * 0.18, h * 0.26, w * 0.82, h * 0.5), (60, 200, 90), 0.12, 1)


def leg_front(a, w, h):
    img = suit_plain(a, w, h)
    a.rect(img, (0, h * 0.55, w, h * 0.62), (200, 210, 220))
    return img


torso.paint = {'-z': chest, '*': 'yellow'}
hood.paint = {'-z': mask, '*': 'yellow'}
m.swatch('yellow', suit_plain)
m.swatch('rubber', rubber(BLACK))
m.swatch('legfront', leg_front)

if __name__ == '__main__':
    m.build()
