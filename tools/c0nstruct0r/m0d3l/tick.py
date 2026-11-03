#!/usr/bin/python3
"""The overnight checklist's bookkeeping.

  tick.py start NAME                 move NAME into NOW (the box stays open)
  tick.py done NAME "note"           close it (out of NOW, ticked in place, note) and log a
                                     C0NSTRUCT0R.md row from the note
"""
import re
import sys

T = '/home/grymmjack/git/bu1ld0r/.claude/TASKS.md'
C = '/home/grymmjack/git/bu1ld0r/C0NSTRUCT0R.md'
HEAD = '## m0d3l overnight (2026-11-01): staged in export/neon-stage/, not installed'


def main(cmd, name, note=''):
    s = open(T).read()
    now = re.search(r'(## 🔨 NOW - doing right now\n\n)(.*?)(\n\n---)', s, re.S)
    if cmd == 'start':
        s = s.replace(f'\n- [ ] {name}\n', '\n', 1)
        s = s[:now.start(2)] + f'- [ ] ➡️ {name}' + s[now.end(2):]
    elif cmd == 'done':
        s = s[:now.start(2)] + '_(between items)_' + s[now.end(2):]
        # ticked at the end of its section's list: before the next blank line after the heading it was under
        s = s.replace('## Props and machines\n\n', '## Props and machines\n\n', 1)
        s = s.rstrip('\n') + f'\n- [x] {name} - {note}\n' if '## Done tonight' in s else \
            s.rstrip('\n') + f'\n\n## Done tonight\n\n- [x] {name} - {note}\n'
        c = open(C).read()
        if HEAD not in c:
            c = c.rstrip('\n') + f'\n\n{HEAD}\n\n| Model | Notes |\n|---|---|\n'
        c = c.rstrip('\n') + f'\n| c0-{name} | {note} |\n'
        open(C, 'w').write(c)
    open(T, 'w').write(s)


if __name__ == '__main__':
    main(*sys.argv[1:4])
