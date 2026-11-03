#!/usr/bin/python3
"""m0kit: a m0d3l model from one spec file - shape, one picture, mapping, materials, checks, staging.

    import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from m0kit import Model
    m = Model('vending', here=os.path.dirname(os.path.abspath(__file__)))
    body = m.box('body', (0, 0.03, 0), (0.34, 0.68, 0.25), '9AA0A8',
                 paint={'-z': front, '+z': back, '+x': side, '-x': side, '+y': top, '-y': under},
                 walls=dark)
    body.cut('-z', (0.02, 0.15, 0.25, 0.62), 0.03)        # world x0 x1 y0 y1 on that face; + in, - out
    m.box('foot-a', (0.12, 0, 0.08), (0.03, 0.03, 0.03), '303030', paint='steel')
    m.swatch('steel', lambda a, w, h: a.tinted(ALU, w, h, (210, 214, 220), 0.5))
    m.material('steel', '0:0:87:13:47:7:33:0'); m.box(..., mat='steel')
    m.build()          # (python3 build.py [shape|map|all]; all is the default)

Painters are f(a, w, h) -> an image (numpy H x W x 3), w and h in the 256 layout's pixels (a is the
paint.Atlas; a.px() converts). Each is drawn as seen from that side: from the front +x is on the
left; a top is seen from above with -x on the right and +z (the back) at the top. A string instead
of a painter names a shared swatch (m.swatch). Round parts (m.cyl) take 'side' (the whole wrap,
drawn left to right going round as seen from outside, starting at the front), 'top', 'bottom'.

Every patch is at the same pixels a cell (P, the largest that packs into 256), drawn at K = 2 into
pictures/c0nstruct0r/c0-NAME.png. Runs against the scripting bu1ld0r in /tmp/claude-1000/bn/app
(rc.py's port), saves models/c0-NAME.bld, exports, writes NAME-eight.png in the model's folder,
the report card, and stages under the game's name (stage.sh).
"""
import json
import math
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '../../..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
from paint import Atlas  # noqa: E402
from rc import Bu1ld0r  # noqa: E402

BN = os.environ.get('M0KIT_DIR', '/tmp/claude-1000/bn/app')
GAME = os.path.expanduser('~/git/neon-caster/neon-caster')
WAYS = {'-z': ((0, 0, -1), 'view 0'), '+z': ((0, 0, 1), 'view 180'), '+x': ((1, 0, 0), 'view 90'),
        '-x': ((-1, 0, 0), 'view 270'), '+y': ((0, 1, 0), 'top'), '-y': ((0, -1, 0), 'top')}
AX = {'x': 0, 'y': 1, 'z': 2}
MATS = {'paint': '0:0:33:47:0:13:33:0', 'felt': '0:0:7:87:0:33:0:53', 'steel': '0:0:87:13:47:7:33:0',
        'iron': '0:0:10:85:80:15:0:0', 'plastic': '0:0:40:50:0:10:20:0', 'rubber': '0:0:10:80:0:20:0:0',
        'wood': '0:0:20:73:0:47:20:0', 'glass': '0:0:90:5:0:0:60:0', 'glow': '0:60:40:40:0:0:20:0'}


CORNER_PX = 16   # models.py's MUZZLE_BOX of a 256 picture


def face_dims(way, sx, sy, sz):
    """(w, h) in cells of a box's face seen from that way."""
    if way in ('-z', '+z'):
        return sx, sy
    if way in ('+x', '-x'):
        return sz, sy
    return sx, sz


def turned_dims(size, rot):
    """The world extents of a box of `size` turned Z, then X, then Y (degrees) - as bu1ld0r does."""
    sx, sy, sz = size
    rz, rx, ry = [math.radians(a) for a in (rot[2], rot[0], rot[1])]
    pts = []
    for x in (-sx / 2, sx / 2):
        for y in (-sy / 2, sy / 2):
            for z in (-sz / 2, sz / 2):
                x1, y1 = x * math.cos(rz) - y * math.sin(rz), x * math.sin(rz) + y * math.cos(rz)
                y2, z2 = y1 * math.cos(rx) - z * math.sin(rx), y1 * math.sin(rx) + z * math.cos(rx)
                x3, z3 = x1 * math.cos(ry) + z2 * math.sin(ry), -x1 * math.sin(ry) + z2 * math.cos(ry)
                pts.append((x3, y2, z3))
    return tuple(max(p[i] for p in pts) - min(p[i] for p in pts) for i in range(3))


