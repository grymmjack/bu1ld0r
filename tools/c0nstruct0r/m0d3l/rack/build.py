#!/usr/bin/python3
"""c0-rack: a server rack - grey cabinet on feet, a deep mesh window onto a wall of glowing fans
(cyan rings, yellow hubs), orange drive bays above, vents top and sides. The game's is 0.45 x 0.82
x 0.26 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, rubber, glow, front_box  # noqa: E402

GREY, CYAN, YELLOW, ORANGE = '5A6068', (60, 220, 255), (255, 220, 70), (255, 150, 40)
m = Model('rack', HERE, seed=47)
m.material('main', 'paint')
for i, (x, z) in enumerate(((0.18, 0.09), (-0.18, 0.09), (0.18, -0.09), (-0.18, -0.09))):
    m.box(f'foot-{i}', (x, 0, z), (0.045, 0.03, 0.045), '18181A', paint='rubber')
cab = m.box('cabinet', (0, 0.03, 0), (0.44, 0.785, 0.26), GREY, walls='inside')
cab.cut('-z', (-0.175, 0.175, 0.07, 0.64), 0.035)


def fans(a, img, s):
    x0, y0, x1, y1 = s
    a.rect(img, s, (14, 18, 24))
    cols, rows = 4, 6
    cw, ch = (x1 - x0) / cols, (y1 - y0) / rows
    r = np.random.default_rng(5)
    for i in range(rows):
        for j in range(cols):
            if r.random() < 0.12:
                continue                                    # a dead fan
            cx, cy = x0 + cw * (j + 0.5), y0 + ch * (i + 0.5)
            rad = min(cw, ch) * 0.38
            for t in np.linspace(0, 2 * np.pi, 48):
                a.rect(img, (cx + np.cos(t) * rad - 0.5, cy + np.sin(t) * rad - 0.5,
                             cx + np.cos(t) * rad + 0.5, cy + np.sin(t) * rad + 0.5), CYAN)
            hub = YELLOW if r.random() < 0.35 else CYAN
            a.rect(img, (cx - rad * 0.3, cy - rad * 0.3, cx + rad * 0.3, cy + rad * 0.3), hub)
            img = glow(img, a, (cx - rad, cy - rad, cx + rad, cy + rad), CYAN, 0.18, 2)
    for yy in np.arange(y0, y1, 1.2):                       # the door's mesh
        a.rect(img, (x0, yy, x1, yy + 0.3), (0, 0, 0), 0.35)
    for xx in np.arange(x0, x1, 1.2):
        a.rect(img, (xx, y0, xx + 0.3, y1), (0, 0, 0), 0.35)
    return img


def front(a, w, h):
    img = paint(GREY)(a, w, h)
    s = front_box(cab, w, h, -0.175, 0.175, 0.07, 0.64)
    a.rect(img, (s[0] - 2, s[1] - 2, s[2] + 2, s[3] + 2), (40, 44, 50))
    img = fans(a, img, s)
    by = h * 0.075
    for k in range(4):                                      # the drive bays
        bx = w * (0.1 + k * 0.205)
        a.rect(img, (bx, by, bx + w * 0.18, by + h * 0.045), ORANGE)
        a.rect(img, (bx + w * 0.02, by + h * 0.015, bx + w * 0.16, by + h * 0.028), (120, 60, 10))
    for k in range(5):                                      # top vents
        a.rect(img, (w * 0.12, h * 0.01 + k * h * 0.011, w * 0.88, h * 0.016 + k * h * 0.011), (34, 36, 40))
    a.rect(img, (s[2] + 1, (s[1] + s[3]) / 2 - 6, s[2] + 2.5, (s[1] + s[3]) / 2 + 6), (190, 194, 200))  # handle
    return img


def side(a, w, h):
    img = paint(GREY)(a, w, h)
    for k in range(30):
        y = h * 0.1 + k * h * 0.027
        a.rect(img, (w * 0.2, y, w * 0.8, y + h * 0.012), (34, 36, 40))
    return img


cab.paint = {'-z': front, '+x': 'side', '-x': 'side', '+z': 'side', '+y': 'top', '-y': 'top'}
m.swatch('side', side)
m.swatch('top', paint(GREY, 0.4))
m.swatch('inside', paint('1C1F24', 0.2, 1))
m.swatch('rubber', rubber((28, 28, 30)))

if __name__ == '__main__':
    m.build()
