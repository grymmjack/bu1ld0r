#!/usr/bin/python3
"""c0-bigmed's mapping: port lines for every face of every part (regions: atlas.py).

  /usr/bin/python3 tools/c0nstruct0r/m0d3l/bigmed/texture.py [K] [--turn] > texture.txt
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from boxmap import lines  # noqa: E402

K = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 2
ALU, LATCH, WSW, RUB = (200, 0), (200, 64), (200, 80), (0, 216)
TRAY = {'-z': (0, 0), '+z': (0, 47), '+x': (128, 0), '-x': (128, 47), '+y': (128, 144), '-y': (128, 144)}
LID = {'-z': (0, 94), '+z': (0, 119), '+x': (128, 94), '-x': (128, 119), '+y': (0, 144), '-y': (0, 144)}
PARTS = [
    (1, (0.36, 0.13, 0.20), TRAY),
    (2, (0.364, 0.065, 0.204), LID),
    (3, (0.06, 0.016, 0.012), ALU), (4, (0.06, 0.016, 0.012), ALU),
    (5, (0.04, 0.04, 0.0105), {'-z': LATCH, '*': ALU}), (6, (0.04, 0.04, 0.0105), {'-z': LATCH, '*': ALU}),
    (7, (0.02, 0.03, 0.024), ALU), (8, (0.02, 0.03, 0.024), ALU),
    (9, (0.20, 0.018, 0.03), RUB),
] + [(p, (0.05, 0.01, 0.03), RUB) for p in (10, 11, 12, 13)] \
  + [(14, (0.028, 0.09, 0.006), ALU), (15, (0.031, 0.028, 0.006), ALU), (16, (0.031, 0.028, 0.006), ALU)] \
  + [(p, (0.006, 0.07, 0.022), ALU) for p in (17, 20)] \
  + [(p, (0.006, 0.022, 0.024), ALU) for p in (18, 19, 21, 22)]
print('\n'.join(lines(PARTS, P=340, K=K, ref='c0nstruct0r/c0-bigmed', turn='--turn' in sys.argv, dist=0.85)))
