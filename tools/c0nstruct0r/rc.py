#!/usr/bin/env python3
"""Talk to bu1ld0r's c0nstruct0r port (bu1ld0r started with --port).

  python3 rc.py status                   one command, its reply printed
  python3 rc.py -f steps.txt             a file of commands, a line each
                                         (# comments; stops at the first err)
  python3 rc.py -i                       type commands, see replies
  python3 rc.py --dir DIR ...            bu1ld0r's folder (where it wrote
                                         c0nstruct0r.port): default, the
                                         repo this file is in

Each reply is a line: "ok ..." or "err why". Commands: `help` lists them;
C0NSTRUCT0R.md and bu1ld0r's README say what each does.
"""
import os
import socket
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..'))


class Bu1ld0r:
    """One connection to bu1ld0r's port: cmd() sends a line, returns the reply."""

    def __init__(self, folder=REPO, timeout=60.0):
        self.timeout = timeout
        path = os.path.join(folder, 'c0nstruct0r.port')
        try:
            port, token = open(path).read().split()[:2]
        except (OSError, ValueError):
            raise SystemExit(f'no {path}: start bu1ld0r with --port')
        for _ in range(20):  # (one connection at a time: the last may still be closing)
            try:
                self.sock = socket.create_connection(('127.0.0.1', int(port)), timeout=timeout)
            except ConnectionRefusedError:
                raise SystemExit(f'nothing on port {port}: bu1ld0r has closed ({path} is left over) - start it with --port')
            self.buf = b''
            try:
                r = self.cmd('hello ' + token)
            except ConnectionError:
                r = 'err busy'
            if 'busy' not in r:
                break
            self.sock.close()
            time.sleep(0.25)
        if not r.startswith('ok'):
            raise SystemExit('bu1ld0r said: ' + r)
        self.version = r[3:]

    def cmd(self, line):
        self.sock.sendall(line.strip().encode() + b'\n')
        asking = line.strip().lower().startswith('ask ')
        if asking:  # (the answer waits for Rick's click: as long as it takes)
            self.sock.settimeout(None)
        try:
            return self._reply()
        finally:
            if asking:
                self.sock.settimeout(self.timeout)

    def _reply(self):
        while b'\n' not in self.buf:
            got = self.sock.recv(65536)
            if not got:
                raise ConnectionError('bu1ld0r closed the port')
            self.buf += got
        reply, self.buf = self.buf.split(b'\n', 1)
        return reply.decode(errors='replace').rstrip('\r')

    def close(self):
        self.sock.close()


def main(argv):
    folder = REPO
    if '--dir' in argv:
        i = argv.index('--dir')
        folder = os.path.expanduser(argv[i + 1])
        del argv[i:i + 2]
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    b = Bu1ld0r(folder)
    if argv[0] == '-f':
        for line in open(argv[1]):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            r = b.cmd(line)
            print(f'> {line}\n  {r}')
            if r.startswith('err'):
                return 1
    elif argv[0] == '-i':
        print('bu1ld0r', b.version, '- Ctrl+D ends')
        for line in sys.stdin:
            if line.strip():
                print(b.cmd(line))
    else:
        r = b.cmd(' '.join(argv))
        print(r)
        return 0 if r.startswith('ok') else 1
    b.close()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
