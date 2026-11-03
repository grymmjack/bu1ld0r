#!/usr/bin/python3
"""c0-console: a control pedestal - slate cabinet with a door panel, a deck with big raised
buttons, an instrument hood with two screens set in (radar green, data blue), a red beacon with
an antenna. The game's is 0.47 x 0.39 x 0.28 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow, front_box  # noqa: E402

SLATE, DARK = '3C4450', '1E2228'
m = Model('console', HERE, seed=17)
m.material('main', 'paint')
cab = m.box('cabinet', (0, 0, 0), (0.46, 0.22, 0.26), SLATE, walls='inside')
cab.cut('-z', (-0.17, 0.17, 0.03, 0.19), 0.012)
deck = m.box('deck', (0, 0.22, 0), (0.47, 0.025, 0.28), DARK)
hood = m.box('hood', (0, 0.245, 0.085), (0.44, 0.06, 0.09), SLATE, walls='inside')
hood.cut('-z', (-0.20, 0.20, 0.255, 0.297), 0.008)
for i, (x, c) in enumerate(((0.06, 'red'), (0, 'green'), (-0.06, 'red'))):
    m.box(f'button-{i}', (x, 0.245, -0.07), (0.035, 0.012, 0.035), 'CC2222', paint=c)
m.box('post', (-0.18, 0.305, 0.10), (0.026, 0.026, 0.026), '888C92', paint='steel')
dome = m.cyl('beacon', (-0.18, 0.331, 0.10), (0.04, 0.03, 0.04), 'E02020', seg=8,
             paint={'side': 'redglow', 'top': 'redglow', 'bottom': 'steel'})
m.box('antenna', (-0.18, 0.361, 0.10), (0.005, 0.028, 0.005), '888C92', paint='steel')


def cab_front(a, w, h):
    img = paint(SLATE)(a, w, h)
    d = front_box(cab, w, h, -0.17, 0.17, 0.03, 0.19)
    a.rect(img, (d[0] - 1.5, d[1] - 1.5, d[2] + 1.5, d[3] + 1.5), (24, 28, 34))
    a.rect(img, d, (52, 60, 70))
    for i in range(5):
        y = d[1] + (d[3] - d[1]) * (0.2 + i * 0.1)
        a.rect(img, ((d[0] + d[2]) / 2 - 12, y, (d[0] + d[2]) / 2 + 12, y + 0.8), (24, 28, 34))
    a.rect(img, (w * 0.06, h * 0.06, w * 0.94, h * 0.08), (90, 230, 255))     # a cyan trim light
    img = glow(img, a, (w * 0.06, h * 0.06, w * 0.94, h * 0.08), (90, 230, 255), 0.25, 1)
    return img


def hood_front(a, w, h):
    img = paint(SLATE)(a, w, h)
    s = front_box(hood, w, h, -0.20, 0.20, 0.255, 0.297)
    a.rect(img, s, (12, 14, 18))
    sw = (s[2] - s[0])
    r1 = (s[0] + sw * 0.03, s[1] + 1, s[0] + sw * 0.38, s[3] - 1)   # radar (on the left, +x)
    r2 = (s[2] - sw * 0.38, s[1] + 1, s[2] - sw * 0.03, s[3] - 1)   # data
    a.rect(img, r1, (6, 30, 14))
    img = glow(img, a, r1, (40, 200, 90), 0.4, 2)
    cx, cy = (r1[0] + r1[2]) / 2, (r1[1] + r1[3]) / 2
    for rr in (2, 4, 6):
        for t in np.linspace(0, 2 * np.pi, 60):
            a.rect(img, (cx + np.cos(t) * rr * 1.6, cy + np.sin(t) * rr, cx + np.cos(t) * rr * 1.6 + 0.4,
                         cy + np.sin(t) * rr + 0.4), (90, 255, 140), 0.7)
    a.rect(img, (cx + 3, cy - 2, cx + 4.2, cy - 0.8), (200, 255, 200))
    a.rect(img, r2, (8, 20, 40))
    img = glow(img, a, r2, (60, 140, 255), 0.45, 2)
    for i in range(5):
        y = r2[1] + 1.2 + i * (r2[3] - r2[1] - 2) / 5
        a.rect(img, (r2[0] + 2, y, r2[0] + 2 + (r2[2] - r2[0] - 4) * (0.4 + 0.12 * ((i * 7) % 5)), y + 0.7),
               (150, 210, 255))
    for i in range(6):                                      # the small buttons between the screens
        x = s[0] + sw * 0.43 + (i % 3) * sw * 0.05
        y = s[1] + 1.5 + (i // 3) * (s[3] - s[1]) * 0.45
        c = (230, 40, 40) if i % 2 == 0 else (40, 220, 90)
        a.rect(img, (x, y, x + sw * 0.03, y + (s[3] - s[1]) * 0.3), c)
    return img


def deck_top(a, w, h):
    img = paint(DARK, 0.4)(a, w, h)
    a.rect(img, (w * 0.02, h * 0.9, w * 0.98, h * 0.94), (90, 230, 255), 0.8)     # the front edge's light strip
    for i in range(8):
        x = w * (0.08 + i * 0.105)
        a.rect(img, (x, h * 0.6, x + w * 0.05, h * 0.68), [(230, 40, 40), (40, 220, 90)][i % 2])
    return img


cab.paint = {'-z': cab_front, '+z': 'back', '+x': 'side', '-x': 'side', '+y': 'side', '-y': 'dark'}
deck.paint = {'+y': deck_top, '*': 'dark'}
hood.paint = {'-z': hood_front, '*': 'side'}
m.swatch('side', paint(SLATE))
m.swatch('back', lambda a, w, h: a.label(paint(SLATE)(a, w, h), (w * 0.35, h * 0.25, w * 0.65, h * 0.6),
                                         [('CTRL-4 PEDESTAL', 3), ('DECK B', 2.4)], 6))
m.swatch('dark', paint(DARK, 0.4))
m.swatch('inside', paint('20242A', 0.2, 1))
m.swatch('steel', steel((170, 174, 180)))


def plastic(rgb):
    def f(a, w, h):
        img = paint(rgb, 0.1, 1)(a, w, h)
        return glow(img, a, (w * 0.2, h * 0.2, w * 0.8, h * 0.8), tuple(min(255, v + 80) for v in rgb), 0.35, 2)
    return f


m.swatch('red', plastic((210, 30, 30)))
m.swatch('green', plastic((30, 190, 80)))
m.swatch('redglow', plastic((235, 40, 40)))

if __name__ == '__main__':
    m.build()
