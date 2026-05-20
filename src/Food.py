import random


class Food:
    """Игровая еда (яблоко)."""
    def __init__(self, field, snake):
        self.position = self._random_position(field, snake)

    def _random_position(self, field, snake):
        """Генерация координат яблока на свободных от змейки клетках."""
        while True:
            pos = (random.randint(0, field.grid_height - 1),
                   random.randint(0, field.grid_width - 1))
            if pos not in snake.positions:
                return pos

    def respawn(self, field, snake):
        """Перемещение яблока на новую позицию."""
        self.position = self._random_position(field, snake)

