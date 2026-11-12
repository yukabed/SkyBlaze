# SkyBlaze - window, layout, backdrop, pens and sprite setup.
# (lines 34-37 and 364-578 of SkyBlaze_test_1.py, copied unchanged)

import base64
import io
import os
import random
import time
import tkinter as tk
import turtle

try:                                    # optional: smooth image scaling
    from PIL import Image
except ImportError:
    Image = None

from difficulties import MAX_ENEMIES
from constants import NB
from dumb_enemy import Invader
from helpers import asset


class DisplayMixin:
    # ------------------------------------------------------------------ setup
    def _setup_screen(self):
        wn = turtle.Screen()
        self.wn = wn
        wn.title("SkyBlaze")
        wn.bgcolor("black")
        try:
            wn.setup(width=1.0, height=1.0)
        except Exception:
            pass
        cv = wn.getcanvas()
        self.canvas = getattr(cv, "_canvas", cv)     # the real tkinter Canvas
        self.root = cv.winfo_toplevel()
        self._go_fullscreen()
        self.W, self.H = self._measure_canvas()
        try:
            wn.screensize(self.W, self.H)            # no scrollbars, origin centred
        except Exception:
            pass
        wn.tracer(0, 0)                              # we redraw once per frame

    def _go_fullscreen(self):
        root = self.root
        try:
            root.attributes("-fullscreen", True)
        except tk.TclError:
            try:
                root.state("zoomed")
            except tk.TclError:
                pass
        try:
            root.update()
        except tk.TclError:
            pass

    def _measure_canvas(self):
        """Wait until the window manager has finished going full-screen."""
        cv, root = self.canvas, self.root
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        last = None
        size = (sw, sh)
        for _ in range(60):
            root.update()
            size = (cv.winfo_width(), cv.winfo_height())
            if (size == last and size[0] >= 0.9 * sw and size[1] >= 0.8 * sh):
                break
            last = size
            time.sleep(0.02)
        w, h = size
        if w < 300 or h < 300:
            w, h = sw, sh
        return int(w), int(h)

    def _build_layout(self):
        W, H = self.W, self.H
        self.HW, self.HH = W / 2.0, H / 2.0
        self.SX = min(max(W / 1000.0, 1.0), 2.0)       # horizontal speed scale
        self.SY = min(max(H / 700.0, 0.8), 1.8)        # vertical speed scale
        self.player_y = -self.HH + 60
        self.player_lim = self.HW - 40                 # player x limit
        self.edge_x = self.HW - 45                     # enemies turn around here
        self.hard_x = self.HW - 25                     # absolute enemy x limit
        self.lose_y = -self.HH + 15                    # an enemy reaching this is missed
        self.top_y = self.HH - 25                      # bullet leaves the field
        # Enemies appear in the central part of the screen only, so the formation
        # always has room to sweep left/right before it has to turn and descend.
        self.spawn_x = self.HW * 0.5
        self.spawn_y_hi = self.HH - 100
        self.spawn_y_lo = self.spawn_y_hi - 150 * self.SY
        self.player_speed = 360.0 * self.SX
        self.bullet_speed = 650.0 * self.SY
        self.react_dist = 0.28 * self.bullet_speed     # enemies react to bullets this close
        self.model.configure(-self.player_lim, self.player_lim)
        # lanes (of the AI's memory) that lie inside the spawn area
        self.spawn_lanes = [b for b in range(NB)
                            if abs(self.model.x_of_bin(b)) <= self.spawn_x]

    def _load_image(self, name, mode):
        """Return a tk.PhotoImage fitted to the screen, or None.

        mode 'cover'   : fill the whole screen (background)
        mode 'contain' : fit inside the screen keeping the aspect ratio
        """
        path = asset(name)
        if not os.path.exists(path):
            return None
        W, H = self.W, self.H
        try:
            if Image is not None:
                with Image.open(path) as im:
                    im = im.convert("RGB")
                    iw, ih = im.size
                    scale = (max(W / iw, H / ih) if mode == "cover"
                             else min(W / iw, H / ih))
                    nw, nh = max(1, round(iw * scale)), max(1, round(ih * scale))
                    resample = getattr(Image, "Resampling", Image).LANCZOS
                    im = im.resize((nw, nh), resample)
                    if mode == "cover" and (nw > W or nh > H):
                        left, top = (nw - W) // 2, (nh - H) // 2
                        im = im.crop((left, top, left + W, top + H))
                    buf = io.BytesIO()
                    im.save(buf, "PNG")
                data = base64.b64encode(buf.getvalue()).decode("ascii")
                return tk.PhotoImage(master=self.canvas, data=data)
            src = tk.PhotoImage(master=self.canvas, file=path)
            if mode == "cover":                       # tile it over the screen
                big = tk.PhotoImage(master=self.canvas, width=W, height=H)
                big.tk.call(big.name, "copy", src.name, "-to", 0, 0, W, H)
                return big
            return src
        except Exception:
            return None

    def _build_backdrop(self):
        cv = self.canvas
        self._images = []                              # keep references alive
        bg = self._load_image("background.gif", "cover")
        if bg is not None:
            self._images.append(bg)
            cv.create_image(0, 0, image=bg, tags="backdrop")
        else:                                          # simple star field
            for _ in range(160):
                x = random.randint(-int(self.HW), int(self.HW))
                y = random.randint(-int(self.HH), int(self.HH))
                s = random.choice((1, 1, 2, 3))
                cv.create_rectangle(x, y, x + s, y + s, outline="",
                                    fill=random.choice(("white", "#9fb4ff", "#ffe9a8")),
                                    tags="backdrop")
        end = self._load_image("end.gif", "contain")
        if end is not None:
            self._images.append(end)
            cv.create_image(0, 0, image=end, tags="end", state="hidden")
            self.end_ready = True
            cv.tag_lower("end")
        cv.tag_lower("backdrop")

    @staticmethod
    def _make_pen():
        t = turtle.Turtle(visible=False)
        t.setundobuffer(None)
        t.speed(0)
        t.penup()
        t.hideturtle()
        return t

    def _build_pens(self):
        # Border (a thin frame around the whole screen)
        border = self._make_pen()
        border.color("white")
        border.pensize(3)
        m = 12
        border.goto(-self.HW + m, -self.HH + m)
        border.setheading(0)
        border.pendown()
        for _ in range(2):
            border.fd(self.W - 2 * m)
            border.lt(90)
            border.fd(self.H - 2 * m)
            border.lt(90)
        border.penup()
        self.hud = self._make_pen()      # score / misses / AI info
        self.ui = self._make_pen()       # main menu
        self.msg = self._make_pen()      # pause / game-over text

    def _register(self, name):
        path = asset(name)
        if not os.path.exists(path):
            return None
        try:
            self.wn.register_shape(path)
            return path
        except Exception:
            return None

    def _build_sprites(self):
        player_shape = self._register("player1.gif")
        enemy_shape = self._register("invader3.gif")

        # Create the player turtle
        self.player = turtle.Turtle(visible=False)
        self.player.setundobuffer(None)
        if player_shape:
            self.player.shape(player_shape)
        else:
            self.player.shape("triangle")
            self.player.color("cyan")
        self.player.penup()
        self.player.speed(0)
        self.player.setposition(0, self.player_y)
        self.player.setheading(90)

        # Create the player's bullet
        self.bullet = turtle.Turtle(visible=False)
        self.bullet.setundobuffer(None)
        self.bullet.color("yellow")
        self.bullet.shape("triangle")
        self.bullet.penup()
        self.bullet.speed(0)
        self.bullet.setheading(90)
        self.bullet.shapesize(0.5, 0.5)
        self.bullet.hideturtle()

        # Create a pool of enemies (only as many as the difficulty needs are used)
        self.pool = []
        for _ in range(MAX_ENEMIES):
            t = turtle.Turtle(visible=False)
            t.setundobuffer(None)
            if enemy_shape:
                t.shape(enemy_shape)
            else:
                t.shape("circle")
                t.color("red")
            t.penup()
            t.speed(0)
            self.pool.append(Invader(t))
