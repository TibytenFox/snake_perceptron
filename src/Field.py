import pygame
import sys
from Snake import *


class Field:
    """Game field: manages drawing, grid, and game state."""
    def __init__(self, width=640, height=480, cell_size=20):
        pygame.init()
        
        # Try to initialize the font module
        self.font_available = False
        try:
            pygame.font.init()
            # Use pygame's default font if available
            self.font = pygame.font.Font(None, 20)
            self.font_available = True
        except Exception:
            # Fallback: no text on screen, we'll use window title
            self.font_available = False
        
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid_width = width // cell_size
        self.grid_height = height // cell_size

        self.bg_color = (0, 0, 0)
        self.grid_color = (40, 40, 40)
        self.snake_color = (0, 255, 0)
        self.snake_head_color = (0, 200, 0)
        self.food_color = (255, 0, 0)

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        """Draw the background grid."""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.width, y))

    def draw_rect(self, pos, color):
        """Draw a single cell at grid position (row, col)."""
        x = pos[1] * self.cell_size
        y = pos[0] * self.cell_size
        pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))

    def display_score(self, score):
        """Show current score - either on screen or in window title."""
        if self.font_available:
            label = self.font.render(f"Score: {score}", 1, (255, 255, 0))
            self.screen.blit(label, (10, 10))
        else:
            # Fallback: show score in window title
            pygame.display.set_caption(f"Snake Game - Score: {score}")

    def update(self, snake):
        """Redraw the whole field."""
        self.screen.fill(self.bg_color)
        self.draw_grid()

        # Draw food
        self.draw_rect(snake.food.position, self.food_color)

        # Draw snake
        for i, segment in enumerate(snake.positions):
            color = self.snake_head_color if i == 0 else self.snake_color
            self.draw_rect(segment, color)

        self.display_score(snake.score)
        pygame.display.flip()
