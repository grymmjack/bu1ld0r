#!/usr/bin/python3
"""c0-safe-open: c0-safe looted - the game swaps it in where the safe stood. Split vault doors
swung open (bolt mechanism inside), a lit cave: a shelf of cash bundles, gold bars on the floor."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'safe'))
from looks import paint, steel, glow, front_box  # noqa: E402
import build as safe  # noqa: E402  (c0-safe's parts and painters)

CYAN = safe.CYAN
m, body = safe.make('safe-open', 63, opened=True)
m.name = 'safe-open'
body.cut('-z', (-0.16, 0.16, 0.13, 0.43), 0.29)
drawer = m.box('drawer', (0, 0.045, -0.186), (0.30, 0.07, 0.02), '24272C')
doors = [m.box(f'door-{i}', (x, 0.13, -0.256), (0.02, 0.30, 0.16), '2A2E34') for i, x in enumerate((0.17, -0.17))]
m.box('shelf', (0, 0.27, -0.03), (0.32, 0.01, 0.28), '30343A', paint='steel')
for i, x in enumerate((-0.11, -0.04, 0.03)):
    m.box(f'cash-{i}', (x, 0.28, -0.05), (0.06, 0.035 - i * 0.008, 0.09), '3C8048', paint={'-z': 'cashend', '+z': 'cashend', '*': 'cash'})
for i, (x, y, z) in enumerate(((0.08, 0.13, -0.06), (0.02, 0.13, -0.06), (0.05, 0.155, -0.06), (-0.09, 0.13, 0.0))):
    m.box(f'gold-{i}', (x, y, z), (0.055, 0.025, 0.1), 'E0B040', paint='gold')
m.box('case', (0.09, 0.28, 0.02), (0.08, 0.07, 0.06), '1A1C20', paint={'-z': 'casefront', '*': 'casebody'})


def front(a, w, h):
    img = paint(safe.BODY, 0.5)(a, w, h)
    s = front_box(body, w, h, -0.16, 0.16, 0.13, 0.43)
    a.rect(img, s, (34, 38, 44))                                       # the cave's back wall
    a.rect(img, (s[0], s[1] - 3, s[2], s[1] - 1.8), CYAN)
    return glow(img, a, (s[0], s[1] - 3, s[2], s[1] - 1.8), CYAN, 0.2, 2)


def door_out(a, w, h):
    """A door's outside (now facing sideways): armour plate, half the ring lock's bezel."""
    img = paint('2A2E34', 0.5)(a, w, h)
    a.rect(img, (w * 0.06, h * 0.05, w * 0.94, h * 0.95), (36, 40, 46))
    a.rect(img, (w * 0.06, h * 0.05, w * 0.94, h * 0.05 + 0.7), (74, 80, 88))
    for v in (0.12, 0.5, 0.88):
        a.rect(img, (w * 0.12 - 1, h * v - 1, w * 0.12 + 1, h * v + 1), (120, 126, 134))
    a.rect(img, (w * 0.86, h * 0.1, w * 0.92, h * 0.9), CYAN)            # the door's edge light
    return glow(img, a, (w * 0.86, h * 0.1, w * 0.92, h * 0.9), CYAN, 0.18, 1)


def door_in(a, w, h):
    """A door's inside: the bolt mechanism - a rail, four steel bolts out at the free edge."""
    img = paint('202328', 0.4)(a, w, h)
    a.rect(img, (w * 0.3, h * 0.08, w * 0.42, h * 0.92), (90, 96, 104))   # rail
    for k in range(4):
        y = h * (0.15 + k * 0.23)
        a.rect(img, (w * 0.3, y, w * 0.98, y + h * 0.06), (176, 182, 190))
        a.rect(img, (w * 0.3, y + h * 0.05, w * 0.98, y + h * 0.06), (90, 96, 104))
    a.rect(img, (w * 0.5, h * 0.4, w * 0.75, h * 0.6), (30, 33, 38))     # gearbox
    a.rect(img, (w * 0.55, h * 0.45, w * 0.6, h * 0.48), (90, 240, 120))
    return img


def cave(a, w, h):
    img = paint('22252A', 0.3, 1)(a, w, h)
    a.rect(img, (0, 0, w, 1.6), (130, 240, 235))                         # the lit strip round the top
    return glow(img, a, (0, 0, w, 1.6), CYAN, 0.25, 2)


def cash(a, w, h):
    img = paint((70, 130, 80), 0.2, 1)(a, w, h)
    for k in range(0, int(h), 2):
        a.rect(img, (0, k, w, k + 0.4), (40, 80, 50))
    a.rect(img, (w * 0.4, 0, w * 0.6, h), (220, 210, 170))              # the band
    return img


def cashend(a, w, h):
    img = cash(a, w, h)
    for k in range(0, int(h), 1):
        a.rect(img, (0, k, w, k + 0.35), (200, 220, 190), 0.5)
    return img


def case_front(a, w, h):
    img = paint('1A1C20', 0.3)(a, w, h)
    a.rect(img, (w * 0.15, h * 0.3, w * 0.85, h * 0.7), (40, 44, 50))
    a.rect(img, (w * 0.4, h * 0.42, w * 0.6, h * 0.58), (240, 70, 200))  # a data case's lock light
    return glow(img, a, (w * 0.4, h * 0.42, w * 0.6, h * 0.58), (240, 70, 200), 0.2, 1)


def gold(a, w, h):
    img = steel((236, 190, 80))(a, w, h)
    return a.edge_dark(img, 1.5, 0.7)


body.paint = {'-z': front, '+z': 'back', '*': 'side'}
drawer.paint = {'-z': safe.drawer_front, '*': 'side'}
doors[0].paint = {'+x': 'doorout', '-x': 'doorin', '*': 'doorside'}
doors[1].paint = {'-x': 'doorout', '+x': 'doorin', '*': 'doorside'}
m.swatch('side', paint(safe.BODY, 0.5))
m.swatch('back', safe.back)
m.swatch('cave', cave)
m.swatch('post', paint(safe.POST, 0.5))
m.swatch('postfront', safe.post_front)
m.swatch('flank', safe.flank)
m.swatch('plinth', paint('15171A', 0.3))
m.swatch('doorout', door_out)
m.swatch('doorin', door_in)
m.swatch('doorside', paint('2A2E34', 0.5))
m.swatch('steel', steel((120, 126, 134)))
m.swatch('cash', cash)
m.swatch('cashend', cashend)
m.swatch('gold', gold)
m.swatch('casebody', paint('1A1C20', 0.3))
m.swatch('casefront', case_front)

if __name__ == '__main__':
    m.build()
