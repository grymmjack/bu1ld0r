#!/usr/bin/python3
"""c0-terminal-broken: a wrecked CRT terminal - dark scorched case, carry handle, the screen
cracked and glitching pink / cyan, its keyboard lying in front. The game's is 0.46 x 0.46 x 0.27."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow, front_box  # noqa: E402

CASE, PINK, CYAN = '23252A', (255, 60, 170), (60, 230, 255)
m = Model('terminal-broken', HERE, seed=13)
m.material('main', 'paint')
stand = m.box('stand', (0, 0, 0.05), (0.28, 0.05, 0.16), '1A1B1E', paint='scorch')
body = m.box('body', (0, 0.05, 0.05), (0.40, 0.33, 0.18), CASE, walls='bezel')
body.cut('-z', (-0.14, 0.14, 0.12, 0.33), 0.03)
for i, x in enumerate((0.15, -0.15)):
    m.box(f'post-{i}', (x, 0.38, 0.05), (0.02, 0.045, 0.02), 'A0A4AA', paint='steel')
m.box('handle', (0, 0.425, 0.05), (0.33, 0.02, 0.022), 'A0A4AA', paint='steel')
kb = m.box('keyboard', (0.02, 0, -0.10), (0.36, 0.024, 0.10), '1C1D20', paint='kbside')


def screen(a, img, box):
    x0, y0, x1, y1 = box
    r = a.rng
    a.rect(img, box, (10, 14, 24))
    img = glow(img, a, (x0 + 2, y0 + 2, x1 - 2, y1 - 2), (30, 90, 120), 0.6, 4)
    for _ in range(14):                                     # glitch bars
        yy = r.uniform(y0, y1 - 2)
        xx = r.uniform(x0, x1 - 10)
        c = PINK if r.random() < 0.5 else CYAN
        a.rect(img, (xx, yy, min(x1, xx + r.uniform(6, 30)), yy + r.uniform(0.5, 2)), c, 0.8)
    img = a.text(img, 'ERR 0x7F  CORE DUMP', (y1 - y0) * 0.1, (x0 + 3, y0 + 3, x1 - 3, y0 + (y1 - y0) * 0.2), CYAN, 'l')
    img = a.text(img, 'SIGNAL LOST', (y1 - y0) * 0.14, (x0, y0 + (y1 - y0) * 0.42, x1, y0 + (y1 - y0) * 0.62), PINK)
    cx, cy = x0 + (x1 - x0) * 0.68, y0 + (y1 - y0) * 0.35        # the crack: a star of jagged lines
    for k in range(9):
        ang = r.uniform(0, 2 * np.pi)
        px, py = cx, cy
        for s in range(int(r.integers(8, 22))):
            ang += r.uniform(-0.5, 0.5)
            nx, ny = px + np.cos(ang) * 1.5, py + np.sin(ang) * 1.5
            if not (x0 < nx < x1 and y0 < ny < y1):
                break
            a.rect(img, (min(px, nx), min(py, ny), max(px, nx) + 0.4, max(py, ny) + 0.4), (230, 240, 255), 0.75)
            px, py = nx, ny
    a.rect(img, (cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5), (240, 245, 255), 0.6)
    return img


def scorched(a, img, n=6):
    h, w = img.shape[0] / a.K, img.shape[1] / a.K
    r = a.rng
    from scipy.ndimage import gaussian_filter
    m_ = np.zeros(img.shape[:2], np.float32)
    for _ in range(n):
        x, y = int(r.uniform(0, w) * a.K), int(r.uniform(0, h) * a.K)
        m_[max(0, y - 2):y + 2, max(0, x - 2):x + 2] = 1
    m_ = np.clip(gaussian_filter(m_, 6 * a.K) * 30, 0, 0.75)[..., None]
    return img * (1 - m_) + np.array((8, 6, 6), np.float32) * m_


def front(a, w, h):
    img = paint(CASE, 1.5)(a, w, h)
    s = front_box(body, w, h, -0.14, 0.14, 0.12, 0.33)
    a.rect(img, (s[0] - 2, s[1] - 2, s[2] + 2, s[3] + 2), (14, 14, 16))
    img = glow(img, a, (s[0] - 2, s[1] - 2, s[2] + 2, s[3] + 2), PINK, 0.2, 2)
    img = screen(a, img, s)
    img = a.text(img, 'VT-220', h * 0.06, (w * 0.06, h * 0.86, w * 0.4, h * 0.95), (120, 120, 126), 'l')
    a.rect(img, (w * 0.86, h * 0.88, w * 0.9, h * 0.92), (255, 120, 40))   # a power lamp, stuck on
    return scorched(a, img, 4)


def side(a, w, h):
    img = paint(CASE, 1.5)(a, w, h)
    for i in range(10):
        y = h * 0.2 + i * h * 0.05
        a.rect(img, (w * 0.25, y, w * 0.75, y + h * 0.02), (8, 8, 10))
    r = a.rng
    for k in range(3):                                      # a cable torn out, hanging
        x = w * (0.55 + k * 0.1)
        for t in np.arange(h * 0.6, h, 0.5):
            x += r.uniform(-0.4, 0.4)
            a.rect(img, (x, t, x + 1.2, t + 0.5), [(200, 40, 140), (40, 160, 220), (220, 200, 40)][k])
    return scorched(a, img, 3)


def keys(a, w, h):
    img = paint('1C1D20', 0.2, 1)(a, w, h)
    cols, rows = 14, 4
    kw, kh = w / cols, h / rows
    r = a.rng
    for rr in range(rows):
        for c in range(cols):
            if r.random() < 0.08:
                continue                                    # keys knocked off
            x0, y0 = c * kw + kw * 0.12, rr * kh + kh * 0.14
            a.rect(img, (x0, y0, x0 + kw * 0.76, y0 + kh * 0.72), (54, 56, 62))
            a.rect(img, (x0, y0, x0 + kw * 0.76, y0 + kh * 0.18), (90, 92, 100))
    return img


body.paint = {'-z': front, '+z': 'back', '+x': side, '-x': side, '+y': 'case', '-y': 'case'}
kb.paint = {'+y': keys, '*': 'kbside'}
m.swatch('case', lambda a, w, h: scorched(a, paint(CASE, 1.5)(a, w, h), 2))
m.swatch('back', lambda a, w, h: scorched(a, paint(CASE, 1.5)(a, w, h), 5))
m.swatch('scorch', lambda a, w, h: scorched(a, paint('1A1B1E', 1)(a, w, h), 3))
m.swatch('bezel', paint('121214', 0.3, 1))
m.swatch('kbside', paint('1C1D20', 0.3, 1))
m.swatch('steel', steel((170, 174, 180)))

if __name__ == '__main__':
    m.build()
