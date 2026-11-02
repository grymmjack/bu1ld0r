#!/usr/bin/env python3
"""c0nstruct0r's MCP server: bu1ld0r's port as tools Claude can call.

  python3 mcp_server.py [--dir DIR]     (stdio; .mcp.json at the repo starts it)

DIR is bu1ld0r's folder - where it was started with --port and wrote
c0nstruct0r.port (default: the repo this file is in; or $C0NSTRUCT0R_DIR).
Plain Python, nothing to install. The tools:

  bu1ld0r    commands, a line each (the port's: `help` lists them)
  look       a picture of the view (from YAW / PITCH if given), or the game's
             eight views in one sheet
  inspect    status / parts / faces as JSON
  painting   the game's painting of a prop (hd/NAME.png): shown, measured,
             copied to pictures/c0nstruct0r/ for `picture`
  check      the report card: an export against the game's own model

Nothing here writes to the game: exports go to bu1ld0r's export/.
"""
import base64
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rc      # noqa: E402  (the port's connection)
import report  # noqa: E402  (the report card)

GAME = report.GAME
FOLDER = os.environ.get('C0NSTRUCT0R_DIR') or rc.REPO
PROTOCOLS = ('2025-06-18', '2025-03-26', '2024-11-05')

_conn = None


def conn():
    """The connection, made (again) when needed."""
    global _conn
    if _conn is None:
        try:
            _conn = rc.Bu1ld0r(FOLDER)
        except SystemExit as e:  # (rc says why: no port file, turned away)
            raise RuntimeError(str(e) + f' (folder {FOLDER})')
    return _conn


def send(line):
    global _conn
    for attempt in (0, 1):
        try:
            return conn().cmd(line)
        except (OSError, ConnectionError):
            _conn = None  # (bu1ld0r restarted, or let go: once more)
            if attempt:
                raise RuntimeError('bu1ld0r is not answering: is it running with --port?')


def text(s, err=False):
    return {'content': [{'type': 'text', 'text': s}], 'isError': err}


def image_part(path, note=None):
    data = base64.b64encode(open(path, 'rb').read()).decode()
    parts = [{'type': 'image', 'data': data, 'mimeType': 'image/png'}]
    if note:
        parts.insert(0, {'type': 'text', 'text': note})
    return parts


