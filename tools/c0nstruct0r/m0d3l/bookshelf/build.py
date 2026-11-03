#!/usr/bin/python3
"""c0-bookshelf: a dark metal shelving unit - sides with pink edge lights, a back, six boards,
five rows of books (spines of every height and colour, a few glowing data-slates). The game's is
0.77 x 0.77 x 0.28 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, glow  # noqa: E402

FRAME, BACK, PINK, CYAN = '2A2C33', (22, 22, 28), (240, 70, 200), (60, 220, 255)
m = Model('bookshelf', HERE, seed=43)
m.material('main', 'paint')
for i, x in enumerate((0.374, -0.374)):
    m.box(f'side-{i}', (x, 0, 0), (0.02, 0.768, 0.28), FRAME, paint={'-z': 'sidefront', '*': 'frame'})
m.box('back', (0, 0, 0.1325), (0.728, 0.768, 0.015), '18181E', paint={'-z': 'backin', '*': 'frame'})
for i, y in enumerate((0, 0.15, 0.30, 0.45, 0.60, 0.75)):
    m.box(f'board-{i}', (0, y, 0.0025), (0.728, 0.018, 0.27), FRAME, paint='board')
rows = []
for i, y in enumerate((0.018, 0.168, 0.318, 0.468, 0.618)):
    b = m.box(f'books-{i}', (0, y, 0.025), (0.72, 0.118, 0.18), '402020')
    rows.append(b)


def spines(seed):
    def f(a, w, h):
        r = np.random.default_rng(seed)
        img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array(BACK, np.float32)
        x = 0.5
        cols = [(110, 30, 34), (30, 40, 90), (30, 74, 50), (90, 60, 34), (70, 70, 80), (120, 100, 50), (50, 30, 70)]
        while x < w - 1:
            bw = r.uniform(1.6, 4.2)
            if r.random() < 0.06:                         # a glowing data-slate standing among the books
                c = CYAN if r.random() < 0.6 else PINK
                bh = h * r.uniform(0.55, 0.8)
                box = (x, h - bh, x + bw * 2.2, h)
                a.rect(img, box, tuple(int(v * 0.5) for v in c))
                a.rect(img, (box[0] + 0.6, box[1] + 0.6, box[2] - 0.6, box[3] - 1.5), c, 0.8)
                img = glow(img, a, box, c, 0.2, 1)
                x += bw * 2.2 + 0.3
                continue
            if r.random() < 0.05:                         # a gap, a book fallen over
                lh = r.uniform(1.4, 2.2)
                a.rect(img, (x, h - lh, x + 7, h), cols[int(r.integers(0, len(cols)))])
                x += 7.5
                continue
            c = cols[int(r.integers(0, len(cols)))]
            c = tuple(int(v * r.uniform(0.75, 1.2)) for v in c)
            bh = h * r.uniform(0.68, 0.97)
            a.rect(img, (x, h - bh, x + bw, h), c)
            a.rect(img, (x, h - bh, x + 0.3, h), tuple(min(255, v + 30) for v in c))
            for t in (0.18, 0.78):
                a.rect(img, (x + 0.3, h - bh * t - 0.5, x + bw - 0.3, h - bh * t), (190, 160, 80), 0.8)
            x += bw + 0.15
        return img
    return f


def sidefront(a, w, h):
    img = paint(FRAME, 0.3)(a, w, h)
    a.rect(img, (w * 0.3, 0, w * 0.7, h), PINK, 0.85)
    return glow(img, a, (w * 0.3, 0, w * 0.7, h), PINK, 0.2, 1)


for i, b in enumerate(rows):
    b.paint = {'-z': spines(100 + i), '+y': 'booktop', '*': 'bookside'}
m.swatch('frame', paint(FRAME, 0.3))
m.swatch('sidefront', sidefront)
m.swatch('board', paint(FRAME, 0.4))
m.swatch('backin', paint('18181E', 0.2))
m.swatch('booktop', paint((60, 50, 44), 0.2, 1))
m.swatch('bookside', paint((90, 40, 36), 0.2, 1))

if __name__ == '__main__':
    m.build()
