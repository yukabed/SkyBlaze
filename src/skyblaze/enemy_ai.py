# SkyBlaze - intelligent-enemy behaviour (spawn avoidance, aiming, sampling, dive attacks).
# (lines 876-901 and 928-968 of SkyBlaze_test_1.py, copied unchanged)

import random

from constants import FORMATION, NB, SAMPLE, WINDUP
from helpers import clamp


class EnemyAIMixin:
    def place_invader(self, inv):
        """Put an enemy at the top - away from the lanes the player favours."""
        model = self.model
        weights = model.spawn_weights(self.diff["spawn_avoid"])
        lanes = self.spawn_lanes
        lane_w = [weights[b] for b in lanes]
        lane_span = model.span / NB
        x = y = 0.0
        for _ in range(20):
            b = random.choices(lanes, lane_w)[0]
            x = clamp(model.x_lo + (b + random.random()) * lane_span,
                      -self.spawn_x, self.spawn_x)
            y = random.uniform(self.spawn_y_lo, self.spawn_y_hi)
            free = True
            for o in self.active:
                if o is not inv:
                    ddx, ddy = o.x - x, o.y - y
                    if ddx * ddx + ddy * ddy < 3600.0:
                        free = False
                        break
            if free:
                break
        inv.x, inv.y = x, y
        inv.mode = FORMATION
        inv.dt = inv.dv = inv.timer = 0.0
        inv.react = -1

    def compute_aim(self):
        """Where should a diving enemy aim?  (blend of prediction and habits)"""
        m, d = self.model, self.diff
        px = self.player_x
        target = px
        w = d["predict"] * m.predictability()
        if w > 0.01:
            pred = m.predict_x(px, int(0.9 / SAMPLE), self.player_speed)
            target += (pred - px) * w
        c = d["predict"] * m.camp
        if c > 0.01:
            target += (m.camp_x - target) * c
        return clamp(target, -self.player_lim, self.player_lim)

    def sample(self):
        """The enemy AI watches the player."""
        d = self.move_dir()
        move = 1 if d < 0 else 2 if d > 0 else 0
        self.model.observe(self.player_x, move, self.fired_flag)
        self.fired_flag = False
        self.aim_x = self.compute_aim()

    def try_start_dive(self):
        d = self.diff
        busy = 0
        for inv in self.active:
            if inv.mode != FORMATION:
                busy += 1
        if busy >= d["max_divers"]:
            return
        min_y = self.player_y + 260 * self.SY
        best, best_s = None, 1e18
        for inv in self.active:
            if inv.mode == FORMATION and inv.y > min_y:
                s = abs(inv.x - self.aim_x) + random.uniform(0.0, 160.0)
                if s < best_s:
                    best, best_s = inv, s
        if best is not None:
            best.mode = WINDUP
            best.timer = d["windup"]
            best.dt = 0.0
