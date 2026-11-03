#!/usr/bin/python3
"""c0-barrel-water-wreck: see ../barrels.py (one spec for all ten coloured barrels)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from barrels import make  # noqa: E402

if __name__ == '__main__':
    make('water', True, HERE).build()
