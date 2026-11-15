# SkyBlaze - intelligent enemy, NORMAL level (called MEDIUM in the game): its full settings dictionary.
# (lines 85-91 of SkyBlaze_test_1.py, copied unchanged; the meaning of every key
#  is documented in difficulties.py)

INTELLIGENT_ENEMY_NORMAL = [
    {"name": "MEDIUM", "color": "#ffc107",
     "desc": ["Enemies learn your lanes and habits within seconds.",
              "10 invaders  -  you may miss up to 5."],
     "enemies": 10, "speed": 115, "speed_gain": 0.07, "step_down": 34,
     "max_missed": 5, "memory": 12.0, "dodge_max": 0.40, "dive_gap": (4.5, 7.5),
     "max_divers": 2, "windup": 0.70, "dive_speed": 230, "homing": 140,
     "commit": 230, "predict": 0.60, "spawn_avoid": 0.60},
]
