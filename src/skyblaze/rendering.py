# SkyBlaze - drawing (HUD + render)
# (lines 1083-1118 of SkyBlaze_test_1.py, copied unchanged)

from constants import WINDUP


class RenderingMixin:
    # -------------------------------------------------------------- drawing
    def draw_hud(self):
        d = self.diff
        pct = int(self.model.read * 100.0 + 0.5)
        key = (self.score, self.missed, pct)
        if key == self._hud_key:
            return
        self._hud_key = key
        hud = self.hud
        hud.clear()
        y = self.HH - 52
        hud.color("white")
        hud.goto(-self.HW + 30, y)
        hud.write("Score: %s" % self.score, False, align="left",
                  font=("Arial", 18, "normal"))
        hud.goto(self.HW - 30, y)
        hud.write("Missed: %d / %d" % (self.missed, d["max_missed"]), False,
                  align="right", font=("Arial", 18, "normal"))
        hud.color(d["color"])
        hud.goto(0, y)
        hud.write("%s   |   Enemy adaptation: %d%%" % (d["name"], pct), False,
                  align="center", font=("Arial", 14, "normal"))

    def render(self):
        px = self.player_x
        if px != self._drawn_px:
            self.player.setx(px)
            self._drawn_px = px
        if self.bullet_state == "fire":
            self.bullet.setposition(self.bx, self.by)
        wob = 6.0 if (int(self.time * 24.0) & 1) else -6.0
        for inv in self.active:
            x = inv.x + wob if inv.mode == WINDUP else inv.x
            inv.t.setposition(x, inv.y)
        self.draw_hud()
        self.wn.update()
