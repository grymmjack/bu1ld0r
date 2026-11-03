"""The game's coloured barrels as m0kit specs: make(kind, wreck, here).

A steel drum (seg 16) with hoops; lava and poison bulge (a wider middle drum, the steps under
hoops). Each kind has its own looks drawn by code: acid yellow with a radiation sign and a tap,
lava charred staves with orange glowing bands round a green porthole, poison purple with a
cage of ribs and a skull, slime grey steel brimming with green slime running down it, water
teal with a white drop. A wreck is the bottom ~0.25 with a jagged crown of 16 teeth, glowing at
their broken tops, the liquid's surface inside and runs down the outside.

Side pictures: u = 0 is the front's middle (at both edges of the picture), columns to the
viewer's right; `fx` below is the signed distance from the front."""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m0kit import Model  # noqa: E402
from looks import paint, steel  # noqa: E402

KINDS = {   # body, hoop, glow, seed
    'acid': ((200, 172, 34), (74, 78, 64), (236, 232, 40), 161),
    'lava': ((54, 48, 46), (210, 96, 30), (255, 130, 30), 163),
    'poison': ((96, 52, 176), (136, 96, 214), (200, 90, 255), 165),
    'slime': ((96, 102, 98), (62, 66, 64), (100, 236, 60), 167),
    'water': ((34, 150, 172), (62, 72, 80), (90, 226, 244), 169),
}
R_IN, R_OUT, H = 0.148, 0.1635, 0.45


def grid(a, w, h):
    yy, xx = np.mgrid[0:a.px(h), 0:a.px(w)] / a.K
    fx = np.where(xx < w / 2, xx, xx - w)
    return xx, yy, fx


def body_tex(kind, a, w, h, cols=16):
    body, hoop, glow, _ = KINDS[kind]
    r = np.random.default_rng(len(kind) * 7 + int(w))
    img = paint(body, 0.6)(a, w, h)
    xx, yy, fx = grid(a, w, h)
    cw = w / cols
    shade = 0.9 + 0.2 * r.random(cols)                                 # each face a touch different
    img *= shade[np.minimum((xx / cw).astype(int), cols - 1)][..., None]
    if kind == 'lava':                                                 # charred staves
        for k in range(cols + 1):
            img[np.abs(xx - k * cw) < 0.6] = (24, 20, 20)
        for k in range(cols):                                          # glowing cracks
            if r.random() < 0.5:
                x0, y0 = k * cw + r.uniform(2, cw - 2), r.uniform(0, h)
                ln = r.uniform(4, 12)
                m = (np.abs(xx - x0 - (yy - y0) * 0.15) < 0.45) & (yy > y0) & (yy < y0 + ln)
                img[m] = glow
    elif kind == 'poison':                                             # the cage's ribs
        for k in range(cols):
            m = np.abs(xx - (k + 0.5) * cw) < 1.2
            img[m] = img[m] * 0.4 + np.array((150, 110, 230)) * 0.6
            img[np.abs(xx - (k + 0.5) * cw - 1.2) < 0.35] = (60, 30, 110)
    else:                                                              # steel streaks
        for k in range(int(w * 0.12)):
            x0 = r.uniform(0, w)
            m = (np.abs(xx - x0) < 0.3) & (yy > r.uniform(0, h * 0.5))
            img[m] *= 0.94
    return img


def drips(img, a, xx, yy, w, h, rgb, n, top=0.0, seed=1):
    r = np.random.default_rng(seed)
    for _ in range(n):
        x0, wd = r.uniform(0, w), r.uniform(0.8, 2.2)
        ln = r.uniform(h * 0.1, h * 0.6)
        m = (np.abs(xx - x0) < wd / 2) & (yy >= top) & (yy < top + ln)
        img[m] = rgb
        img[(np.hypot(xx - x0, yy - top - ln) < wd * 0.7)] = rgb        # a drop at the end
    return img


