# SkyBlaze - keyboard + mouse input, pause, quit
# (lines 580-686 of SkyBlaze_test_1.py, copied unchanged)

from constants import LEFT_SET, MOVE_LEFT, MOVE_RIGHT, RELEASE_GRACE_MS, RIGHT_SET
from difficulties import DIFFICULTIES


class InputMixin:
    def _bind_input(self):
        wn = self.wn
        for k in MOVE_LEFT + MOVE_RIGHT:
            wn.onkeypress(lambda k=k: self.key_down(k), k)
            wn.onkeyrelease(lambda k=k: self.key_up(k), k)
        wn.onkeypress(self.on_action, "space")
        wn.onkeypress(self.on_enter, "Return")
        wn.onkeypress(self.on_enter, "KP_Enter")
        for k in ("Up", "w", "W"):
            wn.onkeypress(lambda: self.move_selection(-1), k)
        for k in ("Down", "s", "S"):
            wn.onkeypress(lambda: self.move_selection(1), k)
        for i, k in enumerate(("1", "2", "3")):
            wn.onkeypress(lambda i=i: self.quick_start(i), k)
        wn.onkeypress(self.toggle_pause, "p")
        wn.onkeypress(self.toggle_pause, "P")
        wn.onkeypress(self.on_escape, "Escape")
        wn.onclick(self.on_click)
        try:                                           # lost focus -> release keys
            self.canvas.bind("<FocusOut>", lambda e: self.held.clear(), add="+")
        except Exception:
            pass
        wn.listen()

    # ------------------------------------------------------------------ input
    def key_down(self, key):
        self.release_token[key] = self.release_token.get(key, 0) + 1
        self.held.add(key)

    def key_up(self, key):
        tok = self.release_token.get(key, 0) + 1
        self.release_token[key] = tok
        if RELEASE_GRACE_MS <= 0:
            self.held.discard(key)
        else:
            self.wn.ontimer(lambda: self._finish_release(key, tok), RELEASE_GRACE_MS)

    def _finish_release(self, key, tok):
        if self.release_token.get(key) == tok:
            self.held.discard(key)

    def move_dir(self):
        held = self.held
        left = bool(held & LEFT_SET)
        right = bool(held & RIGHT_SET)
        return (1 if right else 0) - (1 if left else 0)

    def on_action(self):                 # space bar
        if self.state == "playing":
            self.fire_bullet()
        else:
            self.on_enter()

    def on_enter(self):
        if self.state == "menu":
            self.start_game(self.selected)
        elif self.state == "gameover":
            self.show_menu()

    def move_selection(self, delta):
        if self.state == "menu":
            self.selected = (self.selected + delta) % len(DIFFICULTIES)
            self.draw_menu()
            self.wn.update()

    def quick_start(self, index):
        if self.state == "menu":
            self.start_game(index)

    def on_click(self, x, y):
        if self.state != "menu":
            return
        for i, (cx, cy, w, h) in enumerate(self.buttons):
            if abs(x - cx) <= w / 2 and abs(y - cy) <= h / 2:
                self.start_game(i)
                return

    def on_escape(self):
        if self.state in ("playing", "paused"):
            self.show_menu()
        elif self.state in ("menu", "gameover"):
            self.quit()

    def toggle_pause(self):
        if self.state == "playing":
            self.state = "paused"
            self.loop_token += 1
            self.msg.clear()
            self.msg.color("white")
            self.msg.goto(0, 0)
            self.msg.write("PAUSED", False, align="center", font=("Arial", 48, "bold"))
            self.msg.goto(0, -40)
            self.msg.write("P: resume   Esc: menu", False, align="center",
                           font=("Arial", 16, "normal"))
            self.wn.update()
        elif self.state == "paused":
            self.msg.clear()
            self.state = "playing"
            self.start_loop()

    def quit(self):
        self.state = "quit"
        self.loop_token += 1
        try:
            self.wn.bye()
        except Exception:
            pass
