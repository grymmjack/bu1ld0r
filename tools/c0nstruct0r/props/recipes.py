"""c0nstruct0r recipes: props rebuilt with stepgen (each writes props/NAME.txt).

    python3 tools/c0nstruct0r/props/recipes.py [NAME...]      (default: all)

Pixel numbers are the game's painting (hd/NAME.png, 256 x 256), measured on a
16-pixel grid. Earlier props (alarmpc ... tank) were written by hand-made
scripts; their .txt files are the record.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from stepgen import Steps  # noqa: E402

R = {}


def recipe(f):
    R[f.__name__.replace('_', '-')] = f
    return f


@recipe
def crate():
    s = Steps('crate', 0.42, (244, 214, 4, 18), 'a wooden crate, strapped, its lid a band of its own')
    s.say('the box, 0.38 deep; the lid a touch bigger, so its edge shows')
    body = s.add('box', 10, 120, 238, 226, d=0.38, col='8A5A30', name='body')
    lid = s.add('box', 5, 17, 243, 120, d=0.40, col='A8743C', name='lid')
    s.say('pictures: each from its own patch of the painting, inside the rounded outline; the lid top its planks')
    s.pics(body, front='14 122 234 224', side='14 130 120 222', bottom='4A3018')
    s.pics(lid, front='12 24 236 118', side='12 24 120 110', top='12 24 236 100')
    return s


@recipe
def locker():
    s = Steps('locker', 0.9, (227, 236, 16, 20), 'three lockers in a row - blue, grey, blue - vents at the top')
    cols = [(17, 96, '1E5A8A', 'blue'), (96, 165, '8A929A', 'grey'), (165, 241, '1E5A8A', 'blue')]
    ps = []
    for i, (a, b, c, nm) in enumerate(cols):
        s.say(f'locker {i + 1}: {nm}')
        p = s.add('box', a, 20, b, 250, d=0.4, col=c, name=f'locker-{i + 1}')
        s.recess(p, a + 14, 34, b - 14, 76, 0.015, why='its vents, pressed in')
        ps.append((p, a, b, c))
    s.say('pictures: each front its own column of the painting; the ends a slice of its door; tops and backs plain')
    for p, a, b, c in ps:
        s.pics(p, front=f'{a + 2} 22 {b - 2} 249', back='1A2A3A', side='20 100 60 245', top='2A3A4A', bottom='1A2A3A')
    return s


@recipe
def vending():
    s = Steps('vending', 0.8, (118, 236, 67, 8), 'a vending machine: a silver body with a pink side, a cyan cap, a window of snacks, a slot, a keypad, four feet')
    body = s.add('box', 71, 55, 165, 232, d=0.35, col='B8C0C8', name='body')
    s.recess(body, 85, 60, 143, 160, 0.03, why='the snack window, set in')
    cap = s.add('box', 68, 10, 170, 57, d=0.37, col='3AD8E0', name='cap')
    s.say('four feet')
    feet = [s.add('box', a, 230, a + 8, 243, d=0.04, z=z, col='3AD8E0', name=f'foot-{i}')
            for i, (a, z) in enumerate(((80, -0.13), (80, 0.13), (156, -0.13), (156, 0.13)))]
    s.say('the keypad on its right side')
    key = s.add('box', 165, 90, 175, 135, d=0.05, z=-0.08, col='8A929A', name='keypad')
    s.say('pictures: the front from the painting; the sides pink and silver as its right edge shows')
    s.pics(body, side='E85AA0', back='8A929A', top='B8C0C8', bottom='3A3E44')
    s.pics(cap, side='3AD8E0', back='E85AA0', top='3AD8E0', bottom='3AD8E0')
    for f in feet:
        s.pics(f, side='3AD8E0', back='3AD8E0')
    s.pics(key, front='175 90 185 135', side='175 90 185 135', back='8A929A', top='8A929A')
    return s


@recipe
def bookshelf():
    s = Steps('bookshelf', 0.95, (204, 203, 26, 53), 'a bookshelf: a dark frame, five rows of books, glowing bits among them')
    fr = s.add('box', 27, 53, 230, 256, d=0.32, col='2A2A30', name='frame')
    s.recess(fr, 34, 64, 222, 248, 0.25, k=0.05, why='the shelves: the front cut in deep, the books on the back wall')
    s.say('four boards across it, in front of the books')
    boards = [s.add('box', 34, y, 222, y + 4, d=0.25, z=-0.025, col='3A3A44', name=f'board-{i + 1}')
              for i, y in enumerate((99, 140, 175, 210))]
    s.say('pictures: the front and the books from the painting; the frame outside plain dark')
    s.pics(fr, back='1E1E24', side='2A2A30', top='3A3240', bottom='1E1E24')
    for b in boards:
        s.pics(b, back=None, side='3A3A44', top='4A4A54', bottom='2A2A30')
    return s


@recipe
def safe():
    s = Steps('safe', 0.55, (204, 224, 26, 32), 'a safe, its door open: a thick dark frame, a glowing ring and a drawer inside')
    body = s.add('box', 27, 33, 234, 256, d=0.45, col='2A2E34', name='body')
    s.recess(body, 51, 57, 211, 233, 0.14, k=0.05, why='the inside: the front cut in, the ring and drawer on its back wall')
    s.pics(body, back='1E2228', side='2A2E34', top='3A4048', bottom='1E2228')
    return s


@recipe
def terminal():
    s = Steps('terminal', 0.55, (256, 256, 0, 0), 'a beige terminal: a screen unit on a keyboard unit that juts out in front')
    low = s.add('box', 0, 160, 256, 256, d=0.40, col='D8A870', name='keyboard-unit')
    s.recess(low, 28, 177, 161, 227, -0.01, why='its keys, raised')
    up = s.add('box', 2, 0, 254, 160, d=0.30, z=0.05, col='D8A870', name='screen-unit')
    s.recess(up, 15, 30, 241, 83, 0.02, why='the screen, set in')
    s.say('pictures: the fronts from the painting; sides from its beige panels; tops and backs plain')
    s.pics(low, side='0 165 60 250', back='C89860', top='D8A870', bottom='8A6A40')
    s.pics(up, side='0 90 60 150', back='C89860', top='D8A870', bottom='8A6A40')
    return s


@recipe
def terminal_broken():
    s = Steps('terminal-broken', 0.55, (217, 208, 19, 48), 'a broken old monitor, a keyboard in front of it')
    crt = s.add('box', 55, 50, 212, 256, d=0.30, z=0.04, col='1E1A1E', name='monitor')
    s.recess(crt, 90, 83, 187, 177, 0.02, why='the screen, set into its bezel')
    s.say('the keyboard: thin, lying in front')
    kb = s.add('box', 80, 247, 236, 256, d=0.12, z=-0.17, col='2A2A2E', name='keyboard')
    s.pics(crt, back='141014', side='1E1A1E', top='2A242A', bottom='141014')
    s.pics(kb, front='85 232 236 240', back='2A2A2E', side='2A2A2E', top='85 205 230 240')
    return s


@recipe
def console():
    s = Steps('console', 0.5, (206, 196, 25, 60), 'a console: a grey cabinet, a deck of screens and buttons over it, a red beacon on a post')
    cab = s.add('box', 36, 173, 219, 256, d=0.32, col='4A525C', name='cabinet')
    deck = s.add('box', 27, 113, 224, 173, d=0.36, col='5A6470', name='deck')
    s.say('the beacon: a post, a red light, a thin antenna')
    post = s.add('cylinder', 206, 110, 222, 113, d=None, col='3A3E44', name='beacon-base', extra='seg=10')
    light = s.add('sphere', 205, 90, 223, 112, col='E82A2A', name='beacon', extra='seg=10')
    ant = s.add('cylinder', 212.5, 60, 215.5, 90, col='C8D0D8', name='antenna', extra='seg=6')
    s.pics(cab, side='40 180 100 250', back='3A4048', top='4A525C', bottom='2A2E34')
    s.pics(deck, side='5A6470', back='4A525C', top='6A7480', bottom='3A4048')
    s.pics(post, round_=True, front='206 110 222 113', top='3A3E44')
    s.pics(light, round_=True, front='207 92 221 110')
    s.pics(ant, round_=True, front='213 62 215 88')
    return s


@recipe
def rack():
    s = Steps('rack', 0.9, (128, 233, 64, 11), 'a server rack: a grey frame, a vent and an orange bar on top, glowing lights inside, four feet')
    body = s.add('box', 67, 13, 190, 225, d=0.45, col='6A7078', name='rack')
    s.recess(body, 75, 63, 181, 213, 0.30, k=0.05, why='its open front: cut in deep, the lights on the back wall')
    feet = [s.add('box', a, 223, a + 14, 243, d=0.05, z=z, col='2A2E34', name=f'foot-{i}')
            for i, (a, z) in enumerate(((69, -0.19), (69, 0.19), (168, -0.19), (168, 0.19)))]
    s.pics(body, back='4A5058', side='6A7078', top='5A6068', bottom='3A3E44')
    for f in feet:
        s.pics(f, side='2A2E34', back='2A2E34')
    return s


if __name__ == '__main__':
    names = sys.argv[1:] or list(R)
    for n in names:
        print(R[n]().end())
