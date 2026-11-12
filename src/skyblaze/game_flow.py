# SkyBlaze - game flow (start / loop / tick / game over)
# (lines 767-873 of SkyBlaze_test_1.py, copied unchanged)

import random
import time

from constants import FORMATION, MEMORY_KEEP, STEP
from difficulties import DIFFICULTIES


class GameFlowMixin:
    # ------------------------------------------------------------- game flow
    def start_game(self, index):
        if self.state != "menu":
            return
        self.selected = index
        self.diff = d = DIFFICULTIES[index]
        self.ui.clear()
        self.msg.clear()
        self._set_end_image(False)

        self.score = 0
        self.missed = 0
        self.speed_mult = 1.0
        self.dir = 1
        self.base_speed = d["speed"] * self.SX
        self.dive_speed = d["dive_speed"] * self.SY
        self.homing = d["homing"] * self.SX
        self.commit = d["commit"] * self.SY
        self.step_px = d["step_down"] * self.SY
        self.time = 0.0
        self.sample_acc = 0.0
        self.player_x = 0.0
        self._drawn_px = None
        self.bullet_state = "ready"
        self.bx = self.by = 0.0
        self.shot_id = 0
        self.dodge_p = 0.0
        self.fired_flag = False
        self.aim_x = 0.0
        self.dive_timer = random.uniform(*d["dive_gap"])
        self.held.clear()

        self.model.begin_round(d["memory"], MEMORY_KEEP)

        self.active = []
        for i, inv in enumerate(self.pool):
            if i < d["enemies"]:
                inv.mode = FORMATION
                inv.dt = inv.dv = inv.timer = 0.0
                inv.react = -1
                self.active.append(inv)
                self.place_invader(inv)
                inv.t.showturtle()
            else:
                inv.t.hideturtle()
        self.player.setposition(0, self.player_y)
        self.player.showturtle()
        self.bullet.hideturtle()

        self._hud_key = None
        self.state = "playing"
        self.render()
        self.start_loop()

    def start_loop(self):
        self.loop_token += 1
        token = self.loop_token
        self.last_time = time.perf_counter()
        self.acc = 0.0
        self.wn.ontimer(lambda: self.tick(token), 6)

    def tick(self, token):
        if token != self.loop_token or self.state != "playing":
            return
        now = time.perf_counter()
        self.acc += min(now - self.last_time, 0.1)
        self.last_time = now
        steps = 0
        while self.acc >= STEP and steps < 6:
            self.acc -= STEP
            self.step(STEP)
            steps += 1
            if self.state != "playing":
                return
        if self.acc > STEP:
            self.acc = 0.0                     # we fell behind: don't spiral
        if steps:
            self.render()
        if token == self.loop_token and self.state == "playing":
            self.wn.ontimer(lambda: self.tick(token), 6)

    def end_game(self):
        if self.state != "playing":
            return
        self.state = "gameover"
        self.loop_token += 1
        self.player.hideturtle()
        self.bullet.hideturtle()
        for inv in self.pool:
            inv.t.hideturtle()
        self.hud.clear()
        self._set_end_image(True)
        m = self.msg
        m.clear()
        m.color("white")
        if not self.end_ready:
            m.goto(0, 40)
            m.write("GAME OVER", False, align="center", font=("Arial", 64, "bold"))
        m.color(self.diff["color"])
        m.goto(0, -self.HH + 120)
        m.write("%s  -  Final score: %d" % (self.diff["name"], self.score), False,
                align="center", font=("Arial", 24, "bold"))
        m.color("white")
        m.goto(0, -self.HH + 80)
        m.write("Enter: main menu     Esc: quit", False, align="center",
                font=("Arial", 16, "normal"))
        self.wn.update()
