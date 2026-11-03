#!/usr/bin/python3
"""c0-safe: a heavy charcoal safe on a plinth - armoured corner posts, a sunk door with a glowing
cyan ring lock, status lights, a strip light over it, a deposit drawer under it. The game's is
0.44 x 0.48 x 0.37 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow, front_box  # noqa: E402

BODY, POST, CYAN, GREEN = '2C3036', '1C1F23', (60, 230, 220), (90, 240, 120)


def door(a, img, s, seed=3):
    """The sunk door: plates, a ring lock in the middle, a light column, a vent."""
    x0, y0, x1, y1 = s
    w, h = x1 - x0, y1 - y0
    a.rect(img, s, (40, 44, 50))
    for k, (u0, u1) in enumerate(((0.04, 0.3), (0.7, 0.96))):           # side plates
        a.rect(img, (x0 + w * u0, y0 + h * 0.06, x0 + w * u1, y1 - h * 0.06), (34, 38, 43))
        a.rect(img, (x0 + w * u0, y0 + h * 0.06, x0 + w * u1, y0 + h * 0.06 + 0.6), (70, 76, 84))
    for k in range(7):                                                 # vent slots, left
        yy = y0 + h * (0.16 + k * 0.07)
        a.rect(img, (x0 + w * 0.08, yy, x0 + w * 0.26, yy + h * 0.03), (16, 18, 21))
    for k in range(6):                                                 # status lights, right
        yy = y0 + h * (0.18 + k * 0.1)
        c = GREEN if k < 4 else (255, 170, 40)
        a.rect(img, (x0 + w * 0.8, yy, x0 + w * 0.9, yy + h * 0.035), c)
        img = glow(img, a, (x0 + w * 0.8, yy, x0 + w * 0.9, yy + h * 0.035), c, 0.15, 1)
    cx, cy, r = x0 + w * 0.5, y0 + h * 0.42, min(w, h) * 0.2
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - cx, yy - cy)
    img[d < r * 1.15] = (22, 26, 30)
    ring = (d > r * 0.82) & (d < r)
    img[ring] = CYAN
    img[d < r * 0.5] = (52, 58, 64)
    img[d < r * 0.12] = (200, 206, 212)
    img = glow(img, a, (cx - r, cy - r, cx + r, cy + r), CYAN, 0.2, 2)
    for t in np.linspace(0, 2 * np.pi, 12, endpoint=False):           # the dial's ticks
        a.rect(img, (cx + np.cos(t) * r * 0.66 - 0.4, cy + np.sin(t) * r * 0.66 - 0.4,
                     cx + np.cos(t) * r * 0.66 + 0.4, cy + np.sin(t) * r * 0.66 + 0.4), (180, 190, 196))
    a.rect(img, (x0 + w * 0.36, y0 + h * 0.72, x0 + w * 0.64, y0 + h * 0.8), (20, 22, 25))  # keypad
    for i in range(3):
        for j in range(2):
            a.rect(img, (x0 + w * (0.38 + i * 0.09), y0 + h * (0.733 + j * 0.033),
                         x0 + w * (0.44 + i * 0.09), y0 + h * (0.755 + j * 0.033)), (90, 200, 200))
    return img


def make(name, seed, opened=False):
    m = Model(name, HERE if not opened else os.path.join(HERE, '..', 'safe-open'), seed=seed)
    m.material('main', 'paint')
    m.box('plinth', (0, 0, 0), (0.42, 0.03, 0.35), '15171A', paint='plinth')
    body = m.box('body', (0, 0.03, 0.005), (0.40, 0.44, 0.362), BODY, walls='inner' if not opened else 'cave')
    for i, x in enumerate((0.204, -0.204)):
        m.box(f'post-{i}', (x, 0.03, -0.004), (0.03, 0.451, 0.376), POST, paint={'-z': 'postfront', '+x': 'flank', '-x': 'flank', '*': 'post'})
    m.box('cap', (0, 0.47, 0.005), (0.438, 0.011, 0.362), POST, paint='post')
    return m, body


m, body = make('safe', 61)
body.cut('-z', (-0.16, 0.16, 0.13, 0.43), 0.02)
drawer = m.box('drawer', (0, 0.045, -0.186), (0.30, 0.07, 0.02), '24272C')


def front(a, w, h):
    img = paint(BODY, 0.5)(a, w, h)
    s = front_box(body, w, h, -0.16, 0.16, 0.13, 0.43)
    img = door(a, img, s)
    a.rect(img, (s[0], s[1] - 3, s[2], s[1] - 1.8), CYAN)            # the strip light
    return glow(img, a, (s[0], s[1] - 3, s[2], s[1] - 1.8), CYAN, 0.2, 2)


def drawer_front(a, w, h):
    img = paint('24272C', 0.4)(a, w, h)
    a.rect(img, (w * 0.06, h * 0.2, w * 0.94, h * 0.8), (30, 33, 38))
    a.rect(img, (w * 0.4, h * 0.4, w * 0.6, h * 0.6), (170, 176, 184))  # pull
    a.rect(img, (w * 0.47, h * 0.25, w * 0.53, h * 0.32), CYAN)
    return glow(img, a, (w * 0.47, h * 0.25, w * 0.53, h * 0.32), CYAN, 0.2, 1)


def post_front(a, w, h):
    img = paint(POST, 0.5)(a, w, h)
    for k in range(6):                                                 # bolts
        y = h * (0.06 + k * 0.176)
        a.rect(img, (w * 0.3, y, w * 0.7, y + w * 0.4), (120, 126, 134))
    return img


body.paint = {'-z': front, '+z': 'back', '*': 'side'}
drawer.paint = {'-z': drawer_front, '*': 'side'}
m.swatch('side', paint(BODY, 0.5))
def back(a, w, h):
    img = paint(BODY, 0.5)(a, w, h)
    for k in range(1, 4):
        a.rect(img, (0, h * k / 4, w, h * k / 4 + 0.8), (20, 22, 25))
    a.rect(img, (w * 0.35, h * 0.08, w * 0.65, h * 0.16), (20, 22, 25))      # cable port
    return img


m.swatch('back', back)
m.swatch('inner', paint('22252A', 0.3, 1))
m.swatch('post', paint(POST, 0.5))
m.swatch('postfront', post_front)


def flank(a, w, h):
    img = paint(POST, 0.5)(a, w, h)
    a.rect(img, (w * 0.08, h * 0.08, w * 0.92, h * 0.92), (40, 44, 50))      # an armour plate
    a.rect(img, (w * 0.08, h * 0.08, w * 0.92, h * 0.08 + 0.7), (74, 80, 88))
    a.rect(img, (w * 0.08, h * 0.92 - 0.7, w * 0.92, h * 0.92), (14, 15, 17))
    for u in (0.13, 0.87):
        for v in (0.13, 0.5, 0.87):
            a.rect(img, (w * u - 1, h * v - 1, w * u + 1, h * v + 1), (120, 126, 134))
    for k in range(3):                                                 # ribs
        y = h * (0.3 + k * 0.2)
        a.rect(img, (w * 0.2, y, w * 0.8, y + 1.2), (26, 29, 33))
    img = a.text(img, 'VAULT 7', h * 0.07, (w * 0.25, h * 0.14, w * 0.75, h * 0.24), (200, 180, 60), alpha=0.75)
    a.rect(img, (w * 0.25, h * 0.8, w * 0.75, h * 0.84), (200, 180, 60), 0.6)
    return img


m.swatch('flank', flank)
m.swatch('plinth', paint('15171A', 0.3))

if __name__ == '__main__':
    m.build()
