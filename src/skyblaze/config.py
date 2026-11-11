'''python
"""Centralized configuration for SkyBlaze.

All tunable game settings and asset paths are defined here.
Keeping configuration separate from game logic makes it easier
to adjust the layout and gameplay without changing behaviour.
"""

from pathlib import Path


# --- Asset paths ------------------------------------------------------------

# Resolve paths relative to this file so the game works regardless
# of the current working directory.
PACKAGE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = PACKAGE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"

BACKGROUND_IMAGE = IMAGES_DIR / "background.gif"
END_IMAGE = IMAGES_DIR / "end.gif"
PLAYER_IMAGE = IMAGES_DIR / "player1.gif"
INVADER_IMAGE = IMAGES_DIR / "invader3.gif"

LASER_SOUND = SOUNDS_DIR / "laser.wav"
ENEMY_EXPLOSION_SOUND = SOUNDS_DIR / "explosion-e+b.wav"

REQUIRED_ASSETS = (
    BACKGROUND_IMAGE,
    END_IMAGE,
    PLAYER_IMAGE,
    INVADER_IMAGE,
    LASER_SOUND,
    ENEMY_EXPLOSION_SOUND,
)

# Turtle identifies registered image shapes by their string paths.
# Registration and subsequent shape() calls must use the same values.
PLAYER_SHAPE = str(PLAYER_IMAGE)
INVADER_SHAPE = str(INVADER_IMAGE)


# --- Window and HUD ---------------------------------------------------------

WINDOW_TITLE = "SkyBlaze"
BACKGROUND_COLOR = "blue"

BORDER_COLOR = "white"
BORDER_ORIGIN = (-300, -300)
BORDER_SIZE = 600
BORDER_PEN_SIZE = 3

SCORE_COLOR = "white"
SCORE_POSITION = (-290, 280)
SCORE_FONT = ("Arial", 14, "normal")
POINTS_PER_KILL = 10


# --- Player -----------------------------------------------------------------

UP_HEADING = 90
PLAYER_START_POSITION = (0, -250)
PLAYER_SPEED = 15
PLAYER_X_LIMIT = 280
PLAYER_HIT_DISTANCE = 30


# --- Enemies ----------------------------------------------------------------

ENEMY_COUNT = 10
ENEMY_SPAWN_X_RANGE = (-200, 200)
ENEMY_SPAWN_Y_RANGE = (100, 250)
ENEMY_START_SPEED = 5
ENEMY_SPEED_STEP = 0.5
ENEMY_WALL_X = 270
ENEMY_DROP_STEP = 40
ENEMY_FLOOR_Y = -285
MAX_MISSED_ENEMIES = 5


# --- Bullet -----------------------------------------------------------------

BULLET_COLOR = "yellow"
BULLET_SHAPE = "triangle"
BULLET_SIZE = (0.5, 0.5)
BULLET_SPEED = 30
BULLET_MUZZLE_OFFSET_Y = 10
BULLET_TOP_Y = 275
BULLET_PARKING_POSITION = (0, -400)
BULLET_HIT_DISTANCE = 25
'''