class Part:
    def __init__(self, m, kind, name, at, size, col, paint, walls, mat, seg, amt, rot):
        self.m, self.kind, self.name, self.at, self.size, self.col = m, kind, name, at, size, col
        self.paint, self.walls, self.mat, self.seg, self.amt, self.rot = paint, walls, mat, seg, amt, rot
        self.cuts = []
        self.num = 0

    def cut(self, way, rect, depth, inset=0.1):
        """A recess (depth > 0) or a raised panel (depth < 0) on that face: rect in world terms - for
        a z face x0 x1 y0 y1, an x face z0 z1 y0 y1, a y face x0 x1 z0 z1. One a face."""
        self.cuts.append((way, rect, depth, inset))
        return self

    def box(self):
        """(lo, hi) of the part's own box, raised panels included."""
        x, y, z = self.at
        sx, sy, sz = self.size
        lo, hi = [x - sx / 2, y, z - sz / 2], [x + sx / 2, y + sy, z + sz / 2]
        for way, rect, depth, _ in self.cuts:
            if depth < 0:
                a = AX[way[1]]
                if way[0] == '+':
                    hi[a] += -depth
                else:
                    lo[a] -= -depth
        return lo, hi

    def own_size(self):
        if self.rot:
            return turned_dims(self.size, self.rot)
        lo, hi = self.box()
        return hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]


