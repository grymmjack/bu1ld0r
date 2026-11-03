#!/usr/bin/python3
"""c0-table-flipped: a sci-fi table knocked onto its edge for cover - the top standing up (dark,
cyan light inlays, orange trim), its underside with magenta glow pads and a rim, four legs sticking
out with braces and feet. The game's is 0.95 x 0.50 x 0.54 cells."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, rubber, glow  # noqa: E402

DARK, CYAN, PINK, ORANGE = '22252B', (60, 220, 255), (240, 60, 230), (255, 150, 40)
m = Model('table-flipped', HERE, seed=31)
m.material('main', 'paint')
top = m.box('top', (0, 0, -0.25), (0.95, 0.50, 0.04), DARK)
rim = m.box('rim', (0, 0.05, -0.215), (0.85, 0.40, 0.03), '1A1C21', paint='rimside')
for i, (x, y) in enumerate(((0.39, 0.06), (-0.39, 0.06), (0.39, 0.39), (-0.39, 0.39))):
    m.box(f'leg-{i}', (x, y, 0.01), (0.05, 0.05, 0.42), '30333A', paint='leg')
    m.box(f'foot-{i}', (x, y - 0.006, 0.235), (0.07, 0.062, 0.03), '111114', paint='rubber')
for i, x in enumerate((0.39, -0.39)):
    m.box(f'brace-{i}', (x, 0.11, 0.15), (0.03, 0.28, 0.03), '30333A', paint='leg')


def top_front(a, w, h):
    """The table's top, now facing out: two long cyan inlays, orange edge trim."""
    img = paint(DARK, 0.8)(a, w, h)
    a.rect(img, (0, 0, w, 2), ORANGE)
    a.rect(img, (0, h - 2, w, h), ORANGE)
    for y0, y1 in ((0.15, 0.42), (0.58, 0.85)):
        box = (w * 0.06, h * y0, w * 0.94, h * y1)
        a.rect(img, box, (14, 70, 92))
        img = glow(img, a, box, CYAN, 0.2, 1)
        for k in range(1, 12):                              # the inlay's panel lines
            x = box[0] + (box[2] - box[0]) * k / 12
            a.rect(img, (x, box[1], x + 0.6, box[3]), (8, 30, 40))
        a.rect(img, (box[0], box[1], box[2], box[1] + 1), (150, 240, 255))
        a.rect(img, (box[0], box[3] - 1, box[2], box[3]), (40, 150, 190))
    img = a.text(img, 'MESS DECK 2', h * 0.06, (w * 0.06, h * 0.44, w * 0.5, h * 0.56), ORANGE, 'l')
    return img


def under(a, w, h):
    """The underside, facing the legs: magenta glow pads."""
    img = paint('1A1C21', 0.5)(a, w, h)
    for x0 in (0.1, 0.55):
        box = (w * x0, h * 0.2, w * (x0 + 0.35), h * 0.8)
        a.rect(img, box, (120, 24, 116))
        img = glow(img, a, box, PINK, 0.25, 1)
        a.rect(img, (box[0] + 2, box[1] + 2, box[2] - 2, box[3] - 2), (200, 60, 200), 0.6)
        a.rect(img, (box[0] + 4, box[1] + 4, box[2] - 4, box[3] - 4), (120, 24, 116))
    return img


def edge(a, w, h):
    img = paint(DARK, 0.4)(a, w, h)
    a.rect(img, (0, h * 0.3, w, h * 0.7), ORANGE, 0.9)
    return img


top.paint = {'-z': top_front, '+z': under, '*': 'edge'}
rim.paint = {'+z': under, '*': 'rimside'}
m.swatch('edge', edge)
m.swatch('rimside', paint('1A1C21', 0.3))
m.swatch('leg', steel((110, 114, 122)))
m.swatch('rubber', rubber((30, 30, 32)))

if __name__ == '__main__':
    m.build()
