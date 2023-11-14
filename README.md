# Snake Game e-Sport Version

## Introduction

Welcome to the Snake Game e-Sport Version by Volyo! This Python game utilizes the Pygame library to create a competitive and entertaining snake game with some extra features. Challenge yourself, achieve high scores, and even share your accomplishments on Discord!

## Features

- Classic Snake gameplay with a competitive twist.
- Automatic logging of game events.
- Display of FPS (Frames Per Second) and reaction time.
- Discord integration to share your scores.
- Pause and resume functionality.
- Log viewer to check detailed game logs.

## Requirements

- Python 3.x
- Pygame library
- Requests library
- Discord Webhook URL (to enable Discord integration)

## Installation

1. Install Python 3.x: [Download Python](https://www.python.org/downloads/)

2. Install Pygame library:

   ```bash
   pip install pygame
   ```

3. Install Requests library:

   ```bash
   pip install requests
   ```

4. Obtain a Discord Webhook URL:
   - Create a webhook on your Discord server.
   - Replace the `DISCORD_WEBHOOK_URL` variable at the line 10 in the snake.py with the URL you obtained.

## Usage

Run the script in a terminal or command prompt:

```bash
python snake_game.py
```

- Use arrow keys to control the snake's direction.
- Press 'L' to view detailed game logs.
- Press the spacebar to pause and resume the game.

## Discord Integration

The game will automatically send your score to Discord after each game. To view scores and compete with others, check the Discord channel associated with the webhook.

## Logs

Detailed game logs are stored in the `snake_game.log` file. You can reset the logs by running the game with the log reset function.

## Credits

- Snake Game by Volyo
- Pygame Library: [pygame.org](https://www.pygame.org/)
- Discord Integration using the Requests Library: [docs.python-requests.org](https://docs.python-requests.org/)

Feel free to share your feedback and enjoy playing the Snake Game e-Sport Version! 🐍🎮
