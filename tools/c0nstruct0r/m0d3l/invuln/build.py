#!/usr/bin/python3
"""c0-invuln: a gold medallion standing on edge - a bronze rim, a white star crest on top, a raised
gold shield with an orange-glowing emblem in front. The game's is 0.25 x 0.27 x 0.05 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import steel, glow  # noqa: E402

GOLD, BRONZE, ORANGE = (230, 180, 70), (150, 100, 50), (255, 150, 40)
m = Model('invuln', HERE, seed=129)
m.material('main', 'steel')
rim = m.cyl('rim', (0, 0.124, -0.012), (0.248, 0.024, 0.248), '966432', seg=16, rot=(90, 0, 0))
disc = m.cyl('disc', (0, 0.124, -0.02), (0.19, 0.008, 0.19), 'E6B446', seg=16, rot=(90, 0, 0))
shield = m.box('shield', (0, 0.07, -0.032), (0.1, 0.11, 0.012), 'E6B446')
m.box('crest', (0, 0.244, -0.006), (0.03, 0.026, 0.02), 'F0F0F0', paint='crest')


def gold(rgb):
    def f(a, w, h):
        return a.edge_dark(steel(rgb)(a, w, h), 1, 0.7)
    return f


def disc_front(a, w, h):
    img = gold(GOLD)(a, w, h)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    img[np.abs(d - 0.85) < 0.03] = (170, 120, 50)
    ang = np.arctan2(yy - h / 2, xx - w / 2)
    rays = (np.abs(((ang / (2 * np.pi) * 16) % 1) - 0.5) < 0.12) & (d < 0.8)
    img[rays] = img[rays] * 1.12
    return np.clip(img, 0, 255)


def shield_front(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((40, 30, 20), np.float32)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    u, v = (xx - w / 2) / (w / 2), yy / h
    outline = (np.abs(u) < np.where(v < 0.55, 0.95, 0.95 * (1 - (v - 0.55) / 0.45) ** 0.7)) & (v > 0.02)
    img[outline] = GOLD
    inner = (np.abs(u) < np.where(v < 0.55, 0.75, 0.75 * (1 - (v - 0.55) / 0.42) ** 0.7)) & (v > 0.1) & (v < 0.93)
    img[inner] = ORANGE
    img[inner & (u < 0)] = (255, 190, 80)
    img[inner & (np.abs(u) < 0.06)] = (255, 230, 160)
    return glow(img, a, (w * 0.15, h * 0.1, w * 0.85, h * 0.9), ORANGE, 0.15, 1)


rim.paint = {'*': 'bronze'}
disc.paint = {'-z': disc_front, '*': 'gold'}
shield.paint = {'-z': shield_front, '*': 'gold'}
m.swatch('bronze', gold(BRONZE))
m.swatch('gold', gold(GOLD))
m.swatch('crest', lambda a, w, h: steel((240, 240, 240))(a, w, h))

if __name__ == '__main__':
    m.build()
