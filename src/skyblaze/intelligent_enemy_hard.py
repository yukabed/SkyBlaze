# SkyBlaze - intelligent enemy, HARD level: its full settings dictionary.
# (lines 92-98 of SkyBlaze_test_1.py, copied unchanged; the meaning of every key
#  is documented in difficulties.py)

INTELLIGENT_ENEMY_HARD = [
    {"name": "HARD", "color": "#ff5252",
     "desc": ["Long memory, sharp predictions, up to 3 divers at once.",
              "14 invaders  -  you may miss only 3."],
     "enemies": 14, "speed": 160, "speed_gain": 0.10, "step_down": 40,
     "max_missed": 3, "memory": 20.0, "dodge_max": 0.65, "dive_gap": (2.5, 4.5),
     "max_divers": 3, "windup": 0.50, "dive_speed": 300, "homing": 200,
     "commit": 170, "predict": 0.90, "spawn_avoid": 0.85},
]
