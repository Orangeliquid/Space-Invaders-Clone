# Space Invaders Clone via Pygame

This is my take on the classic game of 'Space Invaders'! I utilize Pygame to create a similar experience with my own twists. The enemies move differently than the original. Instead of moving as a unit when a wall is met, the enemies that touch the wall are moved down. Additionally, the shields do not visually crumble when hit, instead they change from lime green to red. This indicates damage level. After each round the enemies, enemy projectiles, and player projectiles all gain more speed. This makes the game harder! My high score is about 9500, feel free to try and beat my score, or add your own elements to the game!

In the future, I would like to implement original game sounds and better enemy movement.

## Credit

A huge shout out to Brunotnasc for all of the in-game sprites! His github is here -> https://github.com/brunotnasc/space-invaders

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Screenshots](#screenshots)
    - [Starting Round](#starting-round)
    - [Player Death](#player-death)
    - [Shields Damaged](#shields-damaged)
    - [Game Over](#game-over)
- [License](#license)

## Installation

To run the Space-Invaders-Clone, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Orangeliquid/Space-Invaders-Clone.git
   cd Space-Invaders-Clone
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Controls: Right/Left arrow keys to move player, Spacebar to shoot

3. On game over, Backspace to exit, Enter to restart
  
4. Once the game ends the "top_score.txt" will be created to keep track of top scores!

5. Do your best to get a high score, be warned... It does get hard pretty fast

## Features

- Fast paced 'Space Invaders' look alike!
- Multiple sprites for enemy movement, enemy projectiles, and many more!
- Top score functionality for tracking best game played
- Increasing difficulty as rounds progress

## Screenshots

### Starting Round

![Space_invaders_start](https://github.com/Orangeliquid/Space-Invaders-Clone/assets/127478612/e12bd8eb-0a10-4379-8569-2cbcc8b52046)

### Player Death

![Space_invaders_player_death](https://github.com/Orangeliquid/Space-Invaders-Clone/assets/127478612/c9bacab7-d17e-4dde-8327-a743f5d960c8)

### Shields Damaged

![Space_invaders_shields_damaged](https://github.com/Orangeliquid/Space-Invaders-Clone/assets/127478612/1591f6e1-77e6-4e0d-b327-596b9556969b)

### Game Over

![Space_invaders_game_over](https://github.com/Orangeliquid/Space-Invaders-Clone/assets/127478612/0bf60bee-3653-45f1-ad7e-7bf68d24fdad)

## License

This project is licensed under the [MIT License](LICENSE.txt).
