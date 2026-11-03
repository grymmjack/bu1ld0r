#!/usr/bin/python3
"""c0-amp: the damage amp - a round red flask with a cyan lightning bolt on its front, glowing
studs, a steel neck and a dark cap with a red glowing top. The game's is 0.12 x 0.27 x 0.12 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow  # noqa: E402

RED, CYAN = (210, 30, 36), (80, 220, 255)
m = Model('amp', HERE, seed=125)
m.material('main', 'plastic')
m.cyl('flask', (0, 0, 0), (0.119, 0.16, 0.119), 'D21E24', seg=12, kind='sphere', paint={'side': 'flask', 'top': 'flask', 'bottom': 'flask'})
m.cyl('neck', (0, 0.15, 0), (0.05, 0.06, 0.05), 'B0B6BE', seg=12, paint={'side': 'steel', 'top': 'steel', 'bottom': 'steel'})
m.cyl('cap', (0, 0.21, 0), (0.068, 0.06, 0.068), '2A2D32', seg=12, paint={'side': 'capside', 'top': 'captop', 'bottom': 'dark'})


def flask(a, w, h):
    img = paint(RED, 0.2, 1)(a, w, h)
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W] / a.K
    v = yy / h
    img = img * (1.1 - 0.35 * v[..., None])                            # lit from above
    u = np.minimum(xx, w - xx) * np.where(xx < w / 2, 1, -1)           # signed, 0 = the front
    col = w / 12
    # the bolt: three slanted strokes zig-zagging down within a column and a half of the front
    bolt = np.zeros(img.shape[:2], bool)
    for (u0, v0, u1, v1) in ((0.7, 0.18, -0.3, 0.5), (-0.3, 0.5, 0.35, 0.5), (0.35, 0.5, -0.6, 0.85)):
        t = np.clip(((u / col - u0) * (u1 - u0) + (v - v0) * 10 * (v1 - v0) * 10) /
                    ((u1 - u0) ** 2 + (10 * (v1 - v0)) ** 2), 0, 1)
        du, dv = u / col - (u0 + t * (u1 - u0)), (v - (v0 + t * (v1 - v0))) * 10
        bolt |= np.hypot(du, dv) < 0.22
    img[bolt] = CYAN
    edge = np.zeros_like(bolt)
    edge[1:, :] |= bolt[:-1, :] & ~bolt[1:, :]
    img[edge] = (230, 250, 255)
    for k in range(12):                                                # studs round the middle
        if k in (0, 11):
            continue
        cx = (k + 0.5) * col
        a.rect(img, (cx - 1, h * 0.5 - 1, cx + 1, h * 0.5 + 1), CYAN)
    img = glow(np.clip(img, 0, 255).astype(np.float32), a, (0, h * 0.15, col * 1.5, h * 0.9), CYAN, 0.15, 1)
    return glow(img, a, (w - col * 1.5, h * 0.15, w, h * 0.9), CYAN, 0.15, 1)


def cap_top(a, w, h):
    img = paint('2A2D32', 0.2)(a, w, h)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    img[d < 0.7] = (255, 60, 60)
    img[d < 0.4] = (40, 40, 44)
    return img


def cap_side(a, w, h):
    img = paint('2A2D32', 0.3)(a, w, h)
    a.rect(img, (0, h * 0.1, w, h * 0.3), (230, 50, 50))
    return img


m.swatch('flask', flask)
m.swatch('steel', steel((176, 182, 190)))
m.swatch('dark', paint('2A2D32', 0.2))
m.swatch('captop', cap_top)
m.swatch('capside', cap_side)

if __name__ == '__main__':
    m.build()
