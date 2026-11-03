#!/usr/bin/python3
"""c0-chest (and c0-mimic-asleep, c0-chest-open: `build.py mimic` / `build.py open`): a black
armoured loot chest - a skirt, steel corner guards, glowing strips, a lid with a carry handle, a lock
across the seam (cyan; the mimic's is red - its only tell). Open: the lid stands up at the back,
lit inside, the chest heaped with glowing gems. The game's is 0.35 x 0.31 x 0.23 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow, front_box  # noqa: E402

BLACK, TRIM, CYAN = '1E2126', '2E333A', (50, 230, 240)
kind = sys.argv[1] if len(sys.argv) > 1 else 'chest'
NAME = {'chest': 'chest', 'mimic': 'mimic-asleep', 'open': 'chest-open'}[kind]
LOCK = (255, 40, 90) if kind == 'mimic' else CYAN
m = Model(NAME, os.path.join(HERE, '..', NAME), seed={'chest': 71, 'mimic': 73, 'open': 75}[kind])
m.material('main', 'paint')
m.box('skirt', (0, 0, 0), (0.354, 0.016, 0.226), '15171A', paint='skirt')
base = m.box('base', (0, 0.016, 0), (0.33, 0.166, 0.2), BLACK, walls='cavein')
for i, (x, z) in enumerate(((0.158, -0.093), (-0.158, -0.093), (0.158, 0.093), (-0.158, 0.093))):
    m.box(f'guard-{i}', (x, 0.016, z), (0.03, 0.166, 0.03), '8A9098', paint='guard')
if kind == 'open':
    base.cut('+y', (-0.15, 0.15, -0.085, 0.085), 0.13)
    lid = m.box('lid', (0, 0.182, 0.128), (0.34, 0.21, 0.056), TRIM)
    gems = m.box('gems', (0, 0.1, 0), (0.30, 0.07, 0.17), '6040C0', paint={'+y': 'gemtop', '*': 'gemside'})
    r = np.random.default_rng(9)
    cols = ['40E0FF', 'FF40C0', '60FF80', 'FFD040', 'A060FF']
    for i in range(7):
        x, z, s = r.uniform(-0.12, 0.12), r.uniform(-0.06, 0.06), r.uniform(0.025, 0.04)
        m.box(f'gem-{i}', (round(x, 3), 0.17, round(z, 3)), (s, s * 0.8, s), cols[i % 5], paint=f'gem{i % 5}')
else:
    lid = m.box('lid', (0, 0.182, 0), (0.34, 0.08, 0.21), TRIM)
    for i, x in enumerate((0.065, -0.065)):
        m.box(f'handle-post-{i}', (x, 0.262, 0), (0.016, 0.03, 0.022), '8A9098', paint='guard')
    m.box('handle', (0, 0.288, 0), (0.15, 0.017, 0.026), '14161A', paint='grip')
lock = m.box('lock', (0, 0.135 if kind != 'open' else 0.12, -0.106), (0.042, 0.065, 0.013), '30343A')


def base_front(a, w, h):
    img = paint(BLACK, 0.5)(a, w, h)
    for u in (0.24, 0.76):                                             # glowing strips
        box = (w * u - 2.2, h * 0.18, w * u + 2.2, h * 0.86)
        a.rect(img, box, CYAN)
        a.rect(img, (box[0] + 1, box[1] + 1, box[2] - 1, box[3] - 1), (200, 255, 255), 0.6)
        img = glow(img, a, box, CYAN, 0.2, 2)
    a.rect(img, (0, h * 0.08, w, h * 0.08 + 0.8), (60, 66, 74))
    for x in np.arange(w * 0.32, w * 0.68, 3):                         # panel lines
        a.rect(img, (x, h * 0.55, x + 0.5, h * 0.9), (12, 13, 15))
    return img


def base_side(a, w, h):
    img = paint(BLACK, 0.5)(a, w, h)
    a.rect(img, (w * 0.25, h * 0.3, w * 0.75, h * 0.5), (60, 66, 74))  # a side grip
    a.rect(img, (w * 0.3, h * 0.36, w * 0.7, h * 0.44), (14, 15, 17))
    box = (w * 0.42, h * 0.62, w * 0.58, h * 0.68)
    a.rect(img, box, CYAN)
    return glow(img, a, box, CYAN, 0.18, 1)


def lid_face(a, w, h):
    img = paint(TRIM, 0.5)(a, w, h)
    a.rect(img, (0, h - 1.4, w, h), (10, 11, 13))                     # the seam
    a.rect(img, (w * 0.04, 1.2, w * 0.96, 1.9), (90, 200, 210), 0.7)  # a cyan edge line
    return img


def lid_top(a, w, h):
    img = paint(TRIM, 0.5)(a, w, h)
    for u in (0.33, 0.67):                                             # plate seams
        a.rect(img, (w * u, 0, w * u + 0.7, h), (12, 13, 15))
    a.rect(img, (w * 0.04, h * 0.06, w * 0.96, h * 0.06 + 0.7), (90, 200, 210), 0.7)
    a.rect(img, (w * 0.04, h * 0.94 - 0.7, w * 0.96, h * 0.94), (90, 200, 210), 0.7)
    return img


def lid_inside(a, w, h):
    """The open lid's inside: a lit circuit pattern."""
    img = paint('202432', 0.3, 1)(a, w, h)
    r = np.random.default_rng(4)
    for k in range(12):
        x, y = r.uniform(w * 0.1, w * 0.9), r.uniform(h * 0.15, h * 0.85)
        L = r.uniform(6, 20)
        if r.random() < 0.5:
            a.rect(img, (x, y, min(w * 0.92, x + L), y + 0.6), (90, 140, 255))
        else:
            a.rect(img, (x, y, x + 0.6, min(h * 0.88, y + L * 0.5)), (90, 140, 255))
        a.rect(img, (x - 0.8, y - 0.8, x + 0.8, y + 0.8), (180, 210, 255))
    a.rect(img, (w * 0.05, h * 0.05, w * 0.95, h * 0.09), CYAN)
    return glow(img, a, (0, 0, w, h), (90, 120, 255), 0.12, 2)


