#!/usr/bin/python3
"""c0-pickup-scatter: the scatter gun lying in wait, leaning muzzle up to -x as its painting -
an orange stock and barrel, a dark receiver with a grey sight rail, an orange pump under the
barrel, a wooden grip. Each piece is laid out along the gun (s from the butt, n up from its
underside) and turned by the lean. The game's is 0.45 x 0.39 x 0.06 cells."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, wood  # noqa: E402

ORANGE, DARK = (226, 106, 30), (52, 54, 60)
m = Model('pickup-scatter', HERE, seed=157)
m.material('main', 'paint')
# (name, s0, s1, n0, n1, depth, colour, paint key) - along the gun
PIECES = [('stock', 0.0, 0.15, 0.0, 0.085, 0.044, 'E26A1E', 'orange'),
          ('receiver', 0.14, 0.26, 0.03, 0.098, 0.05, '34363C', 'dark'),
          ('barrel', 0.24, 0.49, 0.066, 0.096, 0.03, 'E26A1E', 'orange'),
          ('pump', 0.27, 0.42, 0.032, 0.066, 0.04, 'B85418', 'pump'),
          ('grip', 0.165, 0.2, -0.06, 0.035, 0.034, '6E4426', 'wood'),
          ('rail', 0.15, 0.27, 0.098, 0.114, 0.022, 'A0A4AC', 'steel'),
          ('sight', 0.44, 0.465, 0.096, 0.112, 0.012, '34363C', 'dark'),
          ('guard', 0.2, 0.25, 0.014, 0.03, 0.016, '1E1E20', 'rubber'),
          ('band', 0.465, 0.49, 0.06, 0.102, 0.036, '34363C', 'dark'),
          ('butt', 0.0, 0.014, -0.004, 0.089, 0.048, '1E1E20', 'rubber')]
LEAN, K = 36.0, 1.0


def place(lean, k):
    a = math.radians(lean)
    d, n = (-math.cos(a), math.sin(a)), (math.sin(a), math.cos(a))   # along the gun; its up
    out = []
    for name, s0, s1, n0, n1, dz, col, key in PIECES:
        s0, s1, n0, n1 = s0 * k, s1 * k, n0 * k, n1 * k
        cs, cn = (s0 + s1) / 2, (n0 + n1) / 2
        cx, cy = d[0] * cs + n[0] * cn, d[1] * cs + n[1] * cn
        fx, fy = cx - n[0] * (n1 - n0) / 2, cy - n[1] * (n1 - n0) / 2   # the foot, turned with it
        corners = [(d[0] * s + n[0] * t, d[1] * s + n[1] * t) for s in (s0, s1) for t in (n0, n1)]
        out.append((name, fx, fy, s1 - s0, n1 - n0, dz, col, key, corners))
    xs = [c[0] for o in out for c in o[8]]
    ys = [c[1] for o in out for c in o[8]]
    return out, (min(xs), max(xs), min(ys), max(ys))


best = None
for lean in [30 + i * 0.25 for i in range(60)]:                      # the lean and size that fit
    _, (x0, x1, y0, y1) = place(lean, 1.0)
    k = 0.446 / (x1 - x0)
    err = abs((y1 - y0) * k - 0.39)
    if best is None or err < best[0]:
        best = (err, lean, k)
_, LEAN, K = best
pieces, (x0, x1, y0, y1) = place(LEAN, K)
mx = (x0 + x1) / 2
for name, fx, fy, sx, sy, dz, col, key, _ in pieces:
    m.box(name, (fx - mx, fy - y0, 0), (sx, sy, dz * K), col, paint=key, rot=(0, 0, -LEAN))
print(f'lean {LEAN:.2f} size x{K:.3f}: {(x1 - x0):.3f} x {(y1 - y0):.3f}')

m.swatch('orange', paint(ORANGE, 0.6))
m.swatch('pump', lambda a, w, h: a.edge_dark(paint((184, 84, 24), 0.4)(a, w, h), 1, 0.6))
m.swatch('dark', paint(DARK, 0.3))
m.swatch('wood', wood((110, 68, 38)))
m.swatch('steel', steel((160, 164, 172)))
m.swatch('rubber', paint('1E1E20', 0.2, 1))

if __name__ == '__main__':
    m.build()