def emblem(kind, a, img, xx, yy, fx, cy, s):
    """The front's sign, centred on the front at height cy, s across."""
    body, hoop, glow, _ = KINDS[kind]
    d = np.hypot(fx, yy - cy)
    ang = np.arctan2(yy - cy, fx)
    if kind == 'acid':                                                 # radiation in a black ring
        img[d < s * 0.5] = (24, 24, 22)
        img[d < s * 0.42] = body
        blade = (np.mod(ang + np.pi / 2, 2 * np.pi / 3) < np.pi / 3) & (d > s * 0.1) & (d < s * 0.36)
        img[blade | (d < s * 0.07)] = (24, 24, 22)
    elif kind == 'lava':                                               # the porthole
        img[d < s * 0.5] = hoop
        img[d < s * 0.42] = (30, 26, 26)
        img[d < s * 0.34] = (40, 200, 110)
        img[d < s * 0.2] = (160, 255, 190)
        for t in np.linspace(0, 2 * np.pi, 8, endpoint=False):         # rivets
            img[np.hypot(fx - np.cos(t) * s * 0.46, yy - cy - np.sin(t) * s * 0.46) < 0.7] = (60, 30, 20)
    elif kind == 'poison':                                             # a skull
        sk = (196, 170, 236)
        img[np.hypot(fx / 1.0, (yy - cy + s * 0.08) / 0.95) < s * 0.36] = sk
        img[(np.abs(fx) < s * 0.22) & (yy > cy + s * 0.12) & (yy < cy + s * 0.42)] = sk
        for e in (-1, 1):
            img[np.hypot(fx - e * s * 0.15, yy - cy + s * 0.05) < s * 0.1] = (40, 16, 70)
        img[(np.abs(fx) < s * 0.05 * (1 - (yy - cy - s * 0.1) / (s * 0.12))) & (yy > cy + s * 0.04) & (yy < cy + s * 0.16)] = (40, 16, 70)
        for k in range(-2, 3):
            img[(np.abs(fx - k * s * 0.08) < 0.3) & (yy > cy + s * 0.28) & (yy < cy + s * 0.42)] = (90, 60, 140)
    elif kind == 'slime':                                              # a red biohazard label
        m = (np.abs(fx) < s * 0.36) & (np.abs(yy - cy) < s * 0.36)
        img[m] = (190, 34, 34)
        for t in (0, 2 * np.pi / 3, 4 * np.pi / 3):
            img[np.hypot(fx - np.cos(t - np.pi / 2) * s * 0.12, yy - cy - np.sin(t - np.pi / 2) * s * 0.12) < s * 0.12] = (240, 220, 220)
        img[d < s * 0.06] = (190, 34, 34)
    elif kind == 'water':                                              # a white drop
        drop = (np.hypot(fx, yy - cy - s * 0.12) < s * 0.22) | \
               ((yy < cy + s * 0.12) & (yy > cy - s * 0.38) & (np.abs(fx) < (yy - cy + s * 0.38) * 0.45))
        img[drop] = (236, 244, 246)
    return img


def side_painter(kind, part, y0, y1, wreck):
    """The side picture of one drum piece spanning y0..y1 of the barrel."""
    def f(a, w, h):
        img = body_tex(kind, a, w, h)
        xx, yy, fx = grid(a, w, h)
        body, hoop, glow, _ = KINDS[kind]
        k = h / (y1 - y0)                                              # layout px a cell (up)
        es = (0.13 if kind != 'poison' else 0.17) * k                  # the emblem's size, middle
        ey = (y1 - 0.225) * k
        if wreck:
            es, ey = (0.12 if part == 'mid' else 0.13) * k, (y1 - (0.175 if part == 'mid' else 0.14)) * k
        if part == 'mid' or part == 'drum':
            img = emblem(kind, a, img, xx, yy, fx, ey, es)
            if kind == 'lava':                                         # glowing bands
                for yb in (0.09, 0.4):
                    if y0 < yb < y1:
                        img[np.abs(yy - (y1 - yb) * k) < 0.8] = glow
            if kind == 'water' and not wreck:                          # a scratch
                img[(np.abs(fx - 18 - (yy - 8) * 0.6) < 0.5) & (yy > 8) & (yy < 22)] = (200, 230, 236)
        if kind == 'slime' and part in ('mid', 'drum', 'top'):
            img = drips(img, a, xx, yy, w, h, (90, 220, 50), 22, 0, seed=7 + len(part))
        if wreck:
            img = drips(img, a, xx, yy, w, h, glow, 14, 0, seed=11)
        return a.edge_dark(img, 1.5, 0.75)
    return f


def lid_painter(kind):
    def f(a, w, h):
        body, hoop, glow, _ = KINDS[kind]
        yy, xx = np.mgrid[0:a.px(h), 0:a.px(w)] / a.K
        d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
        if kind == 'slime':                                            # brimming over
            img = paint((80, 210, 50), 0.2, 1)(a, w, h)
            r = np.random.default_rng(3)
            for _ in range(14):
                cx, cy, rr = r.uniform(0, w), r.uniform(0, h), r.uniform(1, 3)
                img[np.hypot(xx - cx, yy - cy) < rr] = (150, 255, 110)
            img[d > 0.9] = (62, 66, 64)
            return img
        img = paint(body if kind != 'lava' else (60, 50, 46), 0.4)(a, w, h)
        if kind == 'lava':
            for k in range(-4, 5):
                img[np.abs(xx - w / 2 - k * w / 9) < 0.5] = (24, 20, 20)
        img[(d > 0.86) & (d < 0.94)] = hoop                             # the rim
        img[np.hypot(xx - w * 0.68, yy - h * 0.36) < w * 0.07] = tuple(int(v * 0.6) for v in hoop)   # the bung
        img[np.hypot(xx - w * 0.68, yy - h * 0.36) < w * 0.035] = (30, 30, 30)
        return img
    return f


