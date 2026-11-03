#!/usr/bin/python3
"""c0-vending: a snack machine - pink sides, cyan trim, a deep glass window of snacks, keypad, a
delivery bin, a lit sign cap. The game's is 0.37 x 0.74 x 0.27 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, rubber, glow, front_box, hexrgb  # noqa: E402

PINK, CYAN, SILVER, DARK = 'E2407F', '2EC8D8', 'A8AEB6', '26282C'
m = Model('vending', HERE, seed=5)
m.material('main', 'paint')

feet = [m.box(f'foot-{i}', (sx * 0.14, 0, sz * 0.095), (0.04, 0.04, 0.04), CYAN, paint='cyan')
        for i, (sx, sz) in enumerate(((1, 1), (-1, 1), (1, -1), (-1, -1)))]
plinth = m.box('plinth', (0, 0.04, 0), (0.34, 0.13, 0.25), SILVER, walls='inside')
plinth.cut('-z', (-0.1, 0.1, 0.065, 0.14), 0.045)
body = m.box('body', (0, 0.17, 0), (0.34, 0.51, 0.25), SILVER, walls='inside')
body.cut('-z', (-0.04, 0.15, 0.24, 0.64), 0.05)
cap = m.box('cap', (0, 0.68, 0), (0.36, 0.06, 0.26), CYAN)
pad = m.box('keypad', (-0.115, 0.36, -0.125), (0.07, 0.22, 0.02), DARK)
card = m.box('reader', (-0.175, 0.38, -0.05), (0.02, 0.12, 0.06), DARK, paint='darkmetal')


def snacks(a, img, box):
    """Shelves of snacks in a window (box in region px), behind tinted glass."""
    x0, y0, x1, y1 = box
    a.rect(img, box, (30, 34, 40))
    rows = 4
    r = a.rng
    cols = [(240, 60, 90), (255, 200, 40), (60, 200, 90), (60, 150, 255), (250, 120, 30), (180, 80, 230)]
    rh = (y1 - y0) / rows
    for i in range(rows):
        sy = y0 + rh * (i + 1)
        a.rect(img, (x0, sy - rh * 0.12, x1, sy), (150, 156, 164))       # the shelf lip
        a.rect(img, (x0, sy - rh * 0.14, x1, sy - rh * 0.12), (220, 225, 230))
        n = 4
        cw = (x1 - x0) / n
        for j in range(n):
            c = cols[int(r.integers(0, len(cols)))]
            px0, px1 = x0 + cw * j + cw * 0.12, x0 + cw * (j + 1) - cw * 0.12
            py0, py1 = sy - rh * 0.14 - rh * 0.66, sy - rh * 0.14
            a.rect(img, (px0, py0, px1, py1), c)
            a.rect(img, (px0, py0, px1, py0 + (py1 - py0) * 0.22), tuple(min(255, v + 50) for v in c))
            a.rect(img, (px0 + (px1 - px0) * 0.2, py0 + (py1 - py0) * 0.42, px1 - (px1 - px0) * 0.2,
                         py0 + (py1 - py0) * 0.62), (250, 250, 245), 0.85)   # the label
            a.rect(img, ((px0 + px1) / 2 - 0.6, sy - rh * 0.14 - 0.1, (px0 + px1) / 2 + 0.6, sy), (60, 60, 64))
    a.rect(img, box, (120, 200, 230), 0.12)                                   # the glass's tint
    hh = y1 - y0
    for k in range(int((x1 - x0 + hh) / 6)):
        u = x0 + k * 6
        for t in np.arange(0, hh, 0.5):
            if r.random() < 0.0:
                continue
        if k % 3 == 0:
            for t in np.arange(0, hh, 0.5):
                xx = u - t * 0.6
                if x0 <= xx < x1 - 2:
                    a.rect(img, (xx, y0 + t, xx + 2.2, y0 + t + 0.5), (255, 255, 255), 0.10)
    return img


def body_front(a, w, h):
    img = paint(SILVER)(a, w, h)
    wb = front_box(body, w, h, -0.04, 0.15, 0.24, 0.64)
    pad_ = 0.03 / 0.34 * w * 0.6
    a.rect(img, (wb[0] - pad_, wb[1] - pad_, wb[2] + pad_, wb[3] + pad_), hexrgb(CYAN))   # the window's frame
    img = snacks(a, img, wb)
    img = a.text(img, 'SNAX-0-MATIC', 4.5, (wb[0], wb[3] + pad_ + 1, wb[2], wb[3] + pad_ + 8), hexrgb(PINK))
    return img


def plinth_front(a, w, h):
    img = paint(SILVER)(a, w, h)
    bb = front_box(plinth, w, h, -0.1, 0.1, 0.065, 0.14)
    a.rect(img, (bb[0] - 2, bb[1] - 2, bb[2] + 2, bb[3] + 2), hexrgb(CYAN))
    a.rect(img, bb, (40, 46, 54))
    a.rect(img, (bb[0], bb[1], bb[2], bb[1] + (bb[3] - bb[1]) * 0.55), (70, 90, 100), 0.9)  # smoked flap
    img = a.text(img, 'PUSH', 4, (bb[0], bb[1] + 1, bb[2], bb[1] + 7), (200, 230, 235))
    return img


def side(a, w, h):
    img = paint(PINK)(a, w, h)
    a.rect(img, (0, 0, w, 2), hexrgb(CYAN))
    a.rect(img, (2, h * 0.08, 3, h * 0.92), (255, 255, 255), 0.25)
    return img


def cap_front(a, w, h):
    img = paint(CYAN)(a, w, h)
    box = (w * 0.12, h * 0.15, w * 0.88, h * 0.85)
    a.rect(img, box, (30, 20, 40))
    img = glow(img, a, (box[0] + 4, box[1] + 2, box[2] - 4, box[3] - 2), hexrgb(PINK), 0.35, 2)
    img = a.text(img, 'SNACKS', h * 0.55, box, (255, 120, 190))
    return img


def keypad(a, w, h):
    img = paint(DARK, 0.3)(a, w, h)
    a.rect(img, (w * 0.12, h * 0.06, w * 0.88, h * 0.2), (20, 40, 30))               # the display
    img = a.text(img, '0.75', h * 0.1, (w * 0.12, h * 0.06, w * 0.88, h * 0.2), (90, 255, 140))
    for i in range(4):
        for j in range(3):
            x0, y0 = w * (0.14 + j * 0.25), h * (0.27 + i * 0.1)
            a.rect(img, (x0, y0, x0 + w * 0.2, y0 + h * 0.07), (190, 196, 204))
            a.rect(img, (x0, y0 + h * 0.06, x0 + w * 0.2, y0 + h * 0.07), (90, 94, 100))
    a.rect(img, (w * 0.4, h * 0.72, w * 0.6, h * 0.86), (12, 12, 14))                # coin slot
    a.rect(img, (w * 0.47, h * 0.74, w * 0.53, h * 0.84), (180, 180, 186))
    return img


def body_back(a, w, h):
    img = paint(SILVER)(a, w, h)
    for i in range(9):                                          # a vent grille for the compressor
        y = h * 0.62 + i * h * 0.035
        a.rect(img, (w * 0.25, y, w * 0.75, y + h * 0.018), (40, 42, 46))
    img = a.label(img, (w * 0.32, h * 0.16, w * 0.68, h * 0.34),
                  [('SNAX-0-MATIC 3000', 3), ('230V  4.2A  REFRIG.', 2.4)], seed=3)
    return img


paint_body = {'-z': body_front, '+z': body_back, '+x': side, '-x': side, '+y': paint(SILVER), '-y': paint(DARK)}
body.paint = paint_body
plinth.paint = {'-z': plinth_front, '+z': paint(SILVER), '+x': side, '-x': side, '+y': paint(SILVER), '-y': paint(DARK)}
cap.paint = {'-z': cap_front, '+z': cap_front, '+x': paint(CYAN), '-x': paint(CYAN), '+y': paint(CYAN), '-y': paint(CYAN)}
pad.paint = {'-z': keypad, '*': 'darkmetal'}
m.swatch('cyan', paint(CYAN, 0.3))
m.swatch('inside', paint('3A3E44', 0.2, 1))
m.swatch('darkmetal', paint(DARK, 0.3))

if __name__ == '__main__':
    m.build()
