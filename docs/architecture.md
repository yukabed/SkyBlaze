# Architecture

## Modules and responsibilities

| Module | Responsibility |
|---|---|
| `config.py` | All constants and asset paths. No logic. |
| `game.py` | `Game`: builds the objects, owns shared state (score, enemy speed, missed enemies, game-over flag), runs `tick()` once per frame. |
| `entities/player.py` | `Player`: clamped left/right movement. |
| `entities/enemy.py` | `Enemy`: respawn, drop one row, floor check. |
| `entities/bullet.py` | `Bullet`: launch, advance, deactivate, park. |
| `systems/collision.py` | `is_collision`: the one distance test used everywhere. |
| `systems/input.py` | Binds keys to player movement and firing. |
| `ui/screen.py` | Window, background, shape registration, arena border, game-over background. |
| `ui/hud.py` | `ScoreBoard`: draws and updates the score. |
| `audio.py` | `play(path)`: picks a sound backend per platform; never raises for audio problems. |

Dependencies point one way: `game` -> `entities`, `systems`, `ui`, `audio` -> `config`.
Entities do not import `game`.

## One frame (`Game.tick`)

For each enemy: move horizontally; if it passes a wall, drop the whole formation
one row (enemies reaching the floor are counted as missed and respawned) and
reverse direction; check bullet collision (score, respawn, reset bullet); check
player collision; if the game is over, hide everything, show the end screen and
stop processing enemies. After the enemy loop the bullet advances.

## Design notes

- **Entities subclass `turtle.Turtle`.** The game already treats every object as
  a turtle (position, visibility, collision by coordinates); subclassing keeps
  that and avoids a wrapper layer.
- **Creation order is preserved** (border, score, player, enemies, bullet)
  because turtle draws in creation order.
- **Behaviour-preserving restructure.** Known bugs are documented in the README
  rather than fixed during the move, so each fix can be reviewed on its own.
- **Tests use a fake `turtle`** (`tests/fake_turtle.py`) so they run headless and
  never need tkinter or a display.