class Model:
    def __init__(self, name, here, K=2, budget=256, gap=2, seed=1):
        self.name, self.here, self.K, self.gap = name, here, K, gap
        self.corner = None                           # muzzle corner colour (models.py's MUZZLE_UV): paint='CORNER'
        self.ref = f'c0nstruct0r/c0-{name}'
        self.out = os.path.join(REPO, 'pictures', 'c0nstruct0r', f'c0-{name}.png')
        self.parts, self.swatches, self.mats, self.say = [], {}, {}, []
        self.budget, self.seed = budget, seed
        self.a = Atlas(K=K, seed=seed, here=here)
        self.layout = {}
        self.P = None

    # -- the spec -------------------------------------------------------------------------
    def _add(self, kind, name, at, size, col, paint, walls, mat, seg, amt, rot):
        p = Part(self, kind, name, at, size, col, paint, walls, mat, seg, amt, rot)
        self.parts.append(p)
        p.num = len(self.parts)
        return p

    def box(self, name, at, size, col='808080', paint=None, walls=None, mat='main', rot=None):
        return self._add('box', name, at, size, col, paint, walls, mat, None, None, rot)

    def cyl(self, name, at, size, col='808080', paint=None, seg=12, amt=None, mat='main', kind='cylinder', rot=None):
        """A round part standing up (cylinder, or cone with amt = the top's share of the radius). Turned
        (rot = RX RY RZ degrees, round its foot): mapped like a box, paint keyed by way."""
        return self._add(kind, name, at, size, col, paint, None, mat, seg, amt, rot)

    def swatch(self, key, painter):
        self.swatches[key] = painter

    def material(self, key, m):
        self.mats[key] = MATS.get(m, m)

    # -- the picture's layout -------------------------------------------------------------
    def _regions(self, P):
        """[(key, w, h)] in layout pixels at P pixels a cell."""
        regs, sw = [], {}
        for p in self.parts:
            sx, sy, sz = p.own_size()
            if p.kind == 'box' or p.rot:
                ways = list(WAYS)
                for way in ways:
                    pt = p.paint.get(way, p.paint.get('*')) if isinstance(p.paint, dict) else p.paint
                    w, h = face_dims(way, sx, sy, sz)
                    if pt == 'CORNER':
                        continue
                    if isinstance(pt, str):
                        cw, ch = sw.get(pt, (0, 0))
                        sw[pt] = (max(cw, w * P), max(ch, h * P))
                    else:
                        regs.append(((p.num, way), w * P, h * P))
                if p.cuts:
                    ws = [face_dims(w, sx, sy, sz) for w in WAYS]
                    W, H = max(a for a, _ in ws), max(b for _, b in ws)
                    if isinstance(p.walls, str):
                        cw, ch = sw.get(p.walls, (0, 0))
                        sw[p.walls] = (max(cw, W * P), max(ch, H * P))
                    else:
                        regs.append(((p.num, 'walls'), W * P, H * P))
            else:
                r = max(sx, sz) / 2
                n = p.seg
                side_w = 2 * n * r * math.sin(math.pi / n) * P   # perimeter of the polygon
                for key, (w, h) in (('side', (side_w, sy * P)), ('top', (sx * P, sz * P)),
                                    ('bottom', (sx * P, sz * P))):
                    pt = p.paint.get(key) if isinstance(p.paint, dict) else p.paint
                    if isinstance(pt, str):
                        cw, ch = sw.get(pt, (0, 0))
                        sw[pt] = (max(cw, w), max(ch, h))
                    else:
                        regs.append(((p.num, key), w, h))
        for k, (w, h) in sw.items():
            regs.append((('sw', k), w, h))
        return regs

    def _pack(self, regs, size):
        """Shelf packing: {key: (x, y, w, h)} or None if it doesn't fit."""
        g = self.gap
        out, x, y, shelf = {}, 0, 0, 0
        for key, w, h in sorted(regs, key=lambda r: (-math.ceil(r[2]), -r[1])):
            w, h = math.ceil(w), math.ceil(h)
            if w > size or h > size:
                return None
            if x + w > size:
                x, y, shelf = 0, y + shelf + g, 0
            if y + h > size:
                return None
            if self.corner and x + w > size - CORNER_PX and y + h > size - CORNER_PX:
                x, y, shelf = 0, y + shelf + g, 0                       # the muzzle corner stays free
                if y + h > size or (x + w > size - CORNER_PX and y + h > size - CORNER_PX):
                    return None
            out[key] = (x, y, w, h)
            x += w + g
            shelf = max(shelf, h)
        return out

    def plan(self):
        lo, hi = 20.0, 3000.0
        best = None
        for _ in range(40):
            mid = (lo + hi) / 2
            lay = self._pack(self._regions(mid), self.budget)
            if lay:
                lo, best = mid, (mid, lay)
            else:
                hi = mid
        self.P, self.layout = best[0] * 0.995, self._pack(self._regions(best[0] * 0.995), self.budget)
        return self.P

    def region(self, key):
        return self.layout[key]

    # -- the picture ----------------------------------------------------------------------
    def draw(self):
        a = self.a
        for key, (x, y, w, h) in self.layout.items():
            if key[0] == 'sw':
                fn = self.swatches[key[1]]
            else:
                p = self.parts[key[0] - 1]
                if key[1] == 'walls':
                    fn = p.walls
                else:
                    fn = p.paint.get(key[1], p.paint.get('*')) if isinstance(p.paint, dict) else p.paint
            img = fn(a, w, h)
            a.put((x, y), img[:a.px(h), :a.px(w)])
        if self.corner:
            c = np.ones((a.px(CORNER_PX), a.px(CORNER_PX), 3), np.float32) * np.array(self.corner, np.float32)
            a.put((self.budget - CORNER_PX, self.budget - CORNER_PX), c)
        a.save(self.out)

    # -- bu1ld0r --------------------------------------------------------------------------
    def connect(self):
        self.b = Bu1ld0r(BN, timeout=120)
        self.run(['take', 'pace 0'])

    def run(self, lines):
        out = []
        for ln in lines:
            ln = ln.strip()
            if not ln or ln.startswith('#'):
                continue
            r = self.b.cmd(ln)
            out.append(r)
            if r.startswith('err'):
                raise RuntimeError(f'{ln} -> {r}')
        return out

    def shape_lines(self):
        L = ['new force']
        for p in self.parts:
            x, y, z = p.at
            sx, sy, sz = p.size
            extra = f' {p.rot[0]} {p.rot[1]} {p.rot[2]}' if p.rot else ''
            if p.kind == 'box':
                L.append(f'add box {x} {y} {z} {sx} {sy} {sz}{extra} col={p.col} name={p.name}')
            else:
                amt = f' amt={p.amt}' if p.amt is not None else ''
                L.append(f'add {p.kind} {x} {y} {z} {sx} {sy} {sz}{extra} seg={p.seg}{amt} col={p.col} name={p.name}')
            for way, rect, depth, k in p.cuts:
                L += self.cut_lines(p, way, rect, depth, k)
        return L

    def cut_lines(self, p, way, rect, depth, k):
        x, y, z = p.at
        sx, sy, sz = p.size
        c = [x, y + sy / 2, z]
        a = AX[way[1]]
        u, v = [i for i in range(3) if i != a]
        dims = [sx, sy, sz]
        r0, r1, s0, s1 = rect
        inner = 1 - k
        sc = [1.0, 1.0, 1.0]
        mv = [0.0, 0.0, 0.0]
        sc[u] = (r1 - r0) / (dims[u] * inner)
        sc[v] = (s1 - s0) / (dims[v] * inner)
        mv[u] = (r0 + r1) / 2 - c[u]
        mv[v] = (s0 + s1) / 2 - c[v]
        n = ' '.join(str(i) for i in WAYS[way][0])
        f = lambda t: f'{t:.5f}'.rstrip('0').rstrip('.') if t else '0'  # noqa: E731
        return [f'edit {p.num}', f'pick facing {n}', f'inset {k}',
                f'scale {f(sc[0])} {f(sc[1])} {f(sc[2])}', f'move {f(mv[0])} {f(mv[1])} {f(mv[2])}',
                f'extrude {f(-depth)}', 'done']

    def faces(self, p):
        self.run([f'edit {p.num}'])
        r = self.b.cmd(f'faces {p.num}')
        if not r.startswith('ok'):
            raise RuntimeError(r)
        return json.loads(r[3:])

    def rect(self, key, w=None, h=None):
        """The port's rect (the picture's own pixels) for a region, or its top-left w x h."""
        if key == ('sw', 'CORNER'):                      # the muzzle corner: u, v > .95 (the game colours it)
            b, K = self.budget, self.K
            return f'{(b - 10) * K:.2f} {(b - 10) * K:.2f} {(b - 2) * K:.2f} {(b - 2) * K:.2f}'
        x, y, rw, rh = self.region(key)
        w = rw if w is None else w
        h = rh if h is None else h
        K = self.K
        return f'{x * K:.2f} {y * K:.2f} {(x + w) * K:.2f} {(y + h) * K:.2f}'

    def key_for(self, p, way):
        pt = p.paint.get(way, p.paint.get('*')) if isinstance(p.paint, dict) else p.paint
        return ('sw', pt) if isinstance(pt, str) else (p.num, way)

    def map_lines(self, p):
        L = []
        sx, sy, sz = p.own_size()
        P = self.P
        if p.rot:                                    # turned: each face from its main axis (triplanar)
            groups = {}
            for f in self.faces(p):
                n = f['n']
                a = max(range(3), key=lambda i: abs(n[i]))
                groups.setdefault(('+' if n[a] > 0 else '-') + 'xyz'[a], []).append(f['f'])
            L.append(f'edit {p.num}')
            for way, ids in groups.items():
                w, h = face_dims(way, sx, sy, sz)
                L += ['pick ' + ' '.join(map(str, ids)),
                      f'picture {self.ref} {WAYS[way][1]} {self.rect(self.key_for(p, way), w * P, h * P)} own']
            L.append('done')
            return L
        if p.kind == 'box':
            if not p.cuts:
                L.append(f'edit {p.num}')
                for way, (n, how) in WAYS.items():
                    w, h = face_dims(way, sx, sy, sz)
                    L += [f'pick facing {" ".join(map(str, n))}',
                          f'picture {self.ref} {how} {self.rect(self.key_for(p, way), w * P, h * P)} own']
                L.append('done')
                return L
            fs = self.faces(p)
            lo, hi = p.box()
            cutways = {c[0] for c in p.cuts}
            groups = {}
            for f in fs:
                n = f['n']
                a = max(range(3), key=lambda i: abs(n[i]))
                if abs(n[a]) < 0.98:
                    raise RuntimeError(f'{p.name}: face {f["f"]} not square to an axis: {n}')
                way = ('+' if n[a] > 0 else '-') + 'xyz'[a]
                ext = hi[a] if n[a] > 0 else lo[a]
                outer = abs(f['c'][a] - ext) < 1e-4 or way in cutways
                groups.setdefault((way, outer), []).append(f['f'])
            L.append(f'edit {p.num}')
            for (way, outer), ids in groups.items():
                n, how = WAYS[way]
                w, h = face_dims(way, sx, sy, sz)
                key = self.key_for(p, way) if outer else (
                    ('sw', p.walls) if isinstance(p.walls, str) else (p.num, 'walls'))
                L += ['pick ' + ' '.join(map(str, ids)),
                      f'picture {self.ref} {how} {self.rect(key, w * P, h * P)} own']
            L.append('done')
            return L
        # round: the side wrapped face by face, the caps from above. With sides not a multiple of 4
        # a face sits centred on the front and two faces share column 0: fine for an even pattern only
        if p.seg % 4:
            print(f'note: {p.name} has {p.seg} sides - its wrap repeats a column (use 8, 12, 16 for a front picture)')
        fs = self.faces(p)
        lo, hi = p.box()
        cx, cz = (lo[0] + hi[0]) / 2, (lo[2] + hi[2]) / 2
        key = ('sw', p.paint['side']) if isinstance(p.paint.get('side'), str) else (p.num, 'side')
        x0, y0, rw, rh = self.region(key)
        w_side = 2 * p.seg * (sx / 2) * math.sin(math.pi / p.seg) * P
        h_side = sy * P
        K = self.K
        L.append(f'edit {p.num}')
        L += self.wrap(fs, x0 * K, y0 * K, w_side * K, h_side * K, p.seg, (lo[0], hi[0], lo[2], hi[2]), cx, cz,
                       {'sphere': (0.7, 0.7), 'diamond': (0.2, 0.98)}.get(p.kind, (0.98, 0.98)))
        if p.kind in ('sphere', 'diamond'):          # its flat-ish top and bottom rows: seen from above
            up, dn = {'sphere': (0.7, 0.7), 'diamond': (0.2, 0.98)}[p.kind]
            ids = [f['f'] for f in fs if f['n'][1] > up or f['n'][1] < -dn]
            if ids:
                L += ['pick ' + ' '.join(map(str, ids)),
                      f'picture {self.ref} top {self.rect(key, min(sx * P, rw), min(sz * P, rh))} own']
        for cap, n in {'sphere': (), 'diamond': (('top', '0 1 0'),)}.get(p.kind, (('top', '0 1 0'), ('bottom', '0 -1 0'))):
            k2 = ('sw', p.paint[cap]) if isinstance(p.paint.get(cap), str) else (p.num, cap)
            L += [f'pick facing {n}', f'picture {self.ref} top {self.rect(k2, sx * P, sz * P)} own']
        L.append('done')
        return L

    def wrap(self, faces, x0, y0, w, h, n, box, cx, cz, lim=(0.98, 0.98)):
        bx0, bx1, bz0, bz1 = box
        step = 360.0 / n
        d = math.radians(step / 2)
        col = w / n
        L = []
        for f in faces:
            nx, ny, nz = f['n']
            fx, fy, fz = f['c'][0] - cx, f['c'][1], f['c'][2] - cz
            if ny > lim[0] or ny < -lim[1] or fx * nx + fz * nz <= 0:
                continue
            am = math.degrees(math.atan2(nz, nx)) % 360
            k = int(round((am - step / 2) / step)) % n
            dist = math.hypot(fx, fz)
            am = (k + 0.5) * step
            yaw = am + 90
            rx, rz = -math.cos(math.radians(yaw)), -math.sin(math.radians(yaw))
            qs = [x * rx + z * rz for x in (bx0, bx1) for z in (bz0, bz1)]
            q0, q1 = min(qs), max(qs)
            qq = q1 - q0
            r = dist / math.cos(d)
            a_ax = cx * rx + cz * rz
            a_left = a_ax - r * math.sin(d)
            # column order: from the front (-z, angle 270) going round as seen from outside
            j = int(round(((270 - (k + 0.5) * step) % 360) / step - 0.5)) % n
            u_left = x0 + j * col
            s = col * qq / (2 * r * math.sin(d))
            sx0 = u_left - (a_left - q0) / qq * s
            L += [f'pick {f["f"]}', f'picture {self.ref} view {yaw % 360:.4f} {sx0:.4f} {y0:.4f} {sx0 + s:.4f} {y0 + h:.4f} own']
        return L

    # -- after ----------------------------------------------------------------------------
    def fix(self):
        r = self.run(['fix'])[0]
        t = r[3:].split()
        return {t[i]: t[i + 1] for i in range(0, len(t) - 1, 2)}

    def shot(self, tag, yaw, pitch, dist=None, how='clean'):
        self.run([f'view {yaw} {pitch}' + (f' {dist}' if dist else '')])
        r = self.run([f'shot {tag} {how}'])[0]
        p = r[3:].strip()
        return p if os.path.isabs(p) else os.path.join(BN, p)

    def sheet(self):
        lo = [min(p.box()[0][i] for p in self.parts) for i in range(3)]
        hi = [max(p.box()[1][i] for p in self.parts) for i in range(3)]
        d = max(hi[i] - lo[i] for i in range(3)) * 2.6
        files = [self.shot(f'm0{f}', f * 45, 10, d) for f in range(8)]
        files += [self.shot('m0top', 30, 55, d), self.shot('m0low', 30, -30, d)]
        ims = []
        for fp in files:
            im = Image.open(fp).convert('RGB')
            W, H = im.size
            cw, ch = int(W * 0.5), int(H * 0.74)
            im = im.crop(((W - cw) // 2, (H - ch) // 2, (W + cw) // 2, (H + ch) // 2)).resize((300, int(300 * ch / cw)))
            ims.append(im)
        w, h = ims[0].size
        out = Image.new('RGB', (w * 5, h * 2))
        for i, im in enumerate(ims):
            out.paste(im, ((i % 5) * w, (i // 5) * h))
        p = os.path.join(self.here, f'{self.name}-eight.png')
        out.save(p)
        return p

    def set_materials(self):
        bld = os.path.join(REPO, 'models', f'c0-{self.name}.bld')
        s = open(bld).read().split('\n')
        by = {p.name: p.mat for p in self.parts}
        for i, ln in enumerate(s):
            if not ln.startswith('part '):
                continue
            mm = re.search(r'name=(\S+)', ln)
            if not mm or mm.group(1) not in by:
                continue
            mat = self.mats.get(by[mm.group(1)], self.mats.get('main'))
            if not mat:
                continue
            ln = re.sub(r'\s+m=\S+', '', ln)
            s[i] = ln.replace(f'  name={mm.group(1)}', f'  m={mat}  name={mm.group(1)}')
        open(bld, 'w').write('\n'.join(s))

    def report(self):
        mine = os.path.join(REPO, 'export', f'c0-{self.name}.obj')
        rep = os.path.join(REPO, 'tools', 'c0nstruct0r', 'report.py')
        a = subprocess.run([sys.executable, rep, mine], capture_output=True, text=True).stdout
        g = subprocess.run([sys.executable, rep, self.name], capture_output=True, text=True).stdout
        return a, g

    def build(self, what='all'):
        P = self.plan()
        print(f'P {P:.1f} px a cell; {len(self.layout)} regions')
        self.draw()
        self.connect()
        self.run(self.shape_lines())
        for p in self.parts:
            self.run(self.map_lines(p))
        self.run([f'save c0-{self.name}'])
        self.set_materials()
        self.run([f'open c0-{self.name} force'])
        fx = self.fix()
        print('fix', ' '.join(f'{k} {v}' for k, v in fx.items()))
        self.run(['export'])
        print('sheet', self.sheet())
        a, g = self.report()
        print('report (this):', a.strip().split('\n')[-1])
        print('report (game):', g.strip().split('\n')[-1])
        st = subprocess.run(['bash', os.path.join(HERE, 'stage.sh'), self.name], capture_output=True, text=True)
        print('staged' if st.returncode == 0 else 'STAGE FAILED ' + st.stdout[-300:] + st.stderr[-300:])
        self.b.close()
        return fx
