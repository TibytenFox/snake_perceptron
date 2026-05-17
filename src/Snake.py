import pygame


class Snake:
    """Manual snake controlled by arrow keys."""
    def __init__(self, field):
        self.field = field
        center_row = field.grid_height // 2
        center_col = field.grid_width // 2
        self.positions = [
            (center_row, center_col),
            (center_row, center_col - 1),
            (center_row, center_col - 2)
        ]
        self.direction = "right"
        self.next_direction = "right"
        self.score = 0
        self.alive = True

    def change_direction(self, key):
        """Change snake direction based on key press (no 180° turns)."""
        if key == pygame.K_UP and self.direction != "down":
            self.next_direction = "up"
        elif key == pygame.K_DOWN and self.direction != "up":
            self.next_direction = "down"
        elif key == pygame.K_LEFT and self.direction != "right":
            self.next_direction = "left"
        elif key == pygame.K_RIGHT and self.direction != "left":
            self.next_direction = "right"

    def move(self, food):
        """Move snake one step, check collisions and food."""
        if not self.alive:
            return

        self.direction = self.next_direction

        # Calculate new head position
        head = self.positions[0]
        if self.direction == "up":
            new_head = (head[0] - 1, head[1])
        elif self.direction == "down":
            new_head = (head[0] + 1, head[1])
        elif self.direction == "left":
            new_head = (head[0], head[1] - 1)
        else:  # right
            new_head = (head[0], head[1] + 1)

        # Insert new head
        self.positions.insert(0, new_head)

        # Check food collision
        if new_head == food.position:
            self.score += 1
            food.respawn(self.field, self)
        else:
            # Remove tail only if no food eaten
            self.positions.pop()

        # Check collisions with walls or self
        row, col = self.positions[0]
        if (row < 0 or row >= self.field.grid_height or
            col < 0 or col >= self.field.grid_width):
            self.alive = False

        if self.positions[0] in self.positions[1:]:
            self.alive = False

    def reset(self):
        """Reset snake to initial state."""
        center_row = self.field.grid_height // 2
        center_col = self.field.grid_width // 2
        self.positions = [
            (center_row, center_col),
            (center_row, center_col - 1),
            (center_row, center_col - 2)
        ]
        self.direction = "right"
        self.next_direction = "right"
        self.score = 0
        self.alive = True
