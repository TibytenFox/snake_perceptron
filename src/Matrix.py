import math
import random


def sigmoid(x):
    return 1 / (1 + math.e ** (-x))

def column(arr: list):
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

    def fromArray(self, arr: list):
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = arr[i * self.cols + j]

    def toArray(self):
        res = []
        for i in range(self.rows):
            for j in range(self.cols):
                res.append(self.matrix[i][j])

        return res

    def randomize(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = random.uniform(-1, 1)

    def addBias(self):
        res = Matrix(self.rows + 1, 1)
        for i in range(self.rows):
            res.matrix[i][0] = self.matrix[i][0]
        res.matrix[self.rows][0] = 1

        return res

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if not (self.cols == other.rows): return
            res = Matrix(self.rows, other.cols)

            for i in range(self.cols):
                for j in range(other.rows):
                    for ind in range(self.cols):
                        res.matrx[i][j] += self.matrix[i + ind] * other.matrix[j + ind]

            return res

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

            return res

    def activate(self):
        res = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                res.matrix[i][j] = sigmoid(self.matrix[i][j])

        return res

    def mutate(self, mutation_rate):
        for i in range(self.rows):
            for j in range(self.cols):
                random_num = random.random()
                if random_num < mutation_rate:
                    self.matrix[i][j] += random.gauss() / 5 # очень маленькое число

                    if self.matrix[i][j] < -1: self.matrix[i][j] = -1
                    if self.matrix[i][j] > 1: self.matrix[i][j] = 1

    def crossover(self, partner):
        child = Matrix(self.rows, self.cols)

        random_row = random.randint(0, self.rows - 1)
        random_col = random.randint(0, self.cols - 1)

        for i in range(self.rows):
            for j in range(self.cols):
                if i < random_row or (i == random_col and j <= random_col):
                    child.matrix[i][j] = self.matrix[i][j]
                else:
                    child.matrix[i][j] = partner.matrix[i][j]

        return child

    def transpose(self):
        res = Matrix(self.cols, self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                res.matrix[j][i] = self.matrix[i][j]

        return res

    def clone(self):
        res = Matrix(self.rows, self.cols)

        for i in range(self.rows):
            for j in range(self.cols):
                res.matrix[i][j] = self.matrix[i][j]

        return res


