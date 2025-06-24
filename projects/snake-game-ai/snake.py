# snake.py

import pygame
from settings import BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_SNAKE

class Snake:
    def __init__(self):
        # Snake starts at the center of the screen with 3 segments
        self.body = [
            [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2],
            [SCREEN_WIDTH // 2 - BLOCK_SIZE, SCREEN_HEIGHT // 2],
            [SCREEN_WIDTH // 2 - 2 * BLOCK_SIZE, SCREEN_HEIGHT // 2]
        ]
        self.direction = "RIGHT"
        self.grow_flag = False

    def move(self):
        # Copy the current head
        head_x, head_y = self.body[0]

        # Move the head in the current direction
        if self.direction == "UP":
            head_y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            head_y += BLOCK_SIZE
        elif self.direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            head_x += BLOCK_SIZE

        # Insert the new head position at the beginning of the body list
        new_head = [head_x, head_y]
        self.body.insert(0, new_head)

        # If the snake ate food, don't remove the tail (it grows)
        if not self.grow_flag:
            self.body.pop()  # Remove last segment (tail)
        else:
            self.grow_flag = False  # Reset the flag

    def change_direction(self, new_direction):
        # Prevent the snake from reversing into itself
        opposite_directions = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def grow(self):
        # Set the flag to grow on the next move
        self.grow_flag = True

    def draw(self, screen):
        # Draw each segment of the snake on the screen
        for segment in self.body:
            pygame.draw.rect(screen, COLOR_SNAKE, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

    def check_self_collision(self):
        # If the head collides with any other part of the body
        return self.body[0] in self.body[1:]

    def check_wall_collision(self):
        head_x, head_y = self.body[0]
        return (
            head_x < 0 or head_x >= SCREEN_WIDTH or
            head_y < 0 or head_y >= SCREEN_HEIGHT
        )

