import random


class Food:
    """Food that appears at a random free cell."""
    def __init__(self, field, snake):
        self.position = self._random_position(field, snake)

    def _random_position(self, field, snake):
        """Return a random cell not occupied by the snake."""
        while True:
            pos = (random.randint(0, field.grid_height - 1),
                   random.randint(0, field.grid_width - 1))
            if pos not in snake.positions:
                return pos

    def respawn(self, field, snake):
        """Move food to a new location."""
        self.position = self._random_position(field, snake)

