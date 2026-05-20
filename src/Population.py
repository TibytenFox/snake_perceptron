import random
from Snake import Snake
from Field import Field


class Population:
	snakes: list[Snake]
	gen: int

	def __init__(self, size, field):
		self.snakes = []
		self.gen = 1

		for i in range(size):
			self.snakes.append(Snake(field))

	def update(self):
		for i in range(len(self.snakes)):
			if self.snakes[i].alive:
				self.snakes[i].look()
				self.snakes[i].change_direction_ai()
				self.snakes[i].move()

	def is_done(self):
		for snake in self.snakes:
			if snake.alive: 
				return False
			
		return True
	
	def calculate_fintess(self):
		for i in range(len(self.snakes)):
			self.snakes[i].calculate_fitness()

	def natural_selection(self, elite_count=2):
		new_snakes = []

		sorted_snakes = sorted(self.snakes, key=lambda s: s.fitness, reverse=True)
		for i in range(elite_count):
			new_snakes.append(sorted_snakes[i].clone())

		while len(new_snakes) < len(self.snakes):
			parent1 = self.select_snake()
			parent2 = self.select_snake()

			child = parent1.crossover(parent2)
			new_snakes.append(child)

		self.snakes = new_snakes.copy()
		self.gen += 1

	def mutate(self, mutation_rate):
		for i in range(len(self.snakes)):
			self.snakes[i].mutate(mutation_rate)

	def select_snake(self):
		fitness_sum = sum([self.snakes[i].fitness for i in range(len(self.snakes))])

		rand = int(random.uniform(0, fitness_sum))
		running_sum = 0

		for i in range(len(self.snakes)):
			running_sum += self.snakes[i].fitness
			if running_sum > rand:
				return self.snakes[i]

		return self.snakes[0]
	
	def get_best_snake(self):
		res = max([(self.snakes[i].fitness, i) for i in range(len(self.snakes))])
		return self.snakes[res[1]]
	
	def save_population(self):
		for i in range(len(self.snakes)):
			self.snakes[i].save_to_file()

	def read_population(self):
		for i in range(len(self.snakes)):
			self.snakes[i].read_from_file()