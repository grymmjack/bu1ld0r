#!/usr/bin/python3
"""c0-medkit's mapping: port lines (pick / picture) for every face of every part.

  /usr/bin/python3 tools/c0nstruct0r/m0d3l/medkit/texture.py [K] [--turn] > texture.txt
  (--turn: a view before each side, looking at it - for watching)

Each face gets a rect exactly its size at P pixels a cell (K = 1) - the body its own regions,
the small parts a corner of their material's swatch. Regions: atlas.py's docstring.
The port's rects are in the picture's OWN pixels: the layout (K = 1) times K (the picture
drawn at K = 2 is 512 across).
"""
import sys
P = 700
K = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 2
REF = 'c0nstruct0r/c0-medkit'
# part: (size x, y, z, {facing: region origin or full rect})
ALU, RUB, WSW, LATCH, GRIP = (216, 81), (0, 180), (184, 180), (230, 0), (124, 180)
BODY = {'-z': (0, 0, 112, 77), '+z': (116, 0, 228, 77), '+x': (0, 81, 45.5, 158),
        '-x': (50, 81, 95.5, 158), '+y': (100, 81, 212, 126.5), '-y': (100, 131, 212, 176.5)}
PARTS = [
    (1, (0.16, 0.11, 0.065), BODY),
    (2, (0.165, 0.008, 0.07), RUB),
] + [(p, (0.012, 0.088, 0.012), ALU) for p in (3, 4, 5, 6)] \
  + [(p, (0.012, 0.018, 0.012), ALU) for p in (24, 25, 26, 27)] \
  + [(p, (0.02, 0.024, 0.006), {'-z': LATCH, '+z': LATCH, '*': ALU}) for p in (7, 8, 9, 10)] \
  + [(p, (0.01, 0.022, 0.013), ALU) for p in (11, 12)] \
  + [(13, (0.08, 0.01, 0.016), {'+y': GRIP, '*': RUB})] \
  + [(p, (0.022, 0.008, 0.015), RUB) for p in (14, 15, 16, 17)] \
  + [(p, (0.0121, 0.0385, 0.006), WSW) for p in (18, 21)] \
  + [(p, (0.0132, 0.0121, 0.006), WSW) for p in (19, 20, 22, 23)]
WAYS = [('-z', '0 0 -1', 'view 0'), ('+z', '0 0 1', 'view 180'), ('+x', '1 0 0', 'view 90'),
        ('-x', '-1 0 0', 'view 270'), ('+y', '0 1 0', 'top'), ('-y', '0 -1 0', 'top')]
# the camera looks at the side being mapped (Rick watches): yaw, pitch for each way
LOOK = {'-z': (0, 8), '+z': (180, 8), '+x': (90, 8), '-x': (270, 8), '+y': (20, 60), '-y': (20, -60)}
TURN = '--turn' in sys.argv
DIST = 0.34


def size(way, sx, sy, sz):
    if way in ('-z', '+z'):
        return sx * P, sy * P
    if way in ('+x', '-x'):
        return sz * P, sy * P
    return sx * P, sz * P


def f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


out = []
for part, (sx, sy, sz), where in PARTS:
    out.append(f'edit {part}')
    for way, normal, how in WAYS:
        reg = where.get(way, where.get('*')) if isinstance(where, dict) else where
        if len(reg) == 4:
            x0, y0, x1, y1 = reg
        else:
            w, h = size(way, sx, sy, sz)
            x0, y0 = reg
            x1, y1 = x0 + w, y0 + h
        if TURN:
            out.append(f'view {LOOK[way][0]} {LOOK[way][1]} {DIST}')
        out.append(f'pick facing {normal}')
        out.append(f'picture {REF} {how} {f(x0 * K)} {f(y0 * K)} {f(x1 * K)} {f(y1 * K)} own')
    out.append('done')
print('\n'.join(out))
