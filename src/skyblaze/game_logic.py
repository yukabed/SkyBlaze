# SkyBlaze - per-frame game logic: step() (player move, bullet, enemies, dives, collisions).
# (lines 875 and 982-1081 of SkyBlaze_test_1.py, copied unchanged)

import random

from constants import (DIVE, DODGE_SPEED, DODGE_TIME, DODGE_TRIGGER, ENEMY_RADIUS_SQ,
                       FORMATION, PLAYER_RADIUS_SQ, SAMPLE, SPEED_CAP, WINDUP)
from helpers import clamp
from sound import play_sound


class GameLogicMixin:
    # ----------------------------------------------------------- game logic

    def step(self, dt):
        d = self.diff
        self.time += dt

        # --- player -------------------------------------------------------
        mv = self.move_dir()
        if mv:
            self.player_x = clamp(self.player_x + mv * self.player_speed * dt,
                                  -self.player_lim, self.player_lim)

        # --- the enemy AI watches the player -------------------------------
        self.sample_acc += dt
        if self.sample_acc >= SAMPLE:
            self.sample_acc -= SAMPLE
            self.sample()

        # --- bullet ---------------------------------------------------------
        if self.bullet_state == "fire":
            y0 = self.by
            self.by = y0 + self.bullet_speed * dt
            y1 = self.by
            bx = self.bx
            for inv in self.active:
                ddx = inv.x - bx
                if ddx * ddx >= ENEMY_RADIUS_SQ:
                    continue
                cy = inv.y if y0 <= inv.y <= y1 else (y0 if inv.y < y0 else y1)
                ddy = inv.y - cy
                if ddx * ddx + ddy * ddy < ENEMY_RADIUS_SQ:      # swept collision
                    play_sound("explosion-e+b.wav")              # sound for windows/linux/mac
                    self.reset_bullet()
                    self.model.record_kill(bx)
                    self.place_invader(inv)
                    self.speed_mult = min(SPEED_CAP, self.speed_mult + d["speed_gain"])
                    self.score += 10
                    break
            if self.bullet_state == "fire" and self.by > self.top_y:
                self.reset_bullet()

        # --- enemies ----------------------------------------------------------
        fire = self.bullet_state == "fire"
        base = self.base_speed * self.speed_mult * self.dir
        edge_hit = False
        for inv in self.active:
            mode = inv.mode
            if mode == FORMATION:
                if fire and inv.react != self.shot_id:
                    gap = inv.y - self.by
                    if 0.0 < gap < self.react_dist:
                        t_hit = gap / self.bullet_speed
                        px = inv.x + base * t_hit           # where it will be then
                        if abs(px - self.bx) < DODGE_TRIGGER:
                            inv.react = self.shot_id        # decide once per bullet
                            if random.random() < self.dodge_p:
                                side = 1.0 if px >= self.bx else -1.0
                                if abs(inv.x + side * 80.0) > self.edge_x - 10.0:
                                    side = -side
                                inv.dv = side * DODGE_SPEED
                                inv.dt = DODGE_TIME
                if inv.dt > 0.0:
                    vx = inv.dv
                    inv.dt -= dt
                else:
                    vx = base
                x = inv.x + vx * dt
                inv.x = x = clamp(x, -self.hard_x, self.hard_x)
                if (x > self.edge_x) if self.dir > 0 else (x < -self.edge_x):
                    edge_hit = True
            elif mode == WINDUP:                            # wiggle, then dive
                inv.timer -= dt
                if inv.timer <= 0.0:
                    inv.mode = DIVE
            else:                                           # DIVE
                inv.y -= self.dive_speed * dt
                if inv.y - self.player_y > self.commit:     # still homing in
                    gap_x = self.aim_x - inv.x
                    mx = self.homing * dt
                    inv.x += mx if gap_x > mx else -mx if gap_x < -mx else gap_x
                if inv.y < self.lose_y:                     # flew past the player
                    self.place_invader(inv)

        if edge_hit:
            self.step_down()
            if self.state != "playing":
                return

        # --- dive attacks ---------------------------------------------------
        self.dive_timer -= dt
        if self.dive_timer <= 0.0:
            lo, hi = d["dive_gap"]
            self.dive_timer = random.uniform(lo, hi) * (1.0 - 0.35 * self.model.read)
            self.try_start_dive()

        # --- check for a collision between the player and an enemy -----------
        px, py = self.player_x, self.player_y
        for inv in self.active:
            ddx, ddy = inv.x - px, inv.y - py
            if ddx * ddx + ddy * ddy < PLAYER_RADIUS_SQ:
                self.end_game()
                return