def liquid_painter(kind):
    def f(a, w, h):
        body, hoop, glow, _ = KINDS[kind]
        yy, xx = np.mgrid[0:a.px(h), 0:a.px(w)] / a.K
        d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
        img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array(glow, np.float32) * 0.8
        r = np.random.default_rng(5)
        for _ in range(12):
            cx, cy, rr = r.uniform(0, w), r.uniform(0, h), r.uniform(1, 3.5)
            img[np.hypot(xx - cx, yy - cy) < rr] = [min(255, v * 1.15 + 30) for v in glow]
        img[d > 0.93] = (30, 30, 30)
        return img
    return f


def make(kind, wreck, here):
    body, hoop, glow, seed = KINDS[kind]
    name = f'barrel-{kind}' + ('-wreck' if wreck else '')
    m = Model(name, here, seed=seed + (50 if wreck else 0))
    m.material('main', 'paint')
    top = 0.25 if wreck else H
    hx = '%02X%02X%02X' % hoop
    bx = '%02X%02X%02X' % body
    capkey = 'liquid' if wreck else 'lid'
    if kind in ('lava', 'poison'):                                     # bulging: three drums
        pieces = [('low', 0, 0.1, R_IN), ('mid', 0.1, min(0.35, top), R_OUT)]
        if not wreck:
            pieces.append(('top', 0.35, H, R_IN))
    else:
        pieces = [('drum', 0, top, R_OUT - 0.004)]
    for i, (pn, y0, y1, rad) in enumerate(pieces):
        last = i == len(pieces) - 1
        m.cyl(pn, (0, y0, 0), (rad * 2, y1 - y0, rad * 2), bx, seg=16,
              paint={'side': side_painter(kind, pn, y0, y1, wreck),
                     'top': capkey if last else 'hoopc', 'bottom': 'bottom' if i == 0 else 'hoopc'})
    bulge = kind in ('lava', 'poison')
    rims = [0.024, 0.1, 0.35, H - 0.024] if bulge else [0.024, 0.15, 0.3, H - 0.024]   # hoop middles
    if wreck:
        rims = [0.024, 0.1] if bulge else [0.024]
    for j, y in enumerate(rims):
        if y + 0.01 > top - 0.004:
            continue
        rad = (R_OUT if (bulge and j in (1, 2)) else (R_IN if bulge else R_OUT - 0.004)) + 0.006
        m.cyl(f'hoop-{j}', (0, y - 0.01, 0), (rad * 2, 0.02, rad * 2),
              hx, seg=16, paint={'side': 'hoop', 'top': 'hoopc', 'bottom': 'hoopc'})
    if kind == 'acid':                                                 # the tap
        m.cyl('tap', (0.09, 0.05, -0.135), (0.026, 0.045, 0.026), '3A3C40', seg=8, rot=(-90, 0, 0),
              paint={'*': 'tap', '-z': 'tapend'})
        m.swatch('tap', steel((120, 124, 130)))
        m.swatch('tapend', paint((24, 24, 26), 0.2))
    if wreck:                                                          # the jagged crown
        r = np.random.default_rng(seed)
        rad = (R_OUT if kind in ('lava', 'poison') else R_OUT - 0.004)
        ap = rad * math.cos(math.pi / 16)
        for k in range(16):
            a = 11.25 + k * 22.5
            th = 0.012
            Rk = ap - th / 2
            pick = r.random()                                          # torn: some stubs, some spikes
            hk = 0.008 if pick < 0.25 else float(r.uniform(0.02, 0.05)) if pick < 0.6 else float(r.uniform(0.05, 0.09))
            m.box(f'tooth-{k}', (round(Rk * math.sin(math.radians(a)), 4), top, round(Rk * math.cos(math.radians(a)), 4)),
                  (round(2 * rad * math.sin(math.pi / 16) + 0.004, 4), round(hk, 4), th), bx,
                  paint={'+y': 'toothtop', '*': 'tooth'}, rot=(0, a, 0))
        m.swatch('tooth', lambda a_, w, h: drips(paint(body, 0.6)(a_, w, h), a_, *grid(a_, w, h)[:2], w, h, glow, 3, 0, seed=4))
        m.swatch('toothtop', lambda a_, w, h: paint(glow, 0.1, 1)(a_, w, h))
        m.swatch('liquid', liquid_painter(kind))
    else:
        m.swatch('lid', lid_painter(kind))
    m.swatch('hoop', lambda a_, w, h: a_.edge_dark(paint(hoop, 0.5)(a_, w, h), 1, 0.7))
    m.swatch('hoopc', paint(hoop, 0.4))
    m.swatch('bottom', paint(tuple(int(v * 0.6) for v in body), 0.3))
    return m
