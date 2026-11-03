#!/usr/bin/python3
"""c0-ammo: three cyan energy cells side by side - glowing cores behind dark bands, steel caps with
a contact. The game's is 0.10 x 0.11 x 0.05 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow  # noqa: E402

CYAN = (60, 220, 240)
m = Model('ammo', HERE, seed=111)
m.material('main', 'plastic')
for i, x in enumerate((0.033, 0, -0.033)):
    m.cyl(f'cell-{i}', (x, 0.008, 0), (0.032, 0.095, 0.032), '3CDCF0', seg=8, paint={'side': 'cell', 'top': 'cap', 'bottom': 'cap'})
    m.cyl(f'top-{i}', (x, 0.103, 0), (0.03, 0.01, 0.03), 'B0B6BE', seg=8, paint={'side': 'steel', 'top': 'contact', 'bottom': 'steel'})
    m.cyl(f'foot-{i}', (x, 0, 0), (0.03, 0.008, 0.03), 'B0B6BE', seg=8, paint={'side': 'steel', 'top': 'steel', 'bottom': 'steel'})


def cell(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array(CYAN, np.float32)
    H = img.shape[0]
    v = (np.arange(H) / a.K / h)[:, None, None]
    img = img * (0.8 + 0.3 * np.sin(v * np.pi))                        # brighter in the middle
    for y in (h * 0.12, h * 0.85):
        a.rect(img, (0, y, w, y + h * 0.05), (20, 40, 50))
    for k in range(8):                                                 # a highlight per facet
        a.rect(img, (k * w / 8 + w / 40, h * 0.2, k * w / 8 + w / 20, h * 0.8), (220, 255, 255), 0.5)
    return glow(np.clip(img, 0, 255).astype(np.float32), a, (0, h * 0.2, w, h * 0.8), (180, 250, 255), 0.15, 1)


def contact(a, w, h):
    img = steel((180, 186, 194))(a, w, h)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    img[np.hypot(xx - w / 2, yy - h / 2) < w * 0.22] = (230, 200, 120)
    return img


m.swatch('cell', cell)
m.swatch('cap', paint((40, 60, 70), 0.2))
m.swatch('steel', steel((176, 182, 190)))
m.swatch('contact', contact)

if __name__ == '__main__':
    m.build()
