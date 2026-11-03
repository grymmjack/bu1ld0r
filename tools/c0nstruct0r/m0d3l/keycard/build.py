#!/usr/bin/python3
"""c0-keycard: an access card standing on edge - one model the game tints three ways (red, blue,
yellow: colour x brightness), so it's drawn in greys: a light card, a dark chip, a clip slot, a
stripe and a printed code. The game's is 0.10 x 0.15 x 0.01 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint  # noqa: E402

m = Model('keycard', HERE, seed=139)
m.material('main', 'plastic')
card = m.box('card', (0, 0, 0), (0.1, 0.15, 0.008), 'E6E6E6')
m.box('clip', (0, 0.15, 0), (0.03, 0.012, 0.01), '505050', paint='clip')


def front(a, w, h):
    img = paint((236, 236, 236), 0.2, 1.5)(a, w, h)
    a.rect(img, (w * 0.35, h * 0.06, w * 0.65, h * 0.12), (60, 60, 60))      # the clip slot
    a.rect(img, (w * 0.12, h * 0.25, w * 0.42, h * 0.45), (120, 120, 120))   # the chip
    for k in range(3):
        a.rect(img, (w * 0.12, h * (0.29 + k * 0.05), w * 0.42, h * (0.29 + k * 0.05) + 0.5), (70, 70, 70))
    a.rect(img, (w * 0.27, h * 0.25, w * 0.28, h * 0.45), (70, 70, 70))
    a.rect(img, (0, h * 0.62, w, h * 0.72), (150, 150, 150))                 # the stripe
    img = a.text(img, 'ACCESS', h * 0.07, (w * 0.1, h * 0.78, w * 0.9, h * 0.88), (90, 90, 90))
    a.rect(img, (w * 0.62, h * 0.28, w * 0.86, h * 0.42), (250, 250, 250))   # a bright square
    return img


def back(a, w, h):
    img = paint((220, 220, 220), 0.2, 1.5)(a, w, h)
    a.rect(img, (0, h * 0.2, w, h * 0.34), (40, 40, 40))                     # the magnetic strip
    return img


card.paint = {'-z': front, '+z': back, '*': 'edge'}
m.swatch('edge', paint((200, 200, 200), 0.2))
m.swatch('clip', paint((80, 80, 80), 0.2))

if __name__ == '__main__':
    m.build()
