# SkyBlaze - main menu
# (lines 688-765 of SkyBlaze_test_1.py, copied unchanged)

from difficulties import DIFFICULTIES


class MenuMixin:
    # ------------------------------------------------------------------- menu
    @staticmethod
    def _rect(t, cx, cy, w, h, fill, outline):
        t.penup()
        t.goto(cx - w / 2.0, cy - h / 2.0)
        t.setheading(0)
        t.color(outline, fill)
        t.pensize(3)
        t.pendown()
        t.begin_fill()
        for _ in range(2):
            t.fd(w)
            t.lt(90)
            t.fd(h)
            t.lt(90)
        t.end_fill()
        t.penup()

    def draw_menu(self):
        ui = self.ui
        ui.clear()
        ui.color("white")
        ui.goto(0, 170)
        ui.write("SKYBLAZE", False, align="center", font=("Arial", 54, "bold"))
        ui.color("#9fb4ff")
        ui.goto(0, 130)
        ui.color("white")
        ui.goto(0, 85)
        ui.write("Choose your difficulty", False, align="center",
                 font=("Arial", 18, "normal"))

        bw, bh, gap = 380, 64, 22
        self.buttons = []
        for i, d in enumerate(DIFFICULTIES):
            cy = 20 - i * (bh + gap)
            self.buttons.append((0, cy, bw, bh))
            if i == self.selected:
                self._rect(ui, 0, cy, bw, bh, "#23305e", d["color"])
                ui.color(d["color"])
            else:
                self._rect(ui, 0, cy, bw, bh, "#0d1126", "#5a6285")
                ui.color("#c8cce0")
            ui.goto(0, cy - 15)
            ui.write("%d   %s" % (i + 1, d["name"]), False, align="center",
                     font=("Arial", 22, "bold"))

        sel = DIFFICULTIES[self.selected]
        ui.color(sel["color"])
        for j, line in enumerate(sel["desc"]):
            ui.goto(0, -225 - j * 26)
            ui.write(line, False, align="center", font=("Arial", 14, "normal"))
        ui.color("#8a90ad")
        ui.goto(0, -self.HH + 45)
        ui.write("Up/Down + Enter or 1/2/3 or click   |   in game: Left/Right or A/D, "
                 "Space = fire, P = pause, Esc = menu   |   Esc here = quit",
                 False, align="center", font=("Arial", 12, "normal"))

    def show_menu(self):
        self.loop_token += 1                   # stop any running game loop
        self.state = "menu"
        self.held.clear()
        self.player.hideturtle()
        self.bullet.hideturtle()
        for inv in self.pool:
            inv.t.hideturtle()
        self.active = []
        self.hud.clear()
        self.msg.clear()
        self._set_end_image(False)
        self.draw_menu()
        self.wn.update()

    def _set_end_image(self, show):
        if self.end_ready:
            try:
                self.canvas.itemconfigure("end", state="normal" if show else "hidden")
            except Exception:
                pass