def magick(*args):
    exe = shutil.which('magick') or shutil.which('convert')
    if not exe:
        return None
    r = subprocess.run([exe, *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


# ---------------------------------------------------------------- the tools

def t_bu1ld0r(a):
    out, bad = [], False
    for line in str(a.get('lines', '')).splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        r = send(line)
        out.append(f'> {line}\n{r}')
        if r.startswith('err'):
            bad = True
            out.append('(stopped at the first err)')
            break
    return text('\n'.join(out) or '(no commands)', bad)


def shot(name, how):
    r = send(f'shot {name} {how}'.strip())
    if not r.startswith('ok'):
        raise RuntimeError(r)
    p = r[3:].strip()
    return p if os.path.isabs(p) else os.path.normpath(os.path.join(FOLDER, p))


def t_look(a):
    how = a.get('how', 'view')
    how = '' if how == 'view' else how
    if a.get('eight'):
        st = json.loads(send('status')[3:])
        cam = st['cam']
        files = []
        for f in range(8):
            r = send(f'view {f * 45} 0')
            if not r.startswith('ok'):
                return text(r, True)
            files.append(shot(f'c0look{f}', how or 'clean'))
        send(f"view {cam['yaw']} {cam['pitch']} {cam['dist']}")
        sheet = os.path.join(os.path.dirname(files[0]), 'c0look-eight.png')
        w = int(a.get('size', 320))
        mid = ['-gravity', 'center', '-crop', '64%x72%+0+0', '+repage', '-resize', f'{w}x{w}']  # (the model's framed in the middle)
        ok = magick('(', *files[:4], *mid, '+append', ')',
                    '(', *files[4:], *mid, '+append', ')', '-append', sheet)
        if ok is None:
            parts = []
            for f, p in enumerate(files):
                parts += image_part(p, f'picture {f} (yaw {f * 45})')
            return {'content': parts, 'isError': False}
        return {'content': image_part(sheet, 'the game\'s eight pictures: yaw 0 45 90 135 (top row), '
                                      '180 225 270 315 (bottom); 0 is the front'), 'isError': False}
    if 'yaw' in a or 'pitch' in a:
        st = json.loads(send('status')[3:])
        yaw = a.get('yaw', st['cam']['yaw'])
        pitch = a.get('pitch', st['cam']['pitch'])
        dist = f" {a['dist']}" if 'dist' in a else ''
        r = send(f'view {yaw} {pitch}{dist}')
        if not r.startswith('ok'):
            return text(r, True)
    p = shot(a.get('name', 'c0look'), how)
    return {'content': image_part(p, p), 'isError': False}


def t_inspect(a):
    what = a.get('what', 'status')
    line = {'status': 'status', 'parts': 'parts'}.get(what)
    if what == 'faces':
        line = f"faces {a.get('part', '')}".strip()
    if line is None:
        return text('what: status, parts or faces', True)
    r = send(line)
    return text(r, r.startswith('err'))


def t_painting(a):
    name = a['name']
    src = os.path.join(GAME, 'hd', name + '.png')
    if not os.path.exists(src):
        return text(f'no painting {src}', True)
    props, shapes = report.models_py_tables(os.path.join(GAME, 'models'))
    dst_dir = os.path.join(FOLDER, 'pictures', 'c0nstruct0r')
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, name + '.png')
    if not os.path.exists(dst):
        shutil.copyfile(src, dst)
    size = magick(src, '-format', '%wx%h', 'info:')
    box = magick(src, '-trim', '-format', '%wx%h%O', 'info:')  # (W x H + left + top)
    lines = [f'painting: {src} ({size})',
             f'subject box (transparent edges trimmed): {box}' if box else 'subject box: (magick not found)',
             f'copied to pictures/c0nstruct0r/{name}.png - `picture c0nstruct0r/{name} ...`']
    if name in props:
        lines.append(f'the game\'s height: {props[name]} cells (models.py PROPS)')
    if name in shapes:
        lines.append(f'models.py builds it: {shapes[name]!r}')
    lines.append(f'budget: {report.BUDGET} triangles')
    if a.get('grid') and magick('-version') is not None:
        sheet = os.path.join(dst_dir, name + '-grid.png')
        w, h = (int(v) for v in size.split('x'))
        k = max(1, 768 // max(w, h))
        step = int(a.get('grid'))
        cmds = []
        for x in range(0, w + 1, step):
            cmds.append(f'line {x * k},0 {x * k},{h * k}')
        for y in range(0, h + 1, step):
            cmds.append(f'line 0,{y * k} {w * k},{y * k}')
        magick(src, '-background', '#808080', '-flatten', '-filter', 'point', '-resize', f'{k * 100}%',
               '-fill', 'none', '-stroke', '#0f0', '-draw', ' '.join(cmds), sheet)
        lines.append(f'grid every {step} px (the painting {k}x bigger)')
        return {'content': image_part(sheet, '\n'.join(lines)), 'isError': False}
    return {'content': image_part(src, '\n'.join(lines)), 'isError': False}


def t_check(a):
    name = a['name']
    mine = os.path.join(os.path.expanduser(a.get('folder') or os.path.join(FOLDER, 'export')), name + '.obj')
    if not os.path.exists(mine):
        return text(f'no {mine}: `export` first', True)
    game = a.get('against', name)
    args = [sys.executable, os.path.join(HERE, 'report.py'), mine]
    r = subprocess.run(args, capture_output=True, text=True)
    out = 'this export:\n' + r.stdout
    gp = os.path.join(GAME, 'models', game + '.obj')
    if os.path.exists(gp):
        r2 = subprocess.run([sys.executable, os.path.join(HERE, 'report.py'), game], capture_output=True, text=True)
        out += '\nthe game\'s own:\n' + r2.stdout
    out += '\n(SCORE: higher is worse.)'
    return text(out)


TOOLS = [
    ('bu1ld0r', t_bu1ld0r,
     'Send commands to bu1ld0r (started with --port), a line each; returns each reply ("ok ..." or "err why"), '
     'stopping at the first err. Start with `take` (control), end with `give`. `help` lists the commands; '
     'C0NSTRUCT0R.md has them all.',
     {'lines': {'type': 'string', 'description': 'commands, one a line (# comments skipped)'}}, ['lines']),
    ('look', t_look,
     'A picture of bu1ld0r\'s view. yaw/pitch/dist turn the camera first (yaw 0 = the front; the game\'s '
     'picture f is yaw f x 45, pitch 0). eight=true: the game\'s eight pictures in one sheet, the camera put back.',
     {'yaw': {'type': 'number'}, 'pitch': {'type': 'number'}, 'dist': {'type': 'number'},
      'how': {'type': 'string', 'enum': ['view', 'clean', 'win'],
              'description': 'view: the 3D view (default); clean: the model alone, no outlines; win: the window'},
      'eight': {'type': 'boolean'}, 'size': {'type': 'integer', 'description': 'eight: each picture\'s size (320)'},
      'name': {'type': 'string', 'description': 'shot file name (c0look)'}}, []),
    ('inspect', t_inspect,
     'bu1ld0r\'s state as JSON: status (model, control, selection, camera), parts (every part: kind, place, '
     'size, turns, colour, name), or faces of a part (number, way out, middle, area, corners, picture).',
     {'what': {'type': 'string', 'enum': ['status', 'parts', 'faces']},
      'part': {'type': 'integer', 'description': 'faces: the part (default: the one being edited)'}}, ['what']),
    ('painting', t_painting,
     'The game\'s painting of a prop (neon-caster hd/NAME.png) to rebuild it from: shown, its subject\'s pixel '
     'box, the game\'s height and models.py\'s recipe, the triangle budget; copied to pictures/c0nstruct0r/ '
     'for `picture c0nstruct0r/NAME ...`. grid=N draws a grid every N pixels to measure by.',
     {'name': {'type': 'string'}, 'grid': {'type': 'integer'}}, ['name']),
    ('check', t_check,
     'The report card for an export (bu1ld0r\'s export/NAME.obj) next to the game\'s own model: SMEAR, SIZE, '
     'ANGLE, ASYM, triangles against the budget. Higher SCORE is worse.',
     {'name': {'type': 'string', 'description': 'the export\'s name'},
      'against': {'type': 'string', 'description': 'the game\'s prop to compare with (default: the same name)'},
      'folder': {'type': 'string', 'description': 'where the export is (default: bu1ld0r\'s export/)'}}, ['name']),
]


def handle(msg):
    m, mid = msg.get('method'), msg.get('id')
    if mid is None:
        return None  # (a notification: nothing to answer)
    if m == 'initialize':
        want = msg.get('params', {}).get('protocolVersion')
        res = {'protocolVersion': want if want in PROTOCOLS else PROTOCOLS[0],
               'capabilities': {'tools': {}},
               'serverInfo': {'name': 'c0nstruct0r', 'version': '0.1.0'}}
    elif m == 'ping':
        res = {}
    elif m == 'tools/list':
        res = {'tools': [{'name': n, 'description': d,
                          'inputSchema': {'type': 'object', 'properties': p, 'required': r}}
                         for n, _, d, p, r in TOOLS]}
    elif m == 'tools/call':
        p = msg.get('params', {})
        fn = {n: f for n, f, *_ in TOOLS}.get(p.get('name'))
        if fn is None:
            return {'jsonrpc': '2.0', 'id': mid, 'error': {'code': -32602, 'message': 'no such tool'}}
        try:
            res = fn(p.get('arguments') or {})
        except Exception as e:  # (an answer, not a crash: the caller sees why)
            res = text(f'{type(e).__name__}: {e}', True)
    else:
        return {'jsonrpc': '2.0', 'id': mid, 'error': {'code': -32601, 'message': f'no method {m}'}}
    return {'jsonrpc': '2.0', 'id': mid, 'result': res}


def main(argv):
    global FOLDER
    if '--dir' in argv:
        FOLDER = os.path.expanduser(argv[argv.index('--dir') + 1])
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        out = handle(msg)
        if out is not None:
            sys.stdout.write(json.dumps(out) + '\n')
            sys.stdout.flush()


if __name__ == '__main__':
    main(sys.argv[1:])
