#!/usr/bin/python3
"""c0-lamp: a retro floor lamp - a pink-red base disc and pole, a cyan neck and holder, a cyan
drum shade lit warm from inside (seen from below), two pull chains. The game's is 0.19 x 0.85
x 0.19 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow  # noqa: E402

RED, CYAN, WARM = (214, 60, 80), (40, 200, 220), (255, 230, 170)
m = Model('lamp', HERE, seed=87)
m.material('main', 'plastic')
m.cyl('base', (0, 0, 0), (0.19, 0.022, 0.19), 'D63C50', seg=12, paint={'side': 'rim', 'top': 'basetop', 'bottom': 'dark'})
m.cyl('pole', (0, 0.022, 0), (0.03, 0.56, 0.03), 'D63C50', seg=8, paint={'side': 'pole', 'top': 'red', 'bottom': 'red'})
m.cyl('collar', (0, 0.582, 0), (0.05, 0.02, 0.05), 'E05868', seg=8, paint={'side': 'red', 'top': 'red', 'bottom': 'red'})
m.cyl('neck', (0, 0.602, 0), (0.034, 0.06, 0.034), '28C8DC', seg=8, paint={'side': 'cyanglass', 'top': 'cyan', 'bottom': 'cyan'})
m.cyl('holder', (0, 0.662, 0), (0.055, 0.03, 0.055), 'E05868', seg=8, paint={'side': 'red', 'top': 'red', 'bottom': 'red'})
m.cyl('shade', (0, 0.692, 0), (0.193, 0.158, 0.193), '28C8DC', seg=12, paint={'side': 'shade', 'top': 'cyan', 'bottom': 'lit'})
for i, x in enumerate((0.05, -0.05)):
    m.box(f'chain-{i}', (x, 0.63, 0), (0.005, 0.062, 0.005), 'C0C4CA', paint='steel')
    m.box(f'pull-{i}', (x, 0.62, 0), (0.012, 0.012, 0.012), 'E05868', paint='red')


def pole(a, w, h):
    img = paint(RED, 0.3, 1)(a, w, h)
    for k in range(8):                                                 # a highlight down each facet
        x = (k + 0.3) * w / 8
        a.rect(img, (x, 0, x + w / 32, h), (255, 170, 170), 0.35)
    return img


def shade(a, w, h):
    img = paint(CYAN, 0.2, 1)(a, w, h)
    H, W = img.shape[:2]
    v = (np.arange(H) / a.K / h)[:, None, None]
    img = img * (0.8 + 0.4 * v)                                        # lit from inside: brighter at the bottom
    for y in (1.2, h - 1.2):
        a.rect(img, (0, y - 0.6, w, y + 0.6), (20, 120, 140))
    for k in range(0, int(w), 3):                                      # fabric weave
        a.rect(img, (k, 0, k + 0.4, h), (20, 150, 170), 0.25)
    return np.clip(img, 0, 255)


def lit(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((60, 160, 170), np.float32)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    t = np.clip(1 - d, 0, 1)[..., None]
    img = img * (1 - t) + np.array(WARM) * t
    img[d < 0.18] = (255, 250, 230)
    return img


def base_top(a, w, h):
    img = paint(RED, 0.3, 1)(a, w, h)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    img[(d > 0.82) & (d < 0.9)] = (120, 24, 40)
    return img


m.swatch('rim', paint('3A1C24', 0.3))
m.swatch('basetop', base_top)
m.swatch('dark', paint('2A1A1E', 0.3))
m.swatch('pole', pole)
m.swatch('red', paint((224, 88, 104), 0.3, 1))
m.swatch('cyan', paint(CYAN, 0.2, 1))
m.swatch('cyanglass', lambda a, w, h: glow(paint(CYAN, 0.1, 1)(a, w, h), a, (0, 0, w, h), (150, 250, 255), 0.25, 1))
m.swatch('shade', shade)
m.swatch('lit', lit)
m.swatch('steel', steel())

if __name__ == '__main__':
    m.build()
