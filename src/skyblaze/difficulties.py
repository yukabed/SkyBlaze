# SkyBlaze - difficulty table: joins the three intelligent-enemy settings files.
# (lines 65-76 and 100 of SkyBlaze_test_1.py, copied unchanged)

from intelligent_enemy_easy import INTELLIGENT_ENEMY_EASY
from intelligent_enemy_hard import INTELLIGENT_ENEMY_HARD
from intelligent_enemy_normal import INTELLIGENT_ENEMY_NORMAL

# Per-difficulty settings.
#   enemies / speed / speed_gain / step_down / max_missed : classic game rules
#   memory      : half-life (s) of what the enemy AI remembers about you
#   dodge_max   : max chance that an enemy dodges a bullet fired from a lane
#                 it has learned (scaled by how predictable your lane is)
#   dive_gap    : seconds between enemy dive attacks (min, max)
#   max_divers  : enemies allowed to dive at the same time
#   windup      : seconds an enemy wiggles (warning) before it dives
#   dive_speed / homing / commit : dive fall speed, sideways homing speed and the
#                 distance to the player at which it stops homing (dodgeable)
#   predict     : how much the AI trusts its prediction of your next moves
#   spawn_avoid : how strongly new enemies avoid the lanes you favour
DIFFICULTIES = INTELLIGENT_ENEMY_EASY + INTELLIGENT_ENEMY_NORMAL + INTELLIGENT_ENEMY_HARD
MAX_ENEMIES = max(d["enemies"] for d in DIFFICULTIES)
