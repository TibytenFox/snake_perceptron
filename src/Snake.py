import pygame
from Food import Food
from Perceptron import Perceptron
from Field import Field


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
        self.food = Food(field, self)

        self.brain = Perceptron(20, 18, 4)
        self.decision = []
        self.vision = [0] * 20

        self.time_to_live = 200
        self.life_time = 0
        self.fitness = 0

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

    def look(self):
        self.vision = [0] * 20
        dirs = ["up", "up-right", "right", "down-right", "down", "down-left", "left", "up-left"]

        border_dis = self.get_border_dis()
        for i in range(8):
            self.vision[i] = border_dis[dirs[i]]

        body_dis = self.get_body_dis()
        for i in range(8):
            self.vision[8 * 1 + i] = body_dis[dirs[i]]

        dirs = ["up", "left", "down", "right"]
        apple_dis = self.get_apple_dis()
        for i in range(4):
            self.vision[8 * 2 + i] = apple_dis[dirs[i]]

    def get_border_dis(self):
        return {"up": 1 / (self.positions[0][0] + 1),
                "up-right": 1 / (min(self.positions[0][0], self.field.grid_width - 1 - self.positions[0][1]) + 1),
                "left": 1 / (self.positions[0][1] + 1),
                "up-left": 1 / (min(self.positions[0]) + 1),
                "down": 1 / (self.field.grid_height - 1 - self.positions[0][0] + 1),
                "down-right": 1 / (
                        min(self.field.grid_height - 1 - self.positions[0][0], self.field.grid_width - 1 - self.positions[0][1]) + 1),
                "down-left": 1 / (min(self.field.grid_height - 1 - self.positions[0][0], self.positions[0][1]) + 1),
                "right": 1 / (self.field.grid_width - 1 - self.positions[0][1] + 1)
                }
    
    def get_body_dis(self):
        directions = {"left": 0,
                      "up-left": 0,
                      "right": 0,
                      "up-right": 0,
                      "up": 0,
                      "down-left": 0,
                      "down": 0,
                      "down-right": 0
                      }
        
        head = self.positions[0]

        for i in range(head[1] - 1, -1, -1):
            if (head[0], i) in self.positions:
                directions["left"] = 1 / (head[1] - i)
                break

        for i in range(head[1] + 1, self.field.grid_width):
            if (head[0], i) in self.positions:
                directions["right"] = 1 / (i - head[1])
                break

        for i in range(head[0] + 1, self.field.grid_height):
            if (i, head[1]) in self.positions:
                directions["down"] = 1 / (i - head[0])
                break

        for i in range(head[0] - 1, -1, -1):
            if (i, head[1]) in self.positions:
                directions["up"] = 1 / (head[0] - i)
                break

        for i in range(1, min(head) + 1):
            if (head[0] - i, head[1] - i) in self.positions:
                directions["up-left"] = 1 / i
                break

        for i in range(1, min(head[0], self.field.grid_width - 1 - head[1]) + 1):
            if (head[0] - i, head[1] + i) in self.positions:
                directions["up-right"] = 1 / i
                break

        for i in range(1, min(self.field.grid_height - 1 - head[0], self.field.grid_width - 1 - head[1]) + 1):
            if (head[0] + i, head[1] + i) in self.positions:
                directions["down-right"] = 1 / i
                break

        for i in range(1, min(self.field.grid_height - 1 - head[0], head[1]) + 1):
            if (head[0] + i, head[1] - i) in self.positions:
                directions["down-left"] = 1 / i
                break

        return directions
    
    def get_apple_dis(self):
        directions = {"left": 0,
                      "right": 0,
                      "up": 0,
                      "down": 0,
                      }
        head = self.positions[0]

        if head[0] <= self.food.position[0]:
            directions["down"] = 1 / (self.food.position[0] - head[0] + 1)
        if head[0] >= self.food.position[0]:
            directions["up"] = 1 / (head[0] - self.food.position[0] + 1)
        if head[1] <= self.food.position[1]:
            directions["right"] = 1 / (self.food.position[1] - head[1] + 1)
        if head[1] >= self.food.position[1]:
            directions["left"] = 1 / (head[1] - self.food.position[1] + 1)

        return directions

    def change_direction_ai(self):
        self.decision = self.brain.output(self.vision)

        opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}
        forbidden = opposite[self.direction]
        idx_map = {"up": 0, "down": 1, "left": 2, "right": 3}
        self.decision[idx_map[forbidden]] = -float('inf')

        res = max([(self.decision[i], i) for i in range(len(self.decision))])

        if res[1] == 0:
            self.next_direction = "up"
        elif res[1] == 1:
            self.next_direction = "down"
        elif res[1] == 2:
            self.next_direction = "left"
        elif res[1] == 3:
            self.next_direction = "right"

    def mutate(self, mutation_rate):
        self.brain.mutate(mutation_rate)

    def calculate_fitness(self):
        if self.score < 2:
            self.fitness = self.life_time * (self.score + 1)
        else:
            self.fitness = self.life_time * (self.score ** 2)

    def crossover(self, partner):
        child = Snake(self.field)
        child.brain = child.brain.crossover(partner.brain)
        return child

    def move(self):
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

        self.time_to_live -= 1
        self.life_time += 1

        # Check food collision
        if new_head == self.food.position:
            self.score += 1
            self.time_to_live += 100
            self.food.respawn(self.field, self)
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

        if self.time_to_live < 0:
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

        self.time_to_live = 200
        self.life_time = 0
        self.fitness = 0
