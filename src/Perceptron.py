from Matrix import *

class Perceptron:
	input_nodes: int
	hidden_nodes: int
	output_nodex: int

	weigths_ih: Matrix
	weights_hh: Matrix
	weights_ho: Matrix

	def __init__(self, input, hidden, output):
		