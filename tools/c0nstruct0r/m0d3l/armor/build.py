#!/usr/bin/python3
"""c0-armor: a suit of power armour standing - blue plates with red trim, a glowing orange chest
core, shoulder pads, a visored helmet, red boots. The game's is 0.15 x 0.27 x 0.05 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, glow  # noqa: E402

BLUE, RED, ORANGE = (60, 110, 190), (190, 50, 40), (255, 150, 40)
m = Model('armor', HERE, seed=123)
m.material('main', 'paint')
for i, x in enumerate((0.026, -0.026)):
    m.box(f'boot-{i}', (x, 0, -0.003), (0.04, 0.03, 0.05), 'BE3228', paint='red')
    m.box(f'leg-{i}', (x, 0.03, 0), (0.034, 0.075, 0.036), '3C6EBE', paint={'-z': 'legfront', '*': 'blue'})
    m.box(f'arm-{i}', (x * 2.45, 0.105, 0), (0.026, 0.085, 0.032), '3C6EBE', paint={'*': 'blue'})
    m.box(f'glove-{i}', (x * 2.45, 0.088, 0), (0.028, 0.02, 0.032), 'BE3228', paint='red')
    m.box(f'pad-{i}', (x * 2.2, 0.18, 0), (0.042, 0.032, 0.046), '3C6EBE', paint={'+y': 'padtop', '*': 'pad'})
m.box('hips', (0, 0.1, 0), (0.084, 0.03, 0.04), '2A2E36', paint='dark')
torso = m.box('torso', (0, 0.13, 0), (0.09, 0.075, 0.048), '3C6EBE')
m.box('collar', (0, 0.205, 0), (0.05, 0.014, 0.038), '2A2E36', paint='dark')
helm = m.box('helmet', (0, 0.219, 0), (0.044, 0.05, 0.046), '3C6EBE')


def plate(rgb, lines=True):
    def f(a, w, h):
        img = paint(rgb, 0.5, 1.5)(a, w, h)
        if lines:
            a.rect(img, (0, h * 0.5, w, h * 0.5 + 0.5), tuple(int(v * 0.55) for v in rgb))
        return img
    return f


def chest(a, w, h):
    img = plate(BLUE, False)(a, w, h)
    a.rect(img, (w * 0.47, 0, w * 0.53, h), (40, 70, 130))
    a.rect(img, (0, h * 0.8, w, h), RED)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h * 0.38)
    img[d < h * 0.17] = (60, 64, 70)
    img[d < h * 0.12] = ORANGE
    img[d < h * 0.06] = (255, 230, 160)
    return glow(img, a, (w * 0.35, h * 0.22, w * 0.65, h * 0.54), ORANGE, 0.2, 1)


def visor(a, w, h):
    img = plate(BLUE, False)(a, w, h)
    a.rect(img, (w * 0.12, h * 0.3, w * 0.88, h * 0.55), (30, 30, 36))
    a.rect(img, (w * 0.16, h * 0.36, w * 0.84, h * 0.48), (90, 220, 255))
    a.rect(img, (w * 0.4, h * 0.65, w * 0.6, h * 0.9), (40, 70, 130))
    return glow(img, a, (w * 0.16, h * 0.36, w * 0.84, h * 0.48), (90, 220, 255), 0.18, 1)


def leg_front(a, w, h):
    img = plate(BLUE)(a, w, h)
    a.rect(img, (w * 0.2, h * 0.35, w * 0.8, h * 0.55), (40, 70, 130))   # knee guard
    return img


def pad(a, w, h):
    img = plate(BLUE, False)(a, w, h)
    a.rect(img, (0, h * 0.7, w, h), RED)
    return img


torso.paint = {'-z': chest, '+z': 'back', '*': 'blue'}
helm.paint = {'-z': visor, '*': 'blue'}
m.swatch('blue', plate(BLUE))
m.swatch('red', plate(RED, False))
m.swatch('dark', paint('2A2E36', 0.4))
m.swatch('legfront', leg_front)
m.swatch('pad', pad)
m.swatch('padtop', plate(BLUE, False))
m.swatch('back', plate((50, 92, 160)))

if __name__ == '__main__':
    m.build()
