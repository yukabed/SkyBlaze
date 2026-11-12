# SkyBlaze - helpers (asset path + clamp)
# (lines 103-116 of SkyBlaze_test_1.py, copied unchanged)

import os

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def asset(name):
    """Full path of a game file (next to the script, or in the working dir)."""
    path = os.path.join(BASE_DIR, name)
    return path if os.path.exists(path) else os.path.join(os.getcwd(), name)


def clamp(value, low, high):
    return low if value < low else high if value > high else value
