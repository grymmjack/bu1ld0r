#!/usr/bin/python3
"""c0-terminal: a retro tan computer terminal - base deck with a green-key keyboard, a monitor
housing behind with its green CRT set in. The game's is 0.55 x 0.55 x 0.33 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, rubber, glow, front_box, hexrgb  # noqa: E402

TAN, DARK, GREEN = 'B8834A', '2A2622', (70, 255, 120)
m = Model('terminal', HERE, seed=9)
m.material('main', 'paint')
base = m.box('base', (0, 0, 0), (0.55, 0.20, 0.32), TAN)
mon = m.box('monitor', (0, 0.20, 0.07), (0.55, 0.35, 0.18), TAN, walls='bezel')
mon.cut('-z', (-0.235, 0.235, 0.37, 0.53), 0.025)
kb = m.box('keyboard', (0.03, 0.20, -0.095), (0.42, 0.022, 0.11), DARK, paint='kbside')
pad = m.box('keypad', (-0.215, 0.20, -0.095), (0.09, 0.03, 0.11), DARK, paint='kbside')


def crt(a, img, box):
    x0, y0, x1, y1 = box
    a.rect(img, box, (8, 30, 14))
    img = glow(img, a, (x0 + 3, y0 + 3, x1 - 3, y1 - 3), (30, 120, 50), 0.5, 4)
    lines = ['> SYS DIAG ......... OK', '> HULL PRESSURE ...... 98%', '> CREW MANIFEST: 4 / 6',
             '> CORE TEMP ....... HIGH', '> _']
    lh = (y1 - y0) / (len(lines) + 1.5)
    for i, t in enumerate(lines):
        img = a.text(img, t, lh * 0.62, (x0 + 4, y0 + lh * (i + 0.6), x1 - 4, y0 + lh * (i + 1.4)), GREEN, 'l', 0.9)
    for yy in np.arange(y0, y1, 0.75):
        a.rect(img, (x0, yy, x1, yy + 0.25), (0, 0, 0), 0.25)      # scanlines
    return img


def mon_front(a, w, h):
    img = paint(TAN)(a, w, h)
    s = front_box(mon, w, h, -0.235, 0.235, 0.37, 0.53)
    a.rect(img, (s[0] - 2.5, s[1] - 2.5, s[2] + 2.5, s[3] + 2.5), hexrgb(DARK))
    img = crt(a, img, s)
    # the strip under the screen: lamps, a dial, a label
    y = s[3] + (h - s[3]) * 0.35
    for i in range(6):
        c = [(80, 255, 120), (255, 200, 60), (80, 255, 120), (255, 60, 60), (80, 160, 255), (80, 255, 120)][i]
        cx = w * 0.12 + i * w * 0.045
        a.rect(img, (cx, y, cx + w * 0.025, y + w * 0.025), c)
        img = glow(img, a, (cx, y, cx + w * 0.025, y + w * 0.025), c, 0.25, 1)
    img = a.text(img, 'DATACORE 6000', h * 0.07, (w * 0.5, y - 2, w * 0.92, y + h * 0.1), (60, 40, 20), 'r')
    for i in range(14):                                     # side vents
        yy = h * 0.08 + i * h * 0.035
        a.rect(img, (w * 0.02, yy, w * 0.06, yy + h * 0.015), (60, 40, 20))
        a.rect(img, (w * 0.94, yy, w * 0.98, yy + h * 0.015), (60, 40, 20))
    return img


def base_front(a, w, h):
    img = paint(TAN)(a, w, h)
    a.rect(img, (w * 0.05, h * 0.18, w * 0.95, h * 0.22), (60, 40, 20))
    for i in range(3):                                      # drive bays
        x0 = w * (0.08 + i * 0.2)
        a.rect(img, (x0, h * 0.35, x0 + w * 0.17, h * 0.62), (34, 30, 26))
        a.rect(img, (x0 + w * 0.02, h * 0.46, x0 + w * 0.15, h * 0.5), (10, 10, 10))
        a.rect(img, (x0 + w * 0.13, h * 0.38, x0 + w * 0.15, h * 0.42), (80, 255, 120))
    a.rect(img, (w * 0.7, h * 0.33, w * 0.92, h * 0.66), (30, 50, 34))
    img = glow(img, a, (w * 0.72, h * 0.36, w * 0.9, h * 0.63), (60, 200, 90), 0.4, 1)
    for i in range(4):
        a.rect(img, (w * 0.73, h * (0.38 + i * 0.065), w * 0.89, h * (0.41 + i * 0.065)), (110, 255, 150))
    return img


def keys(cols, rows, accent=None):
    def f(a, w, h):
        img = paint(DARK, 0.2, 1)(a, w, h)
        kw, kh = w / cols, h / rows
        for r in range(rows):
            for c in range(cols):
                x0, y0 = c * kw + kw * 0.12, r * kh + kh * 0.14
                col = (60, 200, 90) if (accent is None or (r, c) not in accent) else (230, 200, 70)
                a.rect(img, (x0, y0, x0 + kw * 0.76, y0 + kh * 0.72), col)
                a.rect(img, (x0, y0, x0 + kw * 0.76, y0 + kh * 0.2), tuple(min(255, v + 60) for v in col))
        return img
    return f


base.paint = {'-z': base_front, '+z': 'tan', '+x': 'tanside', '-x': 'tanside', '+y': 'tan', '-y': 'dark'}
mon.paint = {'-z': mon_front, '+z': 'tanback', '+x': 'tanside', '-x': 'tanside', '+y': 'tan', '-y': 'dark'}
kb.paint = {'+y': keys(12, 4, {(3, 0), (3, 11)}), '*': 'kbside'}
pad.paint = {'+y': keys(3, 4, {(3, 2)}), '*': 'kbside'}
m.swatch('tan', paint(TAN))
m.swatch('dark', paint(DARK, 0.2))
m.swatch('kbside', paint(DARK, 0.2, 1))
m.swatch('bezel', paint(DARK, 0.2, 1))


def tanside(a, w, h):
    img = paint(TAN)(a, w, h)
    for i in range(8):
        y = h * 0.2 + i * h * 0.05
        a.rect(img, (w * 0.3, y, w * 0.7, y + h * 0.02), (60, 40, 20))
    return img


def tanback(a, w, h):
    img = paint(TAN)(a, w, h)
    return a.label(img, (w * 0.35, h * 0.2, w * 0.65, h * 0.45), [('DATACORE 6000', 3), ('S/N 00731  115V', 2.4)], 4)


m.swatch('tanside', tanside)
m.swatch('tanback', tanback)

if __name__ == '__main__':
    m.build()
