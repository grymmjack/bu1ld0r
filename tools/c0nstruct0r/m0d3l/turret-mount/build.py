#!/usr/bin/python3
"""c0-turret-mount: see ../turrets.py (the turret's parts, the whole turret and its plates)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from turrets import make  # noqa: E402

if __name__ == '__main__':
    make('mount', HERE).build()
