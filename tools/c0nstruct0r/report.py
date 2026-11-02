#!/usr/bin/env python3
"""c0nstruct0r's report card: how good each NEON-CASTER prop's model is.

  python3 report.py                 every prop in the game's models/, worst first
  python3 report.py NAME [NAME...]  just those (NAME, or a path to an .obj)
  python3 report.py --json F        also write the numbers as JSON
  python3 report.py --models DIR    another models folder (a scratch copy)

Reads the OBJ files only (and each texture's size): no window, nothing
written to the game. Plain Python, no numpy. Per prop:

  SMEAR   % of the textured surface whose pixels are stretched: one way at
          least 3x the other - a row of pixels pulled across a side (what
          models.py's extrude does to every side and top) - and not all one
          colour (a plain band stretched shows no streaks: PLAIN, not scored;
          the textures are read through ImageMagick's `magick`, if there)
  SIZE    % of the textured surface whose pixels are more than 1.5x bigger
          or smaller than the prop's usual size (px/cell: that usual size)
  ANGLE   % of the surface tilted 0.75-8 degrees off square or 45 (the
          staircase outlines extrude leaves) - not round things' facets (a
          face meeting a neighbour at 0.5-20 degrees)
  ASYM    how far the prop is from mirror-symmetric left to right: its
          outline from the front and from above, against its own mirror
          image (% of the outline that doesn't match; the worse of the two)
  TRIS    triangles, against the budget: 1000 (any prop - small ones too)
  COLOUR  % of the surface that's plain colour (bu1ld0r's colour squares):
          shown, not scored
  PLAIN   % of the textured surface stretched over pixels of one colour
          (within 24 levels): shown, not scored

SCORE (higher = worse) = SMEAR + ASYM + (SIZE + ANGLE) / 2 + how far over
budget (100 = twice it), each in %.
"""
import ast
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys

GAME = os.environ.get('NEON_CASTER_DIR') or os.path.expanduser('~/git/neon-caster/neon-caster')  # (the game's folder: hd/, models/)
BUDGET = 1000  # (every prop: Rick, 2026-11-01 - small ones had 200)
STRETCH = 3.0   # (pixels this much longer one way than the other: smeared)
SIZE_OFF = 1.5  # (pixels this much bigger or smaller than usual: off size)
ANG_LO, ANG_HI = 0.75, 8.0
GRID = 64       # (the outlines' grid for ASYM)
FLAT = 24       # (a stretch over pixels this close in colour: plain)

# Every direction with components -1, 0 or 1: square, and 45 degrees.
NICE = []
for a in (-1, 0, 1):
    for b in (-1, 0, 1):
        for c in (-1, 0, 1):
            if a or b or c:
                l = math.sqrt(a * a + b * b + c * c)
                NICE.append((a / l, b / l, c / l))


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    return struct.unpack('>II', head[16:24])


_PIX = {}


def tex_pixels(path, size):
    """The picture's RGBA bytes, through ImageMagick; None without it."""
    if path in _PIX:
        return _PIX[path]
    exe = shutil.which('magick') or shutil.which('convert')
    data = None
    if exe and path:
        try:
            data = subprocess.run([exe, path, '-depth', '8', 'rgba:-'], capture_output=True, timeout=30).stdout
            if len(data) != size[0] * size[1] * 4:
                data = None
        except (OSError, subprocess.SubprocessError):
            data = None
    _PIX[path] = data
    return data


def plain(t, size, data):
    """Whether the pixels a triangle's spots cover are all one colour (its
    box on the picture, at least a pixel; see-through pixels left out)."""
    w, h = size
    us = [x[0] * w for x in t]
    vs = [(1 - x[1]) * h for x in t]
    x0, x1 = int(math.floor(min(us))), int(math.ceil(max(us))) - 1
    y0, y1 = int(math.floor(min(vs))), int(math.ceil(max(vs))) - 1
    x1, y1 = max(x0, x1), max(y0, y1)
    lo = [255, 255, 255]
    hi = [0, 0, 0]
    n = 0
    for y in range(y0, y1 + 1):
        yy = y % h
        for x in range(x0, x1 + 1):
            i = (yy * w + x % w) * 4
            if data[i + 3] == 0:
                continue
            n += 1
            for c in range(3):
                v = data[i + c]
                if v < lo[c]: lo[c] = v
                if v > hi[c]: hi[c] = v
            if n > 1 and max(hi[c] - lo[c] for c in range(3)) > FLAT:
                return False
    return True


