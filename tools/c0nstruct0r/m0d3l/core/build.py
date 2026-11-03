#!/usr/bin/python3
"""c0-core: a power core - a cyan crystal cut as a gem (a point below, a small table above), facets
lit from inside, held in a silver collar at its girdle. The game's is 0.16 x 0.23 x 0.16 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import steel, glow  # noqa: E402

CYAN = (60, 210, 250)
m = Model('core', HERE, seed=99)
m.material('main', '0:27:73:20:0:0:47:0')
m.cyl('crystal', (0, 0, 0), (0.158, 0.23, 0.158), '3CD2FA', seg=6, amt=0.25, kind='diamond',
      paint={'side': 'crystal', 'top': 'table', 'bottom': 'table'})
m.cyl('collar', (0, 0.136, 0), (0.172, 0.014, 0.172), 'C0C6CE', seg=6, paint={'side': 'silver', 'top': 'silver', 'bottom': 'silver'})


def crystal(a, w, h):
    H, W = int(a.px(h)), int(a.px(w))
    yy, xx = np.mgrid[0:H, 0:W] / a.K
    v = yy / h
    col = w / 6
    u = (xx % col) / col
    shade = 0.75 + 0.35 * np.abs(u - 0.5) * 2                          # each facet lighter at its edges
    base = np.array((12, 70, 130)) * (1 - v[..., None]) + np.array((40, 170, 230)) * v[..., None]
    img = base * shade[..., None]
    return glow(np.clip(img, 0, 255).astype(np.float32), a, (0, h * 0.3, w, h * 0.8), (160, 240, 255), 0.18, 2)


def table(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((180, 240, 255), np.float32)
    return glow(img, a, (w * 0.3, h * 0.3, w * 0.7, h * 0.7), (255, 255, 255), 0.4, 1)


m.swatch('crystal', crystal)
m.swatch('table', table)
m.swatch('silver', lambda a, w, h: a.edge_dark(steel((205, 210, 218))(a, w, h), 0.8, 0.7))

if __name__ == '__main__':
    m.build()
