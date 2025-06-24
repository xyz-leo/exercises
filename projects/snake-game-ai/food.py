# food.py

import pygame
import random
from settings import BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_FOOD

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        # Generate a random (x, y) position aligned to the grid
        x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        return [x, y]

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_FOOD, pygame.Rect(self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

    def respawn(self):
        self.position = self.random_position()

