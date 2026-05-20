from Matrix import *

class Perceptron:
	"""Многослойный перцептрон (архитектура мозга ИИ)."""
	input_nodes: int
	hidden_nodes: int
	output_nodes: int

	# Матрицы весов связей слоев
	whi: Matrix
	whh: Matrix
	woh: Matrix

	def __init__(self, input_count, hidden_count, output_count):
		self.input_nodes = input_count
		self.hidden_nodes = hidden_count
		self.output_nodes = output_count

		# Инициализация матриц (+1 для нейрона смещения Bias)
		self.whi = Matrix(self.hidden_nodes, self.input_nodes + 1)
		self.whh = Matrix(self.hidden_nodes, self.hidden_nodes + 1)
		self.woh = Matrix(self.output_nodes, self.hidden_nodes + 1)

		self.whi.randomize()
		self.whh.randomize()
		self.woh.randomize()

	def mutate(self, mutation_rate):
		"""Мутация всех весовых матриц."""
		self.whi.mutate(mutation_rate)
		self.whh.mutate(mutation_rate)
		self.woh.mutate(mutation_rate)

	def output(self, input_arr):
		"""Прямой проход сигнала через слои нейросети (Feedforward)."""
		inputs = column(input_arr)
		input_bias = inputs.add_bias()

		# Проход первого скрытого слоя
		hidden_inputs = self.whi * input_bias
		hidden_outputs = hidden_inputs.activate()
		hidden_outputs_bias = hidden_outputs.add_bias()

		# Проход второго скрытого слоя
		hidden_inputs2 = self.whh * hidden_outputs_bias
		hidden_outputs2 = hidden_inputs2.activate()
		hidden_outputs_bias2 = hidden_outputs2.add_bias()

		# Выходной слой
		output_inputs = self.woh * hidden_outputs_bias2
		outputs = output_inputs.activate()

		return outputs.to_array()

	def crossover(self, partner):
		"""Скрещивание матриц весов с матрицами партнера."""
		child = Perceptron(self.input_nodes, self.hidden_nodes, self.output_nodes)

		child.whi = self.whi.crossover(partner.whi)
		child.whh = self.whh.crossover(partner.whh)
		child.woh = self.woh.crossover(partner.woh)

		return child

	def clone(self):
		"""Клонирование структуры и весов перцептрона."""
		res = Perceptron(self.input_nodes, self.hidden_nodes, self.output_nodes)

		res.whi = self.whi.clone()
		res.whh = self.whh.clone()
		res.woh = self.woh.clone()

		return res

