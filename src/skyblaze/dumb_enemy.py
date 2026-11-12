# SkyBlaze - the basic (non-learning) enemy: the Invader body, formation turn-around and 'missed' rule.
# (lines 318-332, 923-926 and 970-980 of SkyBlaze_test_1.py, copied unchanged)

from constants import FORMATION


# ---------------------------------------------------------------------------
# One invader
# ---------------------------------------------------------------------------
class Invader:
    __slots__ = ("t", "x", "y", "mode", "timer", "dv", "dt", "react")

    def __init__(self, turtle_obj):
        self.t = turtle_obj
        self.x = 0.0
        self.y = 0.0
        self.mode = FORMATION
        self.timer = 0.0      # wind-up countdown
        self.dv = 0.0         # sidestep velocity
        self.dt = 0.0         # sidestep time left
        self.react = -1       # id of the last bullet this enemy reacted to


class DumbEnemyMixin:
    def register_miss(self):
        self.missed += 1
        if self.missed >= self.diff["max_missed"]:
            self.end_game()

    def step_down(self):
        """The formation hit a wall: turn around and move down."""
        self.dir = -self.dir
        for inv in self.active:
            if inv.mode == FORMATION:
                inv.y -= self.step_px
                if inv.y < self.lose_y:           # an enemy got past the player
                    self.register_miss()
                    if self.state != "playing":
                        return
                    self.place_invader(inv)
