# SkyBlaze

**SkyBlaze** is a Python-based space shooter game project focused on combining traditional arcade gameplay with adaptive artificial intelligence.

The main idea behind SkyBlaze is to develop an enemy AI system that observes player behavior, learns recurring patterns, and gradually adapts its strategies to create a more dynamic and challenging gameplay experience.

Unlike conventional enemies that follow fixed behaviors, SkyBlaze aims to make enemies respond to how each player actually plays.

## Project Vision

The long-term goal of SkyBlaze is to build an adaptive enemy AI system that can:

- Observe and analyze player behavior during gameplay.
- Identify recurring movement and combat patterns.
- Learn player habits through online learning techniques.
- Adapt enemy strategies based on detected behaviors.
- Increase difficulty progressively while maintaining fair gameplay.
- Remember player behavior across multiple stages and game sessions.

## Core AI Features

### 1. Player Behavior Analysis

The game collects gameplay telemetry at fixed time intervals and converts player actions into discrete symbols.

The AI analyzes several behavioral patterns:

- **Movement Patterns:** Staying in one position, moving toward screen edges, and alternating between left and right.
- **Shooting Patterns:** Regular firing intervals, continuous shooting, preferred shooting positions, and target preferences.
- **Dodging Patterns:** Directional preferences and consistent reaction delays.
- **Action Sequences:** Repeated combinations of movements and shooting actions.

### 2. Adaptive Learning System

SkyBlaze uses lightweight online learning techniques to build a behavioral profile for each player.

The planned learning components include:

- **N-gram Models:** Identifying recurring sequences of 2–4 player actions and estimating the probability of future actions.
- **Entropy Analysis:** Measuring how predictable or repetitive player behavior is.
- **Behavior Histograms:** Tracking movement zones, shooting positions, firing intervals, and dodging directions.
- **Time-based Decay:** Gradually reducing the influence of older behavioral patterns when the player changes their strategy.
- **Persistent Player Profiles:** Saving learned behavioral information locally in JSON files, allowing enemies in later stages to use previously collected information.

### 3. Adaptive Enemy AI

Based on detected player habits, enemies can select different counter-strategies.

Examples include:

| Detected Player Habit | Possible Enemy Response |
|---|---|
| Staying in one column | Targeting that position |
| Staying near screen edges | Covering the edges with projectiles |
| Repeated left-right movement | Predictive shooting |
| Regular shooting intervals | Timing defensive actions |
| Consistent dodging direction | Adjusting projectile direction |
| Repeatedly targeting one enemy | Prioritizing that enemy with defensive actions |

To prevent enemies from becoming predictable themselves, the system is designed to use a **Multi-Armed Bandit** approach, such as Thompson Sampling.

This allows the AI to evaluate different counter-strategies and learn which ones work best against a particular player.

### 4. Progressive Adaptation and Fairness

The adaptation system is designed to become more aggressive when the same player habit is detected repeatedly.

However, enemy adaptation will have defined limits:

- Counter-strategies must have possible ways to avoid or overcome them.
- Adaptation strength will depend on the current stage and difficulty level.
- Enemy firing intervals and dodge cooldowns will follow predefined gameplay constraints.
- The AI will adjust the timing and direction of actions rather than bypassing gameplay limitations.

## Game Progression

The planned game structure includes three difficulty levels:

- Easy
- Normal
- Hard

Gameplay is organized into stages (waves). Each stage ends after the player defeats 15 enemies.

The next stage introduces increased difficulty and may unlock additional enemy counter-strategies.

Player behavioral profiles will persist between stages and game sessions.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Turtle | Initial game development and visualization |
| JSON | Local player profile storage |
| Git & GitHub | Version control and collaboration |

### AI and Learning Components

The initial implementation will primarily use Python's standard library:

- `collections`
- `math`
- `random`
- `json`

The learning system will be developed behind modular interfaces to keep it testable and extensible.

The [River](https://github.com/online-ml/river) library may be considered in future development if more advanced online learning or drift detection capabilities are needed.

## Testing and Evaluation

A major development goal is to make the adaptive AI system testable independently of the graphical game.

The planned testing environment includes scripted player behaviors:

- **Camper:** A player who repeatedly stays in one position.
- **Oscillator:** A player who frequently moves left and right.
- **Shooter:** A player who continuously fires.
- **Random Player:** A player with unpredictable movement and actions.

A simulated game environment and mock Turtle components will be used where possible to evaluate learning behavior without requiring a complete graphical game session.

The main evaluation goals are:

- Measuring how accurately the system identifies recurring habits.
- Evaluating predictive shooting against repetitive movement.
- Testing adaptive defensive timing.
- Verifying that varied player behavior is less exploitable.
- Ensuring that adaptation remains within defined fairness constraints.

## Planned Project Structure

The project is designed around modular components to separate gameplay mechanics, enemy behavior, telemetry, and learning logic.

Planned modules include:

- `stages.py` — Stage and wave progression.
- `difficulty.py` — Difficulty configuration.
- `entities/enemy_bullet.py` — Enemy projectile behavior.
- `adaptation/telemetry.py` — Player behavior data collection.
- `adaptation/habits.py` — Habit detection and pattern analysis.
- `adaptation/counters.py` — Behavioral statistics and counters.
- `adaptation/policy.py` — Adaptive enemy decision-making.
- `adaptation/profile.py` — Player profile management and JSON persistence.

## Development Roadmap

The project will be developed incrementally:

1. **Gameplay Foundations:** Fixed-timestep game loop, keyboard input handling, and core gameplay corrections.
2. **Stages and Difficulty:** Implementing stage progression and Easy, Normal, and Hard difficulty levels.
3. **Enemy Projectiles and Dodging:** Time-based enemy shooting and defensive actions with cooldowns.
4. **Telemetry and Learning:** Collecting player behavior, detecting habits, and saving player profiles.
5. **Adaptive Enemy Strategies:** Implementing counter-strategies, bandit-based selection, and progressive adaptation.
6. **Testing and Debugging:** Evaluating the system using scripted players and developing a debug view for detected habits.

## Project Status

**Active Development**

SkyBlaze is being developed incrementally, with gameplay foundations and the adaptive AI architecture forming the primary development priorities.

Features described in this README represent the project's design goals and planned implementation unless explicitly identified as completed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.