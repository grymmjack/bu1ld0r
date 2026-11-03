#!/usr/bin/python3
"""c0-cryopod: a round cryo pod - a dark plinth with a cyan rim, a white panelled drum with a frosted
window glowing ice blue (a sleeper's shape inside), coolant pipes down both sides, a capped dome
top with a status light. The game's is 0.43 x 0.94 x 0.43 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow  # noqa: E402

WHITE, DARK, ICE = (214, 220, 228), '25292F', (110, 210, 255)
m = Model('cryopod', HERE, seed=81)
m.material('main', 'plastic')
m.cyl('plinth', (0, 0, 0), (0.425, 0.06, 0.425), DARK, seg=12, paint={'side': 'plinthside', 'top': 'plinthtop', 'bottom': 'dark'})
m.cyl('pod', (0, 0.06, 0), (0.38, 0.78, 0.38), 'D6DCE4', seg=12, paint={'side': 'podside', 'top': 'white', 'bottom': 'white'})
m.cyl('cap', (0, 0.84, 0), (0.40, 0.06, 0.40), 'C0C6CE', seg=12, paint={'side': 'capside', 'top': 'white', 'bottom': 'white'})
m.cyl('dome', (0, 0.9, 0), (0.30, 0.035, 0.30), 'C0C6CE', seg=12,
      paint={'side': 'white', 'top': 'domelight', 'bottom': 'white'})
for i, x in enumerate((0.198, -0.198)):
    m.box(f'pipe-{i}', (x, 0.14, 0), (0.03, 0.62, 0.05), '8A9098', paint='pipe')
    for j, y in enumerate((0.16, 0.7)):
        m.box(f'clamp-{i}-{j}', (x, y, 0), (0.04, 0.03, 0.06), '30343A', paint='dark')


def pod_side(a, w, h):
    img = paint(WHITE, 0.4, 1.5)(a, w, h)
    col = w / 12
    for k in range(13):                                                # panel seams at the column edges
        a.rect(img, (k * col - 0.4, 0, k * col + 0.4, h), (150, 156, 166))
    for y in (h * 0.06, h * 0.94):
        a.rect(img, (0, y - 0.5, w, y + 0.5), (130, 136, 146))
    win = col * 2.0                                                    # the window: 2 columns either side of the front
    yy0, yy1 = h * 0.12, h * 0.9
    for x0, x1, off in ((0, win, 0), (w - win, w, -w)):                # it wraps round u = 0
        a.rect(img, (x0, yy0 - 1.5, x1, yy1 + 1.5), (70, 80, 92))
        a.rect(img, (x0, yy0, x1, yy1), ICE)
        H, W = img.shape[:2]
        ys, xs = np.mgrid[0:H, 0:W] / a.K
        u = xs + off                                                   # u: across the window, 0 = front middle
        v = (ys - yy0) / (yy1 - yy0)
        inside = (xs >= x0) & (xs < x1) & (v >= 0) & (v <= 1)
        frost = 0.55 + 0.45 * np.clip(1 - np.abs(u) / win, 0, 1)
        img[inside] = img[inside] * frost[inside][:, None] + np.array((230, 245, 255)) * (1 - frost[inside][:, None]) * 0.6
        body = inside & (((u / (win * 0.28)) ** 2 + ((v - 0.13) / 0.07) ** 2 < 1) |
                         ((np.abs(u) < win * (0.42 - 0.12 * v)) & (v > 0.2) & (v < 0.95)))
        img[body] = img[body] * 0.72 + np.array((40, 90, 140)) * 0.28  # the sleeper, faint through the frost
        rr = np.random.default_rng(int(x0))
        for _ in range(int(win * 1.2)):                                # bubbles
            bx, by = rr.uniform(x0 + 1, x1 - 1), rr.uniform(yy0 + 2, yy1 - 2)
            a.rect(img, (bx, by, bx + 0.7, by + 0.7), (225, 245, 255), 0.7)
        for _ in range(5):                                             # frost streaks
            bx = rr.uniform(x0 + 1, x1 - 1)
            a.rect(img, (bx, yy0, bx + 0.5, yy1), (235, 248, 255), 0.35)
    img = glow(img, a, (0, yy0, win, yy1), ICE, 0.2, 2)
    img = glow(img, a, (w - win, yy0, w, yy1), ICE, 0.2, 2)
    for x in (w * 0.5 - col * 0.6, w * 0.5 + col * 0.2):               # a readout on the back
        a.rect(img, (x, h * 0.4, x + col * 0.4, h * 0.46), (40, 44, 50))
        a.rect(img, (x + 1, h * 0.41, x + col * 0.3, h * 0.43), (90, 240, 120))
    return img


def plinth_side(a, w, h):
    img = paint(DARK, 0.4)(a, w, h)
    a.rect(img, (0, h * 0.3, w, h * 0.5), ICE)
    return glow(img, a, (0, h * 0.3, w, h * 0.5), ICE, 0.2, 1)


def cap_side(a, w, h):
    img = paint((192, 198, 206), 0.4)(a, w, h)
    for k in range(13):
        a.rect(img, (k * w / 12 - 0.4, 0, k * w / 12 + 0.4, h), (140, 146, 156))
    a.rect(img, (0, h * 0.75, w, h), (60, 66, 74))
    return img


def dome_light(a, w, h):
    img = paint((192, 198, 206), 0.4)(a, w, h)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2)
    img[d < w * 0.25] = (60, 66, 74)
    img[d < w * 0.16] = ICE
    return glow(img, a, (w * 0.34, h * 0.34, w * 0.66, h * 0.66), ICE, 0.25, 2)


def pipe(a, w, h):
    img = steel((150, 160, 172))(a, w, h)
    for y in np.arange(4, h, 9):
        a.rect(img, (0, y, w, y + 0.8), (90, 96, 104))
    return img


m.swatch('podside', pod_side)
m.swatch('plinthside', plinth_side)
m.swatch('plinthtop', paint(DARK, 0.4))
m.swatch('dark', paint(DARK, 0.3))
m.swatch('white', paint(WHITE, 0.3, 1.5))
m.swatch('capside', cap_side)
m.swatch('domelight', dome_light)
m.swatch('pipe', pipe)

if __name__ == '__main__':
    m.build()