def models_py_tables(models_dir):
    """PROPS (heights) and SHAPES (how models.py builds each) from models.py,
    read as literals - never run."""
    props, shapes = {}, {}
    path = os.path.join(models_dir, 'models.py')
    if not os.path.exists(path):
        return props, shapes
    tree = ast.parse(open(path).read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ('PROPS', 'SHAPES'):
                try:
                    val = ast.literal_eval(node.value)
                except ValueError:
                    continue
                (props if name == 'PROPS' else shapes).update(val)
    return props, shapes


def read_mtl(path):
    """Each material's texture (map_Kd), as a path."""
    tex, cur = {}, None
    if not os.path.exists(path):
        return tex
    for line in open(path, errors='replace'):
        w = line.split()
        if not w:
            continue
        if w[0] == 'newmtl' and len(w) > 1:
            cur = w[1]
        elif w[0] == 'map_Kd' and cur and len(w) > 1:
            tex[cur] = os.path.normpath(os.path.join(os.path.dirname(path), ' '.join(w[1:])))
    return tex


def read_obj(path):
    """Triangles as (p0, p1, p2, t0, t1, t2, material); t is None with no vt.
    Also the header's 'made by' line."""
    vs, vts, tris = [], [], []
    mtl, mtllib, made = None, None, ''
    for line in open(path, errors='replace'):
        if line.startswith('#'):
            if 'made by' in line and not made:
                made = 'bu1ld0r' if 'bu1ld0r' in line else ('models.py' if 'models.py' in line else line[1:].strip())
            continue
        w = line.split()
        if not w:
            continue
        k = w[0]
        if k == 'v':
            vs.append((float(w[1]), float(w[2]), float(w[3])))
        elif k == 'vt':
            vts.append((float(w[1]), float(w[2]) if len(w) > 2 else 0.0))
        elif k == 'usemtl':
            mtl = w[1] if len(w) > 1 else None
        elif k == 'mtllib':
            mtllib = ' '.join(w[1:])
        elif k == 'f':
            cs = []
            for c in w[1:]:
                p = c.split('/')
                vi = int(p[0])
                vi = vi - 1 if vi > 0 else len(vs) + vi
                ti = None
                if len(p) > 1 and p[1]:
                    ti = int(p[1])
                    ti = ti - 1 if ti > 0 else len(vts) + ti
                cs.append((vi, ti))
            for j in range(1, len(cs) - 1):  # (a polygon: a fan)
                a, b, c = cs[0], cs[j], cs[j + 1]
                t = None if None in (a[1], b[1], c[1]) else (vts[a[1]], vts[b[1]], vts[c[1]])
                tris.append((vs[a[0]], vs[b[0]], vs[c[0]], t, mtl))
    return tris, mtllib, made


def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def pixel_axes(p0, p1, p2, t0, t1, t2, tw, th):
    """Pixels per cell along the triangle's two main ways (s1 >= s2), from
    the map of its plane onto the picture. None if the triangle is flat."""
    e1, e2 = sub(p1, p0), sub(p2, p0)
    n = cross(e1, e2)
    nl = math.sqrt(dot(n, n))
    l1 = math.sqrt(dot(e1, e1))
    if nl < 1e-12 or l1 < 1e-12:
        return None
    a = (e1[0] / l1, e1[1] / l1, e1[2] / l1)
    nn = (n[0] / nl, n[1] / nl, n[2] / nl)
    b = cross(nn, a)
    x1, y1 = l1, 0.0
    x2, y2 = dot(e2, a), dot(e2, b)
    u1, v1 = (t1[0] - t0[0]) * tw, (t1[1] - t0[1]) * th
    u2, v2 = (t2[0] - t0[0]) * tw, (t2[1] - t0[1]) * th
    det = x1 * y2 - x2 * y1
    if abs(det) < 1e-15:
        return None
    # M = T * inverse(X): plane -> pixels
    i11, i12, i21, i22 = y2 / det, -x2 / det, -y1 / det, x1 / det
    m11, m12 = u1 * i11 + u2 * i21, u1 * i12 + u2 * i22
    m21, m22 = v1 * i11 + v2 * i21, v1 * i12 + v2 * i22
    s = m11 * m11 + m12 * m12 + m21 * m21 + m22 * m22
    d = m11 * m22 - m12 * m21
    r = math.sqrt(max(0.0, s * s - 4 * d * d))
    s1 = math.sqrt(max(0.0, (s + r) / 2))
    s2 = math.sqrt(max(0.0, (s - r) / 2))
    return s1, s2


def angle_off(n):
    """Degrees from the nearest square / 45-degree way."""
    best = max(abs(dot(n, q)) for q in NICE)
    return math.degrees(math.acos(min(1.0, best)))


def outline(tris, ax, ay, lo, hi):
    """The model's outline seen along the third axis, on a GRID x GRID grid
    over its box (x across): a set of filled cells."""
    sx = hi[ax] - lo[ax]
    sy = hi[ay] - lo[ay]
    span = max(sx, sy, 1e-9)
    cell = span / GRID
    nx = max(1, int(math.ceil(sx / cell - 1e-9)))
    ny = max(1, int(math.ceil(sy / cell - 1e-9)))
    filled = set()
    for p0, p1, p2, _, _ in tris:
        pts = [((p[ax] - lo[ax]) / cell, (p[ay] - lo[ay]) / cell) for p in (p0, p1, p2)]
        (ax0, ay0), (bx0, by0), (cx0, cy0) = pts
        area = (bx0 - ax0) * (cy0 - ay0) - (cx0 - ax0) * (by0 - ay0)
        if abs(area) < 1e-12:
            continue
        i0 = max(0, int(math.floor(min(ax0, bx0, cx0))))
        i1 = min(nx - 1, int(math.floor(max(ax0, bx0, cx0))))
        j0 = max(0, int(math.floor(min(ay0, by0, cy0))))
        j1 = min(ny - 1, int(math.floor(max(ay0, by0, cy0))))
        for j in range(j0, j1 + 1):
            y = j + 0.5
            for i in range(i0, i1 + 1):
                x = i + 0.5
                w0 = (bx0 - x) * (cy0 - y) - (cx0 - x) * (by0 - y)
                w1 = (cx0 - x) * (ay0 - y) - (ax0 - x) * (cy0 - y)
                w2 = (ax0 - x) * (by0 - y) - (bx0 - x) * (ay0 - y)
                if (w0 >= 0 and w1 >= 0 and w2 >= 0) or (w0 <= 0 and w1 <= 0 and w2 <= 0):
                    filled.add((i, j))
    return filled, nx


def asym(tris, lo, hi):
    """% of the outline that isn't its own mirror image (x flipped), the
    worse of the front view (x, y) and the top (x, z)."""
    worst = 0.0
    for ay in (1, 2):
        f, nx = outline(tris, 0, ay, lo, hi)
        if not f:
            continue
        miss = sum(1 for (i, j) in f if (nx - 1 - i, j) not in f)
        worst = max(worst, 100.0 * miss / len(f))
    return worst


def round_facet(corners, n, tris):
    """A round thing's facet: a triangle meeting another that shares a corner with it at
    0.5 to 20 degrees (a cylinder's sides, a sphere's) - not a crooked face."""
    key = lambda p: (round(p[0], 4), round(p[1], 4), round(p[2], 4))
    mine = {key(p) for p in corners}
    for p0, p1, p2, _, _ in tris:
        if not ({key(p0), key(p1), key(p2)} & mine):
            continue
        m = cross(sub(p1, p0), sub(p2, p0))
        ml = math.sqrt(dot(m, m))
        if ml < 1e-12:
            continue
        d = max(-1.0, min(1.0, dot(n, m) / ml))
        if 0.5 < math.degrees(math.acos(d)) < 20:
            return True
    return False


def wmedian(pairs):
    """The area-weighted median of (value, area) pairs."""
    pairs = sorted(pairs)
    tot = sum(a for _, a in pairs)
    acc = 0.0
    for v, a in pairs:
        acc += a
        if acc >= tot / 2:
            return v
    return 0.0


def grade(path, name, props, shapes):
    tris, mtllib, made = read_obj(path)
    if not tris:
        return None
    mats = read_mtl(os.path.join(os.path.dirname(path), mtllib)) if mtllib else {}
    base = os.path.dirname(path)
    fallback = None
    for c in (os.path.join(base, '..', 'hd', 'models', name + '_tex.png'), os.path.join(base, name + '_tex.png')):
        if os.path.exists(c):
            fallback = os.path.normpath(c)
            break
    sizes = {}

    def tex_size(m):
        p = mats.get(m) or (next(iter(mats.values())) if mats else None)
        if not p or not os.path.exists(p):
            p = fallback
        if p not in sizes:
            sizes[p] = png_size(p) if p and os.path.exists(p) else None
        return sizes[p], p

    lo = [min(t[k][i] for t in tris for k in range(3)) for i in range(3)]
    hi = [max(t[k][i] for t in tris for k in range(3)) for i in range(3)]

    area_all = area_tex = area_col = 0.0
    smear = ang = flat = 0.0
    dens = []
    texs = set()
    crooked = []
    for p0, p1, p2, t, m in tris:
        n = cross(sub(p1, p0), sub(p2, p0))
        nl = math.sqrt(dot(n, n))
        if nl < 1e-12:
            continue
        a = nl / 2
        area_all += a
        off = angle_off((n[0] / nl, n[1] / nl, n[2] / nl))
        if ANG_LO <= off <= ANG_HI:
            crooked.append(((p0, p1, p2), (n[0] / nl, n[1] / nl, n[2] / nl), a))
        if t is None:
            area_col += a
            continue
        sz, tp = tex_size(m)
        if not sz:
            area_col += a
            continue
        texs.add(tp)
        r = pixel_axes(p0, p1, p2, t[0], t[1], t[2], sz[0], sz[1])
        if r is None:
            continue
        s1, s2 = r
        if s1 < 1e-6:  # (all three corners on one pixel: a colour square)
            area_col += a
            continue
        area_tex += a
        if s2 * STRETCH < s1:
            px = tex_pixels(tp, sz)
            if px is not None and plain(t, sz, px):
                flat += a
            else:
                smear += a
        else:
            dens.append((math.sqrt(s1 * s2), a))
    ang = sum(a for c, n, a in crooked if not round_facet(c, n, tris))
    pxc = wmedian(dens) if dens else 0.0
    texd = area_tex - smear - flat
    offsz = sum(a for d, a in dens if d > pxc * SIZE_OFF or d * SIZE_OFF < pxc) if pxc else 0.0

    budget = BUDGET
    shp = shapes.get(name)
    kind = made or '?'
    if made == 'models.py' and shp:
        kind = shp[0]
    elif made == 'models.py':
        kind = 'pixelmon' if os.path.exists(os.path.join(base, 'src', name + '.gltf')) else 'models.py'

    pct = lambda x, of: 100.0 * x / of if of > 0 else 0.0
    r = {
        'name': name, 'kind': kind, 'tris': len(tris), 'budget': budget,
        'smear': pct(smear, area_tex), 'size': pct(offsz, texd),
        'plain': pct(flat, area_tex),
        'angle': pct(ang, area_all), 'asym': asym(tris, lo, hi),
        'colour': pct(area_col, area_all), 'px_cell': pxc,
        'box': [round(hi[i] - lo[i], 3) for i in range(3)],
        'textures': sorted(os.path.relpath(p, base) for p in texs if p),
    }
    over = max(0.0, 100.0 * (len(tris) / budget - 1))
    r['over'] = over
    r['score'] = r['smear'] + r['asym'] + (r['size'] + r['angle']) / 2 + min(over, 200.0)
    return r


def main(argv):
    models = os.path.join(GAME, 'models')
    out_json = None
    names = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--models':
            models = os.path.expanduser(argv[i + 1]); i += 1
        elif a == '--json':
            out_json = argv[i + 1]; i += 1
        elif a in ('-h', '--help'):
            print(__doc__); return 0
        else:
            names.append(a)
        i += 1
    props, shapes = models_py_tables(models)
    paths = []
    if names:
        for n in names:
            paths.append(n if n.endswith('.obj') else os.path.join(models, n + '.obj'))
    else:
        paths = sorted(os.path.join(models, f) for f in os.listdir(models) if f.endswith('.obj'))
    rows = []
    for p in paths:
        if not os.path.exists(p):
            print(f'(no {p})', file=sys.stderr)
            continue
        name = os.path.splitext(os.path.basename(p))[0]
        r = grade(p, name, props, shapes)
        if r:
            rows.append(r)
    rows.sort(key=lambda r: -r['score'])

    print(f"{'#':>3}  {'PROP':<22}{'KIND':<10}{'SCORE':>6}{'SMEAR':>7}{'SIZE':>6}{'ANGLE':>7}{'ASYM':>6}{'TRIS':>11}{'COLOUR':>8}{'PLAIN':>7}{'PX/CELL':>9}")
    for k, r in enumerate(rows, 1):
        tris = f"{r['tris']}/{r['budget']}"
        print(f"{k:>3}  {r['name']:<22}{r['kind']:<10}{r['score']:>6.0f}{r['smear']:>6.0f}%{r['size']:>5.0f}%{r['angle']:>6.0f}%"
              f"{r['asym']:>5.0f}%{tris:>11}{r['colour']:>7.0f}%{r['plain']:>6.0f}%{r['px_cell']:>9.0f}")
    if out_json:
        with open(out_json, 'w') as f:
            json.dump(rows, f, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