def lock_front(a, w, h):
    img = paint('30343A', 0.3)(a, w, h)
    box = (w * 0.25, h * 0.18, w * 0.75, h * 0.82)
    a.rect(img, box, LOCK)
    a.rect(img, (box[0] + w * 0.12, box[1] + h * 0.08, box[2] - w * 0.12, box[3] - h * 0.08),
           tuple(min(255, v + 90) for v in LOCK), 0.7)
    return glow(img, a, box, LOCK, 0.25, 1)


def gem_top(a, w, h):
    """A heap of gems from above: facets of every colour, each lit from inside."""
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((40, 30, 70), np.float32)
    r = np.random.default_rng(12)
    cols = [(64, 224, 255), (255, 64, 192), (96, 255, 128), (255, 208, 64), (160, 96, 255)]
    for k in range(int(w * h / 8)):
        x, y, s = r.uniform(0, w), r.uniform(0, h), r.uniform(2, 4.5)
        c = cols[int(r.integers(0, 5))]
        a.rect(img, (x, y, x + s, y + s), tuple(int(v * 0.7) for v in c))
        a.rect(img, (x + 0.4, y + 0.4, x + s * 0.55, y + s * 0.55), tuple(min(255, v + 60) for v in c))
    return glow(img, a, (0, 0, w, h), (180, 140, 255), 0.1, 2)


def gem(c):
    def f(a, w, h):
        img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array(c, np.float32) * 0.75
        a.rect(img, (w * 0.15, h * 0.15, w * 0.5, h * 0.5), tuple(min(255, v + 80) for v in c), 0.8)
        return a.edge_dark(img, 1, 0.6)
    return f


base.paint = {'-z': base_front, '+x': 'bside', '-x': 'bside', '+z': base_front, '*': 'black'}
if kind == 'open':
    lid.paint = {'-z': lid_inside, '+z': 'lidtop', '*': 'lidface'}
else:
    lid.paint = {'+y': lid_top, '*': 'lidface'}
lock.paint = {'-z': lock_front, '*': 'lockside'}
m.swatch('black', paint(BLACK, 0.4))
m.swatch('bside', base_side)
m.swatch('cavein', paint('2A2440', 0.2, 1))
m.swatch('skirt', paint('15171A', 0.3))
m.swatch('guard', steel((92, 98, 106)))
m.swatch('grip', paint('14161A', 0.2, 1))
m.swatch('lidface', lid_face)
m.swatch('lidtop', lid_top)
m.swatch('lockside', paint('30343A', 0.3))
if kind == 'open':
    m.swatch('gemtop', gem_top)
    m.swatch('gemside', gem_top)
    for i, c in enumerate([(64, 224, 255), (255, 64, 192), (96, 255, 128), (255, 208, 64), (160, 96, 255)]):
        m.swatch(f'gem{i}', gem(c))

if __name__ == '__main__':
    m.build()
