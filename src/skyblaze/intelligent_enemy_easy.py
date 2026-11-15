# SkyBlaze - intelligent enemy, EASY level: its full settings dictionary.
# (lines 78-84 of SkyBlaze_test_1.py, copied unchanged; the meaning of every key
#  is documented in difficulties.py)

INTELLIGENT_ENEMY_EASY = [
    {"name": "EASY", "color": "#3ddc84",
     "desc": ["Slow, forgetful enemies that rarely dodge or dive.",
              "8 invaders  -  you may miss up to 8."],
     "enemies": 8, "speed": 80, "speed_gain": 0.04, "step_down": 28,
     "max_missed": 8, "memory": 6.0, "dodge_max": 0.20, "dive_gap": (7.0, 11.0),
     "max_divers": 1, "windup": 0.90, "dive_speed": 170, "homing": 90,
     "commit": 300, "predict": 0.30, "spawn_avoid": 0.35},
]
