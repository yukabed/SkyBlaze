#SkyBlaze by Mohammadreza & Yukabed
# ---------------------------------------------------------------------------
# Upgraded version
#   1. Main menu with 3 difficulty levels (Easy / Medium / Hard)
#   2. Adaptive enemies: they learn the player's habits (where he stands, which
#      lanes he shoots from, how he moves) and counter them, so the same trick
#      cannot be exploited again and again
#   3. Full-screen play field that adapts itself to any screen resolution
#
# Optional library: Pillow  (pip install pillow)
#   -> lets the background / game-over pictures be scaled smoothly to the
#      screen.  The game runs without it too (the background is tiled instead).
#
# Controls
#   Menu    : Up/Down (or W/S) + Enter/Space, 1/2/3, or click a button, Esc quits
#   In game : Left/Right (or A/D) move, Space fire, P pause, Esc back to menu
# ---------------------------------------------------------------------------

import tkinter as tk
import turtle

from game import Game


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    try:
        main()
    except (turtle.Terminator, tk.TclError):
        pass                                   # window was closed
