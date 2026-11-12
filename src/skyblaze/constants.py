# SkyBlaze - constants
# (lines 40-63 of SkyBlaze_test_1.py, copied unchanged)

import sys

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
STEP = 1.0 / 60.0            # fixed physics step (seconds)
SAMPLE = 0.1                 # how often the enemy AI "watches" the player (s)
NB = 24                      # number of horizontal lanes the AI memorises
MEMORY_KEEP = 0.5            # share of the AI's knowledge kept between rounds
SPEED_CAP = 3.0              # enemies never get faster than 3x their base speed

FORMATION, WINDUP, DIVE = 0, 1, 2     # enemy modes

ENEMY_RADIUS_SQ = 25 * 25    # bullet <-> enemy collision (same 25 px as before)
PLAYER_RADIUS_SQ = 30 * 30   # player <-> enemy collision (same 30 px as before)
DODGE_TRIGGER = 30.0         # how close to the bullet's lane an enemy must be
DODGE_SPEED = 480.0          # px/s of a sidestep
DODGE_TIME = 0.16            # seconds a sidestep lasts

MOVE_LEFT = ("Left", "a", "A")
MOVE_RIGHT = ("Right", "d", "D")
LEFT_SET = frozenset(MOVE_LEFT)
RIGHT_SET = frozenset(MOVE_RIGHT)
# X11 sends fake "release + press" pairs while a key auto-repeats; a tiny grace
# period on release keeps the movement smooth there.
RELEASE_GRACE_MS = 35 if sys.platform.startswith("linux") else 0
