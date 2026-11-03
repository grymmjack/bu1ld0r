#!/usr/bin/python3
"""c0-alarmpc: a security command desk - two pedestals, a desk slab, a back panel with cyan
underlights, a raised control deck glowing red / cyan, a monitor bank with the main screen set in,
a red-topped joystick. The game's is 0.53 x 0.51 x 0.27 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow, front_box  # noqa: E402

CASE, DARK, CYAN, RED = '2A2E35', '17191D', (60, 230, 255), (255, 50, 60)
m = Model('alarmpc', HERE, seed=19)
m.material('main', 'paint')
peds = [m.box(f'pedestal-{i}', (x, 0, 0), (0.08, 0.26, 0.24), CASE) for i, x in enumerate((0.22, -0.22))]
under = m.box('underpanel', (0, 0.04, 0.10), (0.36, 0.20, 0.02), DARK)
desk = m.box('desk', (0, 0.26, 0), (0.53, 0.04, 0.265), DARK)
deckp = m.box('deck', (0, 0.30, -0.06), (0.50, 0.025, 0.13), CASE)
bank = m.box('monitors', (0, 0.30, 0.075), (0.50, 0.18, 0.10), CASE, walls='inside')
bank.cut('-z', (-0.15, 0.15, 0.335, 0.465), 0.015)
stick = m.cyl('joystick', (-0.20, 0.325, -0.07), (0.03, 0.035, 0.03), 'E02020', seg=8,
              paint={'side': 'redknob', 'top': 'redknob', 'bottom': 'dark'})


def bank_front(a, w, h):
    img = paint(CASE)(a, w, h)
    s = front_box(bank, w, h, -0.15, 0.15, 0.335, 0.465)
    a.rect(img, (s[0] - 1.5, s[1] - 1.5, s[2] + 1.5, s[3] + 1.5), (10, 10, 12))
    a.rect(img, s, (6, 22, 30))
    img = glow(img, a, s, (40, 160, 200), 0.5, 3)
    sw, sh = s[2] - s[0], s[3] - s[1]
    for i in range(3):                                      # camera feeds: 3 x 2 tiles
        for j in range(2):
            t = (s[0] + 2 + i * (sw - 4) / 3, s[1] + 2 + j * (sh - 4) / 2)
            box = (t[0] + 0.6, t[1] + 0.6, t[0] + (sw - 4) / 3 - 0.6, t[1] + (sh - 4) / 2 - 0.6)
            a.rect(img, box, (20, 50, 60))
            a.rect(img, (box[0], box[3] - (box[3] - box[1]) * 0.35, box[2], box[3]), (30, 70, 80))
            img = a.text(img, f'CAM {i + 3 * j + 1}', (box[3] - box[1]) * 0.2, (box[0] + 1, box[1] + 0.5,
                         box[2], box[1] + (box[3] - box[1]) * 0.3), CYAN, 'l')
    a.rect(img, (s[0] + sw * 0.69, s[1] + sh * 0.53, s[0] + sw * 0.97, s[1] + sh * 0.97), RED, 0.35)
    img = a.text(img, 'ALERT', sh * 0.12, (s[0] + sw * 0.69, s[1] + sh * 0.6, s[0] + sw * 0.97, s[1] + sh * 0.9), RED)
    for side_x in (w * 0.03, w * 0.82):                     # side readouts
        for k in range(6):
            y = h * 0.15 + k * h * 0.12
            c = RED if (k + int(side_x)) % 3 == 0 else CYAN
            a.rect(img, (side_x, y, side_x + w * 0.15 * (0.5 + 0.1 * (k % 4)), y + h * 0.05), c, 0.8)
    return img


def deck_top(a, w, h):
    img = paint(CASE)(a, w, h)
    for i in range(5):                                      # glowing keys, red and cyan
        for j in range(2):
            x0 = w * (0.08 + i * 0.12)
            y0 = h * (0.35 + j * 0.25)
            c = RED if (i + j) % 2 else CYAN
            box = (x0, y0, x0 + w * 0.09, y0 + h * 0.16)
            a.rect(img, box, tuple(int(v * 0.7) for v in c))
            img = glow(img, a, box, c, 0.3, 1)
    a.rect(img, (w * 0.04, h * 0.1, w * 0.7, h * 0.2), CYAN, 0.9)            # the strip near the monitors
    img = glow(img, a, (w * 0.04, h * 0.1, w * 0.7, h * 0.2), CYAN, 0.3, 2)
    return img


def under_front(a, w, h):
    img = paint(DARK, 0.3)(a, w, h)
    for k in range(4):
        y = h * (0.2 + k * 0.18)
        a.rect(img, (w * 0.08, y, w * 0.92, y + h * 0.03), CYAN)
        img = glow(img, a, (w * 0.08, y, w * 0.92, y + h * 0.03), CYAN, 0.35, 2)
    return img


def ped_front(a, w, h):
    img = paint(CASE)(a, w, h)
    for k in range(9):                                      # drive / module slots with lights
        y = h * (0.08 + k * 0.1)
        a.rect(img, (w * 0.12, y, w * 0.88, y + h * 0.07), (14, 15, 18))
        a.rect(img, (w * 0.72, y + h * 0.02, w * 0.82, y + h * 0.05), RED if k % 3 == 0 else CYAN)
    return img


for p in peds:
    p.paint = {'-z': ped_front, '*': 'case'}
under.paint = {'-z': under_front, '*': 'dark'}
desk.paint = {'*': 'dark', '-z': 'deskedge'}
deckp.paint = {'+y': deck_top, '*': 'case'}
bank.paint = {'-z': bank_front, '+z': 'back', '*': 'case'}
m.swatch('case', paint(CASE))
m.swatch('dark', paint(DARK, 0.3))
m.swatch('inside', paint('101114', 0.2, 1))


def deskedge(a, w, h):
    img = paint(DARK, 0.3)(a, w, h)
    a.rect(img, (0, h * 0.4, w, h * 0.6), CYAN, 0.9)
    return img


m.swatch('deskedge', deskedge)
m.swatch('back', lambda a, w, h: a.label(paint(CASE)(a, w, h), (w * 0.38, h * 0.3, w * 0.62, h * 0.65),
                                         [('SEC-NET 9', 3), ('ALARM CONTROL', 2.4)], 8))
m.swatch('redknob', lambda a, w, h: glow(paint((220, 30, 30), 0.1, 1)(a, w, h), a,
                                         (w * 0.2, h * 0.2, w * 0.8, h * 0.8), (255, 120, 120), 0.3, 2))

if __name__ == '__main__':
    m.build()
