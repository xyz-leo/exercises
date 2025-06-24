# game.py

import pygame
from snake import Snake
from food import Food
from settings import COLOR_BACKGROUND, GAME_SPEED
from ai_controller import SnakeAI
import time


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.running = True
        self.ai = SnakeAI(self.snake, self.food)

    def reset(self):
        time.sleep(0.5)
        self.snake = Snake()
        self.food = Food()
        self.ai = SnakeAI(self.snake, self.food)
        self.ai.activate()

    
    def handle_events(self):
        # Optional: still allow quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # AI takes control
        new_direction = self.ai.get_next_direction()
        self.snake.change_direction(new_direction)


    #def handle_events(self): # Player mode
        # Handle keyboard input
    #    for event in pygame.event.get():
    #        if event.type == pygame.QUIT:
    #            self.running = False
    #        elif event.type == pygame.KEYDOWN:
    #            if event.key == pygame.K_UP:
    #                self.snake.change_direction("UP")
    #            elif event.key == pygame.K_DOWN:
    #                self.snake.change_direction("DOWN")
    #            elif event.key == pygame.K_LEFT:
    #                self.snake.change_direction("LEFT")
    #            elif event.key == pygame.K_RIGHT:
    #                self.snake.change_direction("RIGHT")

    def update(self):
        self.snake.move()

        # Check if snake eats the food
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.respawn()

        # Check for collisions
        if self.snake.check_self_collision() or self.snake.check_wall_collision():
            self.ai.deactivate()
            self.reset()

    def draw(self):
        self.screen.fill(COLOR_BACKGROUND)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        pygame.display.flip()

    def run(self):
        # Main game loop
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(GAME_SPEED)

