#!/usr/bin/python3
"""m0d3l's ready painters, f(a, w, h) -> image, for m0kit specs. Renders shared from the earlier models."""
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
R = {'red': os.path.join(HERE, 'medkit', 'red.png'), 'alu': os.path.join(HERE, 'medkit', 'alu.png'),
     'rubber': os.path.join(HERE, 'medkit', 'rubber.png'), 'pine': os.path.join(HERE, 'crate', 'pine-a.png'),
     'pine2': os.path.join(HERE, 'crate', 'pine-b.png')}
_cache = {}


def src(a, k):
    if k not in _cache:
        _cache[k] = a.load(R[k], (0, 120) if k == 'rubber' else None)
    return _cache[k]


def hexrgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def paint(rgb, scuffs=0.6, edge=2.5):
    """Painted metal / plastic in rgb (hex or tuple): orange peel, a few scuffs, darker edges."""
    rgb = hexrgb(rgb) if isinstance(rgb, str) else rgb

    def f(a, w, h):
        return a.edge_dark(a.painted(src(a, 'red'), w, h, rgb, 1.3, scuffs), edge, 0.85)
    return f


def steel(rgb=(214, 218, 224)):
    """Brushed steel, scratch lines capped (see SKILL: look at swatches zoomed)."""
    from scipy.ndimage import gaussian_filter1d

    def f(a, w, h):
        st = a.tinted(src(a, 'alu'), w, h, rgb, 0.6)
        sm = gaussian_filter1d(st, 4 * a.K, axis=0)
        return np.clip(st, sm * 0.97, sm * 1.03)
    return f


def rubber(rgb=(56, 56, 59)):
    def f(a, w, h):
        return a.tinted(src(a, 'rubber'), w, h, rgb, 1.0)
    return f


def wood(rgb=None, k='pine'):
    def f(a, w, h):
        img = a.tinted(src(a, k), w, h, rgb, 1.0) if rgb else a.tinted(src(a, k), w, h, (190, 150, 105), 1.0)
        return a.edge_dark(img, 2, 0.8)
    return f


def flat(rgb):
    rgb = hexrgb(rgb) if isinstance(rgb, str) else rgb

    def f(a, w, h):
        return np.ones((a.px(h), a.px(w), 3), np.float32) * np.array(rgb, np.float32)
    return f


def glow(img, a, box, rgb, k=0.5, r=3):
    """A soft glow of rgb round box (x0 y0 x1 y1, layout px) - screens, signs. Keep k <= .25 and
    r <= 2 on panels: more blurs them into fuzzy blobs (the flipped table's inlays)."""
    from scipy.ndimage import gaussian_filter
    m = np.zeros(img.shape[:2], np.float32)
    x0, y0, x1, y1 = [round(v * a.K) for v in box]
    m[max(0, y0):y1, max(0, x0):x1] = 1
    m = gaussian_filter(m, r * a.K)[..., None] * k
    return img * (1 - m) + np.array(rgb, np.float32) * m


def front_px(part, w, h):
    """World (x, y) on a part's -z face -> (px, py) in its front region (w x h layout px).
    From the front +x is on the left, so px grows as x falls."""
    lo, hi = part.box()

    def f(x, y):
        return (hi[0] - x) / (hi[0] - lo[0]) * w, (hi[1] - y) / (hi[1] - lo[1]) * h
    return f


def front_box(part, w, h, x0, x1, y0, y1):
    """A world rect on the -z face -> (px0, py0, px1, py1) in its front region."""
    f = front_px(part, w, h)
    a, b = f(max(x0, x1), max(y0, y1))
    c, d = f(min(x0, x1), min(y0, y1))
    return a, b, c, d
