#!/usr/bin/python3
"""c0-desk: an office desk - wood top, steel legs, a drawer unit, a modesty panel, a monitor of
green text on a stand, a keyboard, a red mug. The game's is 0.42 x 0.34 x 0.24 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, wood, glow, front_box  # noqa: E402

GREY, LEG, WOODC = '9EA4AC', '3A3D42', (176, 112, 66)
m = Model('desk', HERE, seed=23)
m.material('main', 'paint')
top = m.box('top', (0, 0.20, 0), (0.42, 0.018, 0.23), 'B07042')
for i, z in enumerate((0.095, -0.095)):
    m.box(f'leg-{i}', (0.19, 0, z), (0.018, 0.20, 0.018), LEG, paint='leg')
drawers = m.box('drawers', (-0.135, 0, 0), (0.12, 0.20, 0.21), GREY)
m.box('panel', (0.035, 0.09, 0.098), (0.30, 0.10, 0.012), LEG, paint='leg')
m.box('stand', (0.03, 0.218, 0.05), (0.07, 0.006, 0.05), LEG, paint='leg')
m.box('neck', (0.03, 0.224, 0.06), (0.016, 0.026, 0.012), LEG, paint='leg')
mon = m.box('screen', (0.03, 0.248, 0.052), (0.19, 0.10, 0.014), '1A1C20', walls='bezel')
mon.cut('-z', (-0.055, 0.115, 0.256, 0.34), 0.004)
kb = m.box('keyboard', (0.03, 0.218, -0.06), (0.13, 0.008, 0.045), 'D8D8D4', paint='kbside')
mug = m.cyl('mug', (-0.12, 0.218, -0.03), (0.03, 0.034, 0.03), 'C02020', seg=8,
            paint={'side': 'mugside', 'top': 'coffee', 'bottom': 'red'})
m.box('mug-handle', (-0.1385, 0.226, -0.03), (0.008, 0.018, 0.006), 'C02020', paint='red')


def screen(a, w, h):
    img = paint('1A1C20', 0.2, 1)(a, w, h)
    s = front_box(mon, w, h, -0.055, 0.115, 0.256, 0.34)
    a.rect(img, s, (6, 20, 10))
    img = glow(img, a, s, (40, 160, 70), 0.35, 3)
    lines = ['MAIL (3)', '> SHIFT LOG 0300', '> DECK C SEALED', '> REPORT TO MED']
    lh = (s[3] - s[1]) / 6
    for i, t in enumerate(lines):
        img = a.text(img, t, lh * 0.7, (s[0] + 2, s[1] + lh * (i + 0.5), s[2] - 2, s[1] + lh * (i + 1.4)),
                     (110, 255, 140), 'l')
    a.rect(img, (s[0] + 2, s[1] + lh * 4.8, s[0] + (s[2] - s[0]) * 0.6, s[1] + lh * 5.3), (90, 230, 120))
    return img


def drawers_front(a, w, h):
    img = paint(GREY)(a, w, h)
    for k, (y0, y1) in enumerate(((0.05, 0.3), (0.33, 0.6), (0.63, 0.95))):
        a.rect(img, (w * 0.05, h * y0, w * 0.95, h * y1), (170, 176, 184))
        a.rect(img, (w * 0.05, h * y1 - 0.8, w * 0.95, h * y1), (90, 94, 100))
        a.rect(img, (w * 0.35, h * (y0 + 0.05), w * 0.65, h * (y0 + 0.09)), (60, 62, 66))
    return img


def top_face(a, w, h):
    img = wood(WOODC)(a, w, h)
    a.rect(img, (w * 0.62, h * 0.55, w * 0.8, h * 0.85), (240, 238, 228))      # papers
    a.rect(img, (w * 0.64, h * 0.6, w * 0.82, h * 0.9), (250, 250, 244))
    for k in range(5):
        a.rect(img, (w * 0.66, h * (0.64 + k * 0.045), w * 0.79, h * (0.65 + k * 0.045)), (90, 90, 96))
    return img


def kb_top(a, w, h):
    img = paint('D8D8D4', 0.1, 1)(a, w, h)
    cols, rows = 14, 4
    kw, kh = w / cols, h / rows
    for r in range(rows):
        for c in range(cols):
            x0, y0 = c * kw + kw * 0.12, r * kh + kh * 0.14
            a.rect(img, (x0, y0, x0 + kw * 0.76, y0 + kh * 0.72), (238, 238, 234))
            a.rect(img, (x0, y0 + kh * 0.6, x0 + kw * 0.76, y0 + kh * 0.72), (160, 160, 156))
    return img


def mugside(a, w, h):
    img = paint((196, 30, 30), 0.1, 1)(a, w, h)
    return a.text(img, 'WORLD\'S OK-EST TECH', h * 0.14, (w * 0.25, h * 0.35, w * 0.75, h * 0.6), (250, 245, 240))


top.paint = {'+y': top_face, '-y': 'woodplain', '*': 'woodedge'}
drawers.paint = {'-z': drawers_front, '*': 'grey'}
mon.paint = {'-z': screen, '*': 'bezel'}
kb.paint = {'+y': kb_top, '*': 'kbside'}
m.swatch('woodplain', wood(WOODC))
m.swatch('woodedge', lambda a, w, h: wood((196, 110, 50))(a, w, h))
m.swatch('grey', paint(GREY))
m.swatch('leg', steel((120, 124, 130)))
m.swatch('bezel', paint('1A1C20', 0.2, 1))
m.swatch('kbside', paint('C8C8C4', 0.1, 1))
m.swatch('red', paint((196, 30, 30), 0.1, 1))
m.swatch('mugside', mugside)
m.swatch('coffee', lambda a, w, h: a.cross(paint((60, 34, 18), 0, 1)(a, w, h), 0, 0, 0, 0, (0, 0, 0)))

if __name__ == '__main__':
    m.build()
