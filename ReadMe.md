# Space Shooter Game

Welcome to the Space Shooter Game! This is a fun and action-packed arcade-style shooter built with Python and Pygame.

## Features

- **Multiple Player Modes**: Play as different characters with unique abilities.
- **Various Enemies**: Face a variety of enemies, including powerful bosses.
- **Power-ups and Allies**: Collect power-ups and call for ally support.
- **Sound Effects**: Enjoy immersive sound effects and background music.

## Getting Started

### Prerequisites

- Python 3.x
- Pygame

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/enhanced-shooting-game.git
   ```
2. Navigate to the project directory:
   ```sh
   cd enhanced-shooting-game
   ```
3. Install Pygame:
   ```sh
   pip install pygame
   ```

### Running the Game

To start the game, run the `main.py` file:

```sh
python main.py
```

## Controls

- **Arrow Keys**: Move the player.
- **Spacebar**: Shoot bullets.
- **Enter**: Start/Restart the game.

## Game Mechanics

- **Player Modes**:

  - **Normal Mode**: Standard shooting with one bullet.
  - **Mode 2**: Shotgun-style spread shooting (activated when health is ≥ 10).
  - **Mode 3**: Full-circle spread shooting with auto-fire (activated when health is ≥ 20).

- **Enemies**:

  - **Standard Enemies**: Basic foes that move downwards.
  - **Extra Enemies**: Appear after score reaches 20; have higher health and shooting capability.
  - **Boss**: Appears when score reaches 100; tough to beat and shoots in multiple directions.

- **Power-ups**:

  - **Health Packs**: Restore player health.

- **Allies**:
  - **Ally Support**: Appears when score reaches 40 and no boss is present; helps in combat.

## Assets

- **Images**: Place all the image assets in the `images/` directory.
- **Sounds**: Place all the sound assets in the `audio/` directory.

## Development

Feel free to contribute to the project. Here are some areas you might want to explore:

- Adding new enemy types.
- Implementing new power-ups.
- Enhancing the graphics and sound effects.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Enjoy the game!
