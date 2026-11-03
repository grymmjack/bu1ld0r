"""NEON-CASTER's turret as m0kit specs: make(which, here) - 'base', 'head', 'whole', 'mount',
'mount-broken'.

As its painting: a grey tripod on a pedestal with a hazard collar (the base, 0.17 high: the head
turns on its top - the game's turPivot is the base's highest point); the head a yellow and black
armoured box with a big lens in front, red light pods either side, two barrels pointing forward
(-z) in shrouds, a sensor stack on top with two red eyes. The barrels' ends are textured from the
picture's white corner (u, v > .95): the game colours them by the turret's weapon and finds its
muzzles by them (RENDER/MODELS.BM). The head's own file starts at its pivot (y 0); the whole
turret is the two together. The mount is the hex plate it's bolted on (0.36 across); broken, a
charred hole blown through it, wires torn out."""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m0kit import Model  # noqa: E402
from looks import paint, steel, rubber, glow  # noqa: E402

YEL, BLK, GREY, DGREY, RED = (232, 186, 30), (30, 30, 32), (128, 134, 142), (64, 68, 76), (255, 40, 40)
BASE_H = 0.17


def hazard(a, w, h, k=5.0, angle=1):
    img = paint(YEL, 0.5)(a, w, h)
    yy, xx = np.mgrid[0:a.px(h), 0:a.px(w)] / a.K
    img[((xx + angle * yy) / k).astype(int) % 2 == 0] = BLK
    return img


def add_base(m):
    for i, ang in enumerate((0, 120, 240)):                            # the tripod
        s, c = math.sin(math.radians(ang)), math.cos(math.radians(ang))
        m.box(f'leg-{i}', (round(0.1 * s, 4), 0.02, round(0.1 * c, 4)), (0.045, 0.035, 0.2), '80868E',
              paint={'+y': 'legtop', '*': 'grey'}, rot=(0, ang, 0))
        m.box(f'pad-{i}', (round(0.19 * s, 4), 0, round(0.19 * c, 4)), (0.075, 0.025, 0.075), '1E1E20',
              paint='rubber', rot=(0, ang, 0))
    m.cyl('hub', (0, 0.0, 0), (0.15, 0.07, 0.15), '40444C', seg=8,
          paint={'side': 'hubside', 'top': 'dgrey', 'bottom': 'dgrey'})
    m.cyl('pedestal', (0, 0.07, 0), (0.09, 0.07, 0.09), '80868E', seg=8,
          paint={'side': 'pedestal', 'top': 'dgrey', 'bottom': 'dgrey'})
    m.cyl('collar', (0, 0.14, 0), (0.15, 0.03, 0.15), 'E8BA1E', seg=8,
          paint={'side': 'collar', 'top': 'collartop', 'bottom': 'dgrey'})


def add_head(m, y0):
    m.corner = (255, 255, 255)                                         # the muzzles' white corner
    m.cyl('neck', (0, y0, 0), (0.1, 0.04, 0.1), '40444C', seg=8, paint={'side': 'dgrey', 'top': 'dgrey', 'bottom': 'dgrey'})
    body = m.box('body', (0, y0 + 0.04, 0), (0.26, 0.18, 0.2), 'E8BA1E')
    lens = m.cyl('lens', (0, y0 + 0.15, -0.1), (0.13, 0.035, 0.13), '50545C', seg=12, rot=(-90, 0, 0))
    lens.paint = {'-z': 'eye', '*': 'grey'}
    for i, x in enumerate((0.15, -0.15)):
        pod = m.box(f'pod-{i}', (x, y0 + 0.07, 0), (0.04, 0.13, 0.12), '50545C')
        pod.paint = {('+x' if x > 0 else '-x'): 'podlights', '*': 'grey'}
        m.cyl(f'shroud-{i}', (x * 0.7, y0 + 0.08, -0.1), (0.075, 0.05, 0.075), '40444C', seg=8, rot=(-90, 0, 0),
              paint={'*': 'shroud'})
        m.cyl(f'barrel-{i}', (x * 0.7, y0 + 0.08, -0.15), (0.05, 0.08, 0.05), '6A707A', seg=8, rot=(-90, 0, 0),
              paint={'-z': 'CORNER', '*': 'gun'})
    m.box('sensor', (0, y0 + 0.22, 0.01), (0.11, 0.08, 0.1), '1E1E20', paint={'*': 'sensor', '+y': 'dgrey'})
    stalk = m.box('stalk', (0, y0 + 0.3, 0.0), (0.09, 0.058, 0.06), '1E1E20')
    stalk.paint = {'-z': 'eyes', '*': 'black'}
    body.paint = {'-z': body_front, '+z': body_back, '+x': 'bodyside', '-x': 'bodyside', '+y': 'bodytop', '-y': 'dgrey'}


