#!/usr/bin/python3
"""m0d3l helpers: map pictures onto round parts face by face, and build one atlas.

  m0d3l.py faces DIR P > faces.json        a part's faces from a bu1ld0r's port (DIR: its folder;
                                           if the MCP server holds that port - "busy" - save the
                                           MCP `inspect faces` reply to the file instead)
  m0d3l.py wrap faces.json REF X0 Y0 W H N --box X0 X1 Z0 Z1 Y0 Y1 [--part P] [--edge]
        step lines: each outward side face of an N-sided round part (a cylinder, or a
        cylinder made a mesh and extruded / scaled into bands) gets its own column of the
        region X0 Y0 W H of pictures/REF.png - column width W / N, seen head on, so the
        picture wraps round with no seam and every face's pixels are the same size.
        --box is the part's own box (as `picture ... own` uses it). --edge: also the
        `edit P` / `done` round it.

Why per face: `picture REF view YAW RECT own` projects one way, so a round part mapped from
four sides squashes the pixels near each quarter's edge and the quarters don't meet. Seen
head on (yaw = the face's way + 90) each face takes exactly its column; neighbours share the
column edge (to well under a pixel on a tapered band).

Columns run right to left round the part as seen from outside (k = 0 is the face at angle
360 / 2N from +x; column j = -k mod N). Draw stave seams / rivets at the column edges in the
atlas and they land on the part's edges.

Needs /usr/bin/python3 (PIL, numpy) only for the atlas helpers below; wrap is plain Python.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def side_faces(faces, n_sides):
    """The outward side faces: way out mostly level, pointing away from the axis."""
    out = []
    step = 360.0 / n_sides
    for f in faces:
        nx, ny, nz = f['n']
        cx, cy, cz = f['c']
        if abs(ny) > 0.7 or cx * nx + cz * nz <= 0 or math.hypot(cx, cz) < 1e-6:
            continue
        am = math.degrees(math.atan2(nz, nx)) % 360
        k = int(round((am - step / 2) / step)) % n_sides
        out.append((f['f'], k, math.hypot(cx, cz), cy))
    return out


def wrap_lines(faces, ref, x0, y0, w, h, n_sides, box, cx=0.0, cz=0.0):
    """picture lines for each side face (box: x0 x1 z0 z1 y0 y1 of the part)."""
    bx0, bx1, bz0, bz1, by0, by1 = box
    step = 360.0 / n_sides
    d = math.radians(step / 2)
    col = w / n_sides
    lines = []
    for f, k, dist, _ in side_faces(faces, n_sides):
        am = (k + 0.5) * step
        yaw = am + 90
        rx, rz = -math.cos(math.radians(yaw)), -math.sin(math.radians(yaw))
        qs = [x * rx + z * rz for x in (bx0, bx1) for z in (bz0, bz1)]
        q0, q1 = min(qs), max(qs)
        qq = q1 - q0
        r = dist / math.cos(d)               # the face's middle radius from its centre
        # the axis may be off the origin: shift a by the axis's own projection
        a_ax = cx * rx + cz * rz
        a_left = a_ax - r * math.sin(d)      # (angle am + d: the left edge as seen)
        j = (-k) % n_sides
        u_left = x0 + j * col
        s = col * qq / (2 * r * math.sin(d))
        sx0 = u_left - (a_left - q0) / qq * s
        sx1 = sx0 + s
        lines.append(f'pick {f}')
        lines.append(f'picture {ref} view {yaw % 360:.4f} {sx0:.4f} {y0:.4f} {sx1:.4f} {y0 + h:.4f} own')
    return lines


def wrap_main(argv):
    if len(argv) < 7 or '--box' not in argv:
        raise SystemExit(__doc__)
    bi = argv.index('--box')
    box = [float(v) for v in argv[bi + 1:bi + 7]]
    part = None
    if '--part' in argv:
        part = int(argv[argv.index('--part') + 1])
    edge = '--edge' in argv
    fj, ref, x0, y0, w, h, n = argv[:7]
    txt = open(fj).read().strip()
    if txt.startswith('ok '):              # (pasted straight from `faces P` / the MCP inspect)
        txt = txt[3:]
    faces = json.loads(txt)
    cx = (box[0] + box[1]) / 2
    cz = (box[2] + box[3]) / 2
    if abs(cx) > 1e-9 or abs(cz) > 1e-9:
        faces = [dict(f, c=[f['c'][0] - cx, f['c'][1], f['c'][2] - cz]) for f in faces]
        box = [box[0] - cx, box[1] - cx, box[2] - cz, box[3] - cz, box[4], box[5]]
    lines = wrap_lines(faces, ref, float(x0), float(y0), float(w), float(h), int(n), box)
    if edge and part:
        lines = [f'edit {part}'] + lines + ['done']
    print('\n'.join(lines))


def faces_main(argv):
    from rc import Bu1ld0r
    folder, part = argv[0], argv[1]
    b = Bu1ld0r(os.path.expanduser(folder))
    b.cmd('take')
    r = b.cmd(f'faces {part}')
    if not r.startswith('ok '):
        raise SystemExit(r)
    print(r[3:])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == 'wrap':
        wrap_main(rest)
    elif cmd == 'faces':
        faces_main(rest)
    else:
        raise SystemExit(__doc__)
