# SkyBlaze - the Game class: it only wires together the parts that live in the other files.
# (lines 335-337, 339-362 and 1120-1121 of SkyBlaze_test_1.py, copied unchanged)

from difficulties import DIFFICULTIES
from display import DisplayMixin
from dumb_enemy import DumbEnemyMixin
from enemy_ai import EnemyAIMixin
from enemy_brain import PlayerModel
from game_flow import GameFlowMixin
from game_logic import GameLogicMixin
from input_handler import InputMixin
from menu import MenuMixin
from player import PlayerMixin
from rendering import RenderingMixin


# ---------------------------------------------------------------------------
# The game
# ---------------------------------------------------------------------------
class Game(DisplayMixin, InputMixin, MenuMixin, GameFlowMixin, GameLogicMixin,
           PlayerMixin, DumbEnemyMixin, EnemyAIMixin, RenderingMixin):
    def __init__(self):
        self.model = PlayerModel()
        self.state = "menu"            # menu / playing / paused / gameover / quit
        self.selected = 1              # highlighted difficulty (Medium)
        self.diff = DIFFICULTIES[1]
        self.held = set()
        self.release_token = {}
        self.loop_token = 0
        self.active = []
        self.buttons = []
        self.score = 0
        self.missed = 0
        self.time = 0.0
        self._hud_key = None
        self._drawn_px = None
        self.end_ready = False

        self._setup_screen()
        self._build_layout()
        self._build_backdrop()
        self._build_pens()
        self._build_sprites()
        self._bind_input()
        self.show_menu()

    def run(self):
        self.wn.mainloop()
