#!/usr/bin/python3
"""c0-alarm (and c0-alarm-off: `build.py off`): a wall alarm box - a red back plate in a yellow
safety frame with a pipe run, a grey face plate, a big red push button, a black key switch, a
warning lamp, a yellow label strip. Off: the button dark, the lamp out, the frame dimmer. The
game's is 0.24 x 0.27 x 0.03 cells."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from m0kit import Model  # noqa: E402
from looks import paint, steel, glow  # noqa: E402

OFF = len(sys.argv) > 1 and sys.argv[1] == 'off'
NAME = 'alarm-off' if OFF else 'alarm'
RED = (120, 30, 34) if OFF else (200, 36, 40)
YEL = (170, 130, 30) if OFF else (240, 190, 30)
BTN = (90, 40, 44) if OFF else (235, 40, 44)
m = Model(NAME, os.path.join(HERE, '..', NAME), seed=95 if not OFF else 97)
m.material('main', 'paint')
back = m.box('back', (0, 0, 0.002), (0.236, 0.27, 0.024), 'C82428')
face = m.box('face', (0, 0.045, -0.016), (0.15, 0.13, 0.012), '8A9098')
m.box('button', (-0.033, 0.1, -0.028), (0.06, 0.06, 0.012), 'EB282C', paint={'-z': 'btnface', '*': 'btnside'})
m.box('key', (0.042, 0.088, -0.026), (0.03, 0.04, 0.008), '18191C', paint={'-z': 'keyface', '*': 'dark'})
m.box('lamp', (0.042, 0.142, -0.026), (0.018, 0.018, 0.008), 'E02020', paint='lamp')
m.box('pipe', (0, 0.215, -0.016), (0.16, 0.014, 0.014), 'A0A6AE', paint='pipe')


def back_front(a, w, h):
    img = paint(RED, 0.5)(a, w, h)
    for k in range(8):                                                 # circuit lines in the red
        y = h * (0.12 + k * 0.1)
        a.rect(img, (w * 0.1, y, w * 0.9, y + 0.5), tuple(int(v * 0.7) for v in RED))
    for t in (2, 3.2):                                                 # the yellow safety frame
        a.rect(img, (t, t, w - t, t + 0.9), YEL)
        a.rect(img, (t, h - t - 0.9, w - t, h - t), YEL)
        a.rect(img, (t, t, t + 0.9, h - t), YEL)
        a.rect(img, (w - t - 0.9, t, w - t, h - t), YEL)
    for x, y in ((5.5, 5.5), (w - 5.5, 5.5), (5.5, h - 5.5), (w - 5.5, h - 5.5)):
        a.rect(img, (x - 1, y - 1, x + 1, y + 1), (60, 64, 70))
    return a.edge_dark(img, 1.5, 0.6)


def face_front(a, w, h):
    img = steel((150, 156, 164))(a, w, h)
    img = a.edge_dark(img, 1.2, 0.6)
    a.rect(img, (0, h * 0.72, w, h * 0.86), YEL)                        # the label strip
    img = a.text(img, 'PUSH IN EMERGENCY', h * 0.1, (w * 0.06, h * 0.73, w * 0.94, h * 0.85), (30, 30, 30))
    return img


def btn_face(a, w, h):
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array((40, 40, 44), np.float32)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    img[d < 0.95] = np.array(BTN) * 0.6
    img[d < 0.85] = BTN
    hi = np.hypot(xx - w * 0.38, yy - h * 0.36) / (w / 2) < 0.25
    img[hi & (d < 0.85)] = np.minimum(np.array(BTN) + 70, 255)
    if not OFF:
        img = glow(img, a, (w * 0.1, h * 0.1, w * 0.9, h * 0.9), (255, 60, 60), 0.12, 1)
    return img


def key_face(a, w, h):
    img = paint('18191C', 0.2)(a, w, h)
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]] / a.K
    d = np.hypot(xx - w / 2, yy - h * 0.4)
    img[d < w * 0.35] = (60, 62, 66)
    img[(np.abs(xx - w / 2) < 0.6) & (d < w * 0.3)] = (10, 10, 12)
    return img


def lamp(a, w, h):
    c = (70, 20, 20) if OFF else (255, 60, 50)
    img = np.ones((a.px(h), a.px(w), 3), np.float32) * np.array(c, np.float32)
    a.rect(img, (w * 0.2, h * 0.2, w * 0.5, h * 0.5), tuple(min(255, v + 80) for v in c))
    return img


back.paint = {'-z': back_front, '+z': 'backplate', '*': 'redside'}
face.paint = {'-z': face_front, '*': 'faceside'}
m.swatch('redside', paint(RED, 0.4))
m.swatch('backplate', paint('3A3D42', 0.5))
m.swatch('faceside', steel((120, 126, 134)))
m.swatch('btnface', btn_face)
m.swatch('btnside', paint(tuple(int(v * 0.7) for v in BTN), 0.2, 1))
m.swatch('keyface', key_face)
m.swatch('dark', paint('18191C', 0.2))
m.swatch('lamp', lamp)
m.swatch('pipe', lambda a, w, h: a.edge_dark(steel((160, 166, 174))(a, w, h), 0.8, 0.6))

if __name__ == '__main__':
    m.build()
