# ai_controller.py

class SnakeAI:
    def __init__(self, snake, food):
        self.snake = snake
        self.food = food
        self.is_active = True  # Active by default

    def get_next_direction(self):
        if not self.is_active:
            return None  # If AI its not active, don't do nothing 

        head_x, head_y = self.snake.body[0]
        food_x, food_y = self.food.position
        current_direction = self.snake.direction

        # Prefer vertical if needed
        if food_y < head_y and current_direction != "DOWN":
            return "UP"
        elif food_y > head_y and current_direction != "UP":
            return "DOWN"
        elif food_x < head_x and current_direction != "RIGHT":
            return "LEFT"
        elif food_x > head_x and current_direction != "LEFT":
            return "RIGHT"

        return current_direction  # fallback if blocked

    def deactivate(self):
        self.is_active = False  # Deactivates AI

    def activate(self):
        self.is_active = True  # Actives AI automatically

