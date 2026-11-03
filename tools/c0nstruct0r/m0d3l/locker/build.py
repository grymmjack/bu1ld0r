#!/usr/bin/python3
"""c0-locker: a bank of three lockers (blue, grey, blue) - doors standing proud of their frames,
vents, name cards, steel handles, on a kick base. The game's is 0.79 x 0.83 x 0.45 cells."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, front_box, hexrgb  # noqa: E402

BLUE, GREY, BASE = '2F5F8F', '78838E', '24272B'
m = Model('locker', HERE, seed=7)
m.material('main', 'paint')
m.box('base', (0, 0, 0.01), (0.78, 0.04, 0.42), BASE, paint='base')
lockers = []
for i, (x, col) in enumerate(((0.265, BLUE), (0, GREY), (-0.265, BLUE))):
    p = m.box(f'locker-{i}', (x, 0.04, 0), (0.26, 0.79, 0.44), col, walls=f'edge{i}')
    p.cut('-z', (x - 0.115, x + 0.115, 0.06, 0.815), -0.006)
    lockers.append((p, col, x, i))
    m.box(f'handle-{i}', (x - 0.085, 0.40, -0.2295), (0.018, 0.07, 0.014), 'C8CCD2', paint='steel')


def door(p, col, x, i):
    def f(a, w, h):
        img = paint(col)(a, w, h)
        d = front_box(p, w, h, x - 0.115, x + 0.115, 0.06, 0.815)
        a.rect(img, d, tuple(min(255, v + 10) for v in hexrgb(col)), 0.5)
        dw, dh = d[2] - d[0], d[3] - d[1]
        for k in range(7):                                         # the vents, pressed louvres
            y = d[1] + dh * 0.05 + k * dh * 0.03
            a.rect(img, (d[0] + dw * 0.15, y, d[2] - dw * 0.15, y + dh * 0.016), (18, 22, 28))
            a.rect(img, (d[0] + dw * 0.15, y + dh * 0.016, d[2] - dw * 0.15, y + dh * 0.02),
                    tuple(min(255, v + 45) for v in hexrgb(col)))
        cy = d[1] + dh * 0.33
        a.rect(img, (d[0] + dw * 0.3, cy, d[2] - dw * 0.3, cy + dh * 0.05), (60, 60, 60))      # card holder
        a.rect(img, (d[0] + dw * 0.32, cy + dh * 0.006, d[2] - dw * 0.32, cy + dh * 0.044), (240, 220, 140))
        img = a.text(img, ['R. VASQUEZ', 'SPARE', 'D. OKAFOR'][i], dh * 0.025,
                     (d[0] + dw * 0.32, cy + dh * 0.006, d[2] - dw * 0.32, cy + dh * 0.044), (40, 40, 40))
        img = a.text(img, f'{14 + i:02d}', dh * 0.05, (d[0], d[1] + dh * 0.86, d[2], d[1] + dh * 0.95),
                     (235, 235, 230), alpha=0.8)
        if i == 2:
            a.rect(img, (d[0] + dw * 0.18, d[1] + dh * 0.70, d[0] + dw * 0.42, d[1] + dh * 0.76), (200, 40, 40))
            img = a.text(img, 'NO', dh * 0.03, (d[0] + dw * 0.18, d[1] + dh * 0.70, d[0] + dw * 0.42,
                                                 d[1] + dh * 0.76), (250, 250, 245))
        return img
    return f


def side(col):
    def f(a, w, h):
        img = paint(col)(a, w, h)
        a.rect(img, (0, h * 0.02, w, h * 0.025), (0, 0, 0), 0.25)
        return img
    return f


for p, col, x, i in lockers:
    p.paint = {'-z': door(p, col, x, i), '+z': f'plain{col}', '+x': f'side{col}', '-x': f'side{col}',
               '+y': f'plain{col}', '-y': 'base'}
    m.swatch(f'plain{col}', paint(col))
    m.swatch(f'side{col}', side(col))
    m.swatch(f'edge{i}', paint(tuple(int(v * 0.8) for v in hexrgb(col)), 0.2, 1))
m.swatch('steel', steel())
m.swatch('base', paint(BASE, 0.4))

if __name__ == '__main__':
    m.build()
