"""c0nstruct0r's step writer: a prop's port commands from measurements in its painting.

    from stepgen import Steps
    s = Steps('crate', 0.42, (244, 214, 4, 18), 'a wooden crate')   # height, subject W H LEFT TOP
    body = s.add('box', 10, 100, 244, 232, d=0.4, col='8A5A30', name='body')  # painting pixels
    s.pics(body, side='4 110 124 230', top='10 30 240 100')
    s.end()        # writes tools/c0nstruct0r/props/crate.txt

Parts are given as pixel boxes of the painting (px0 py0 px1 py1): the model's
x = 0 is the subject's middle (the painting's right is -x), y = 0 its foot.
`pics` maps each part's faces: the front from the painting as seen (or a
patch, `front=RECT`, over the part's own box), the back the front mirrored
(or `back='RRGGBB'` / a RECT), sides and top from patches (`own`) or plain
colours. Run the .txt with rc.py (bu1ld0r --port).
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def _is_col(v):
    return isinstance(v, str) and len(v) == 6 and all(c in '0123456789abcdefABCDEF' for c in v)


def _mirror(rect):
    x0, y0, x1, y1 = rect.split()
    return f'{x1} {y0} {x0} {y1}'


class Steps:
    def __init__(self, name, height, box, what, pace=400):
        w, h, left, top = box
        self.N, self.P = name, f'c0nstruct0r/{name}'
        self.k = height / h            # cells a pixel
        self.cx = left + w / 2
        self.bot = top + h
        self.FR = f'{left} {top} {left + w} {top + h}'
        self.L, self.n, self.parts = [], 0, {}
        a = self.L.append
        a(f'# c0nstruct0r: {name}, rebuilt from hd/{name}.png ({height} tall; subject {w}x{h} at +{left}+{top})')
        a(f'# run: python3 tools/c0nstruct0r/rc.py -f tools/c0nstruct0r/props/{name}.txt'
          f'  (bu1ld0r started with --port; needs pictures/c0nstruct0r/{name}.png)')
        a('take')
        a(f'pace {pace}')
        a(f'say {name}: {what}')
        a('new force')

    # painting pixels -> cells
    def X(self, px): return round((self.cx - px) * self.k, 4)
    def Y(self, py): return round((self.bot - py) * self.k, 4)
    def W(self, n): return round(n * self.k, 4)

    def say(self, t): self.L.append(f'say {t}')
    def raw(self, *lines): self.L.extend(lines)

    def add(self, kind, px0, py0, px1, py1, d=None, z=0.0, col='808080', name='', extra='', y0=None):
        """A part filling that pixel box (d: its depth, the width if not given)."""
        w = self.W(px1 - px0)
        y = self.Y(py1) if y0 is None else y0
        h = round(self.Y(py0) - y, 4)
        if h <= 0 or w <= 0:
            raise ValueError(f'{name}: no size ({w} x {h}) - py0 must be above py1')
        d = w if d is None else d
        self.L.append(f'add {kind} {self.X((px0 + px1) / 2)} {y} {round(z, 4)} {w} {h} {round(d, 4)} '
                      f'{extra + " " if extra else ""}col={col} name={name}')
        self.n += 1
        self.parts[self.n] = (px0, py0, px1, py1)
        return self.n

    def recess(self, p, px0, py0, px1, py1, depth, k=0.1, why=''):
        """Part p's front cut in where that pixel box is: inset, shrunk and moved there, pushed in."""
        a0, b0, a1, b1 = self.parts[p]
        fw, fh = a1 - a0, b1 - b0
        inner = 1 - k
        sx = round(((px1 - px0) / fw) / inner, 4)
        sy = round(((py1 - py0) / fh) / inner, 4)
        mx = round((((a0 + a1) / 2) - ((px0 + px1) / 2)) * self.k, 4)
        my = round((((b0 + b1) / 2) - ((py0 + py1) / 2)) * self.k, 4)
        if why:
            self.say(why)
        self.raw(f'edit {p}', 'pick facing 0 0 -1', f'inset {k}', f'scale {sx} {sy} 1',
                 f'move {mx} {my} 0', f'extrude {-depth}', 'done')

    def pics(self, p, front=None, round_=False, back=True, side=None, top=None, bottom=None, deg=45):
        """Part p's pictures. front: None = the painting as seen (the model's box), a RECT = that
        patch over p's own box. back: True = the front mirrored, a colour, a RECT, or None.
        side / top / bottom: a RECT (own patch; sides mirrored for -x) or a colour."""
        a = self.L.append
        a(f'edit {p}')
        fd = 90 if round_ else deg
        if front:
            fr, own = front, ' own'
        else:
            fr, own = self.FR, ''
        a(f'pick facing 0 0 -1 {fd}')
        a(f'picture {self.P} view 0 {fr}{own}')
        bd = 89.9 if round_ else deg
        if back is True:
            a(f'pick facing 0 0 1 {bd}')
            a(f'picture {self.P} view 180 {_mirror(fr)}{own}')
        elif _is_col(back):
            a(f'pick facing 0 0 1 {bd}')
            a(f'colour {back}')
        elif back:
            a(f'pick facing 0 0 1 {bd}')
            a(f'picture {self.P} view 180 {back} own')
        if not round_:
            if _is_col(side):
                a('pick facing 1 0 0')
                a('pick add facing -1 0 0')
                a(f'colour {side}')
            elif side:
                a('pick facing 1 0 0')
                a(f'picture {self.P} view 90 {side} own')
                a('pick facing -1 0 0')
                a(f'picture {self.P} view 270 {_mirror(side)} own')
        if _is_col(top):
            a('pick facing 0 1 0 30')
            a(f'colour {top}')
        elif top:
            a('pick facing 0 1 0 30')
            a(f'picture {self.P} top {top} own')
        if _is_col(bottom):
            a('pick facing 0 -1 0 30')
            a(f'colour {bottom}')
        a('done')

    def end(self, folder=None):
        a = self.L.append
        a('sel none')
        a('say done - the eight views the game makes')
        a('view 0 0')
        a('look all')
        for f in range(8):
            a(f'view {f * 45} 0')
            a(f'shot {self.N}{f} clean')
        a('view 25 18')
        a(f'save c0-{self.N}')
        a('export')
        a('give')
        out = os.path.join(folder or os.path.join(HERE, 'props'), self.N + '.txt')
        with open(out, 'w') as f:
            f.write('\n'.join(self.L) + '\n')
        return out