def body_front(a, w, h):
    img = paint(YEL, 0.6)(a, w, h)
    a.rect(img, (0, h * 0.86, w, h), BLK)
    for u in (0.05, 0.92):                                             # black side strips
        a.rect(img, (w * u, 0, w * u + w * 0.03, h * 0.86), BLK)
    a.rect(img, (w * 0.1, h * 0.08, w * 0.35, h * 0.14), (60, 60, 64))  # vents
    a.rect(img, (w * 0.65, h * 0.08, w * 0.9, h * 0.14), (60, 60, 64))
    return a.edge_dark(img, 2, 0.7)


def body_back(a, w, h):
    img = hazard(a, w, h)
    a.rect(img, (w * 0.2, h * 0.25, w * 0.8, h * 0.75), DGREY)          # a hatch
    a.rect(img, (w * 0.24, h * 0.3, w * 0.76, h * 0.7), (84, 88, 96))
    return a.edge_dark(img, 2, 0.7)


def body_side(a, w, h):
    img = paint(YEL, 0.6)(a, w, h)
    yy, xx = np.mgrid[0:a.px(h), 0:a.px(w)] / a.K
    band = (yy > h * 0.6) & (yy < h * 0.85)
    img[band & (((xx + yy) / 4).astype(int) % 2 == 0)] = BLK
    a.rect(img, (w * 0.15, h * 0.12, w * 0.85, h * 0.16), (150, 116, 20))
    return a.edge_dark(img, 2, 0.7)


def eye(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array(GREY, np.float32)
    yy, xx = np.mgrid[0:a.px(h), 0:a.px(w)] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2) / (min(w, h) / 2)
    img[d < 0.86] = (40, 44, 52)
    img[d < 0.7] = (20, 60, 110)
    img[d < 0.45] = (70, 170, 240)
    img[np.hypot(xx - w * 0.4, yy - h * 0.38) < w * 0.07] = (230, 250, 255)
    return img


def pod_lights(a, w, h):
    img = paint(DGREY, 0.4)(a, w, h)
    for k in range(3):
        y = h * (0.12 + k * 0.28)
        a.rect(img, (w * 0.25, y, w * 0.75, y + h * 0.18), RED)
        img = glow(img, a, (w * 0.25, y, w * 0.75, y + h * 0.18), (255, 120, 100), 0.2, 1)
    return img


def eyes(a, w, h):
    img = paint(BLK, 0.3)(a, w, h)
    for u in (0.3, 0.7):
        cx, cy = w * u, h * 0.45
        a.rect(img, (cx - w * 0.1, cy - h * 0.18, cx + w * 0.1, cy + h * 0.18), RED)
        img = glow(img, a, (cx - w * 0.12, cy - h * 0.2, cx + w * 0.12, cy + h * 0.2), (255, 140, 120), 0.25, 1)
    return img


def sensor(a, w, h):
    img = paint(BLK, 0.3)(a, w, h)
    a.rect(img, (0, h * 0.35, w, h * 0.65), YEL)
    return img


def banded(rgb, band, n):
    def f(a, w, h):
        img = paint(rgb, 0.4)(a, w, h)
        for k in range(n):
            v = h * (k + 0.5) / n
            a.rect(img, (0, v - 0.6, w, v + 0.6), band)
        return img
    return f


