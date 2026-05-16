import math
import random


def sigmoid(x):
	return 1 / (1 + math.e ** (-x))

def column(arr):
	res = Matrix(len(arr), 1)
	for i in range(len(arr)):
		res.matrix[i][0] = arr[i]
	
	return arr

class Matrix:
	rows: int
	cols: int
	data: [[float]]

	def __init__(self, *args, **kwargs):
		if "data" in kwargs:
            self.rows = len(kwargs["data"])
            self.cols = len(kwargs["data"][0])
            self.matrix = kwargs["data"].copy()
            return
        self.rows = args[0]
        self.cols = args[1]
        self.matrix = [[0 for _ in range(self.cols)] for __ in range(self.rows)]

	def fromArray(self, arr):
		for i in range(self.rows):
			for j in range(self.cols):
				self.matrix[i][j] = arr[i * self.cols + j]

	def toArray(self):
		res = []
		for i in range(self.rows):
			for j in range(self.cols):
				res.append(self.matrix[i][j])

	def randomize(self):
		for i in range(self.rows):
			for j in range(self.cols):
				self.matrix[i][j] = random.uniform(-1, 1)

	def __mul__(self, other):
		if isinstance(other, Matrix):
			if not (self.cols == other.rows): return 
			res = Matrix(self.rows, other.cols)

			for i in range(self.cols):
				for j in range(other.rows):
					for ind in range(self.cols):
						res.matrx[i][j] += self.matrix[i + ind] * other.matrix[j + ind]

			return new_matrix

		res = Matrix(self.rows, self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				res.matrix[i][j] = self.matrix[i][j] * other

		return res

	def __add__(self, other):
		if isinstance(other, Matrix):
            if not (self.rows == other.rows and self.cols == other.cols): return 
			
			res = Matrix(self.rows, self.cols)
			for i in range(self.rows):
				for j in range(self.cols):
					res.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]

			return res

	def __sub__(self, other):
		if isinstance(other, Matrix):
            if not (self.rows == other.rows and self.cols == other.cols): return 
			
			res = Matrix(self.rows, self.cols)
			for i in range(self.rows):
				for j in range(self.cols):
					res.matrix[i][j] = self.matrix[i][j] - other.matrix[i][j]

			return new_matrix

	def activate(self):
		res = Matrix(self.rows, self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				res.matrix[i][j] = sigmoid(self.matrix[i][j])

		return res

	def transpose(self):
		res = Matrix(self.cols, self.rows)
		for i in range(self.rows):
			for j in range(self.cols):
				res.matrix[j][i] = self.matrix[i][j]

		return new_matrix

	def clone(self):
        res = Matrix(self.rows, self.cols)

        for i in range(self.rows):
            for j in range(self.cols):
                res.matrix[i][j] = self.matrix[i][j]

        return res


	