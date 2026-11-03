#!/usr/bin/python3
"""m0d3l's box mapping: port lines giving every face of box-made parts its patch of one picture.

    from boxmap import lines
    PARTS = [(1, (0.36, 0.13, 0.20), {'-z': (0, 0, 122.4, 44.2), '*': (128, 144)}), ...]
    print('\\n'.join(lines(PARTS, P=340, K=2, ref='c0nstruct0r/c0-NAME', turn=True)))

A part is (number, its box size x y z, where): `where` is a region origin (x0, y0) - the face
gets a rect its own size from there - or a full rect (x0, y0, x1, y1), or a dict of those per
way ('-z' '+z' '+x' '-x' '+y' '-y', '*' for the rest). Regions are in the layout's K = 1
pixels at P pixels a cell; the port's rects are the picture's OWN pixels, so they're x K
(the picture drawn at K = 2 is 512 across - giving 256 numbers halves every face).

Ways: -z front (view 0), +z back (180), +x (90), -x (270), +y / -y (top). turn=True puts a
`view` before each side, looking at it, so whoever watches sees the face take its picture.
"""
WAYS = [('-z', '0 0 -1', 'view 0'), ('+z', '0 0 1', 'view 180'), ('+x', '1 0 0', 'view 90'),
        ('-x', '-1 0 0', 'view 270'), ('+y', '0 1 0', 'top'), ('-y', '0 -1 0', 'top')]
LOOK = {'-z': (0, 8), '+z': (180, 8), '+x': (90, 8), '-x': (270, 8), '+y': (20, 60), '-y': (20, -60)}


def face_size(way, sx, sy, sz, P):
    if way in ('-z', '+z'):
        return sx * P, sy * P
    if way in ('+x', '-x'):
        return sz * P, sy * P
    return sx * P, sz * P


def num(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def lines(parts, P, K, ref, turn=False, dist=0.5, ways=None):
    out = []
    for part, (sx, sy, sz), where in parts:
        out.append(f'edit {part}')
        for way, normal, how in WAYS:
            if ways and way not in ways:
                continue
            reg = where.get(way, where.get('*')) if isinstance(where, dict) else where
            if reg is None:
                continue
            if len(reg) == 4:
                x0, y0, x1, y1 = reg
            else:
                w, h = face_size(way, sx, sy, sz, P)
                x0, y0 = reg
                x1, y1 = x0 + w, y0 + h
            if turn:
                out.append(f'view {LOOK[way][0]} {LOOK[way][1]} {dist}')
            out.append(f'pick facing {normal}')
            out.append(f'picture {ref} {how} {num(x0 * K)} {num(y0 * K)} {num(x1 * K)} {num(y1 * K)} own')
        out.append('done')
    return out