def mount_top(broken):
    def f(a, w, h):
        img = steel((88, 92, 104))(a, w, h)
        yy, xx = np.mgrid[0:a.px(h), 0:a.px(w)] / a.K
        cx, cy = w / 2, h / 2
        band = np.abs(yy - cy) < h * 0.06                              # the hazard stripe
        img[band] = YEL
        img[band & (((xx) / 4).astype(int) % 2 == 0)] = BLK
        for k in range(6):                                             # the bolts
            t = k * math.pi / 3 + math.pi / 6
            q = min(w, h)
            bx, by = cx + q * 0.36 * math.cos(t), cy + q * 0.36 * math.sin(t)
            img[np.hypot(xx - bx, yy - by) < q * 0.035] = (170, 175, 185)
            img[np.hypot(xx - bx, yy - by) < q * 0.015] = (60, 62, 68)
        if broken:                                                     # blown open: a charred ragged hole
            r = np.random.default_rng(9)
            ang = np.arctan2(yy - cy, xx - cx)
            rad = min(w, h) * (0.22 + 0.06 * np.sin(ang * 5 + 1) + 0.03 * np.sin(ang * 11))
            d = np.hypot(xx - cx, yy - cy)
            img[d < rad * 1.35] = img[d < rad * 1.35] * 0.45 + np.array((40, 24, 14)) * 0.55   # scorched
            img[d < rad] = (14, 10, 9)
            img[(d > rad * 0.92) & (d < rad)] = (120, 50, 14)          # glowing torn edge
        return img
    return f


def make(which, here):
    names = {'base': 'turret-base', 'head': 'turret-head', 'whole': 'turret',
             'mount': 'turret-mount', 'mount-broken': 'turret-mount-broken'}
    m = Model(names[which], here, seed=171 + list(names).index(which))
    m.material('main', 'paint')
    if which in ('base', 'whole'):
        add_base(m)
    if which in ('head', 'whole'):
        add_head(m, BASE_H if which == 'whole' else 0.0)
    if which.startswith('mount'):
        broken = which == 'mount-broken'
        m.cyl('plate', (0, 0, 0), (0.36, 0.03, 0.36), '585C68', seg=6, rot=(0, 90, 0),  # (corners at +-z, as the game's)
              paint={'+y': 'platetop', '*': 'edge'})
        m.swatch('platetop', mount_top(broken))
        m.swatch('edge', paint((55, 58, 66), 0.3))
        if broken:
            m.cyl('pit', (0, -0.05, 0), (0.12, 0.05, 0.12), '181210', seg=8,
                  paint={'side': 'char', 'top': 'char', 'bottom': 'char'})
            m.swatch('char', paint((30, 22, 18), 0.4, 1))
            r = np.random.default_rng(7)
            for k, col in enumerate(('DC2828', 'F0D228', '3278FF', '1E1E1E')):
                a = float(r.uniform(0, 360))
                lean = float(r.uniform(18, 40))
                hgt = float(r.uniform(0.06, 0.1))
                m.box(f'wire-{k}', (round(0.02 * math.cos(math.radians(a)), 4), 0.0, round(0.02 * math.sin(math.radians(a)), 4)),
                      (0.008, round(hgt, 3), 0.008), col, paint=f'wire{k}', rot=(round(lean, 1), round(a, 1), 0))
                m.swatch(f'wire{k}', paint(tuple(int(col[i:i + 2], 16) for i in (0, 2, 4)), 0.2, 1))
    m.swatch('grey', paint(GREY, 0.5))
    m.swatch('dgrey', paint(DGREY, 0.4))
    m.swatch('black', paint(BLK, 0.3))
    m.swatch('rubber', rubber((30, 30, 32)))
    m.swatch('legtop', lambda a, w, h: a.edge_dark(steel((150, 156, 164))(a, w, h), 1, 0.7))
    m.swatch('hubside', banded(DGREY, (40, 42, 48), 2))
    m.swatch('pedestal', banded(GREY, (90, 94, 100), 3))
    m.swatch('collar', lambda a, w, h: hazard(a, w, h, 3.0))
    m.swatch('collartop', paint(YEL, 0.5))
    m.swatch('bodyside', body_side)
    m.swatch('bodytop', lambda a, w, h: a.edge_dark(paint(YEL, 0.6)(a, w, h), 2, 0.7))
    m.swatch('eye', eye)
    m.swatch('podlights', pod_lights)
    m.swatch('shroud', paint((50, 52, 58), 0.4))
    m.swatch('gun', steel((110, 116, 126)))
    m.swatch('sensor', sensor)
    m.swatch('eyes', eyes)
    return m
