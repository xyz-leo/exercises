# Snake Game with AI (Pygame)

This project is a classic Snake game implemented using Pygame, designed with object-oriented programming and modular architecture. It includes two gameplay modes:

- Manual mode: controlled by the player.
- AI mode: a simple programmed AI controls the snake.

## Features

- Object-oriented design
- Modular code structure
- Manual and automatic game modes
- AI that follows food and avoids reversing direction
- Game reset and switching modes without restarting the app

## AI Overview

The AI in this version is rule-based. It is not trained using machine learning or reinforcement learning. It follows a simple logic to move toward the food and avoid reversing direction.

A future version will include a reinforcement learning agent using Q-Learning or Deep Q-Learning.

## Controls

| Key        | Action                        |
|------------|-------------------------------|
| Arrow Keys | Move the snake manually       |
| SPACE      | Toggle between AI and Manual  |
| ESC        | Quit the game                 |

## Project Structure
.
├── main.py # Entry point
├── game.py # Main game logic and loop
├── snake.py # Snake class
├── food.py # Food class
├── ai.py # Basic rule-based AI
├── settings.py # Game settings and constants
├── misc/ # Temporary or dev-related files (ignored by Git)
├── venv/ # Virtual environment (ignored)
└── pycache/ # Python bytecode (ignored)


## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/snake-ai-pygame.git
   cd snake-ai-pygame

2. (Optional) Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Run the game:
    ```bash
    python3 main.py


Future Work

    Add timing and score tracking

    Improve AI to avoid collisions with itself

    Implement reinforcement learning (Q-Learning or Deep Q-Network)
