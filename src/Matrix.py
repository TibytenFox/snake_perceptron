import math
import random


def sigmoid(x):
    """Функция активации сигмоида."""
    return 1 / (1 + math.e ** (-x))

def column(arr: list):
    """Преобразование одномерного массива в матрицу-столбец."""
    res = Matrix(len(arr), 1)
    for i in range(len(arr)):
        res.matrix[i][0] = arr[i]

    return res

class Matrix:
    """Математическое ядро для работы с матрицами весов."""
    rows: int
    cols: int
    data: list[list[float]]

    def __init__(self, *args, **kwargs):
        if "data" in kwargs:
            self.rows = len(kwargs["data"])
            self.cols = len(kwargs["data"][0])
            self.matrix = kwargs["data"].copy()
            return
        self.rows = args[0]
        self.cols = args[1]
        self.matrix = [[0 for _ in range(self.cols)] for __ in range(self.rows)]

    def from_array(self, arr: list):
        """Заполнение матрицы из плоского списка."""
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = arr[i * self.cols + j]

    def to_array(self):
        """Конвертация матрицы в плоский список."""
        res = []
        for i in range(self.rows):
            for j in range(self.cols):
                res.append(self.matrix[i][j])

        return res

    def randomize(self):
        """Заполнение случайными числами от -1 до 1."""
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = random.uniform(-1, 1)

    def add_bias(self):
        """Добавление строки/нейрона смещения (Bias) со значением 1."""
        res = Matrix(self.rows + 1, 1)
        for i in range(self.rows):
            res.matrix[i][0] = self.matrix[i][0]
        res.matrix[self.rows][0] = 1

        return res

    def __mul__(self, other):
        """Умножение матриц или матрицы на число."""
        if isinstance(other, Matrix):
            if self.cols != other.rows: return
            res = Matrix(self.rows, other.cols)

            for i in range(self.rows):
                for j in range(other.cols):
                    for ind in range(self.cols):
                        res.matrix[i][j] += self.matrix[i][ind] * other.matrix[ind][j]

            return res

        res = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                res.matrix[i][j] = self.matrix[i][j] * other

        return res

    def __add__(self, other):
        """Поэлементное сложение двух матриц."""
        if isinstance(other, Matrix):
            if not (self.rows == other.rows and self.cols == other.cols): return 

            res = Matrix(self.rows, self.cols)
            for i in range(self.rows):
                for j in range(self.cols):
                    res.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]

            return res

    def __sub__(self, other):
        """Поэлементное вычитание двух матриц."""
        if isinstance(other, Matrix):
            if not (self.rows == other.rows and self.cols == other.cols): return 

            res = Matrix(self.rows, self.cols)
            for i in range(self.rows):
                for j in range(self.cols):
                    res.matrix[i][j] = self.matrix[i][j] - other.matrix[i][j]

            return res

    def activate(self):
        """Применение сигмоиды ко всем элементам матрицы."""
        res = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                res.matrix[i][j] = sigmoid(self.matrix[i][j])

        return res

    def mutate(self, mutation_rate):
        """Гауссовская мутация весов с ограничением в диапазоне [-1, 1]."""
        for i in range(self.rows):
            for j in range(self.cols):
                random_num = random.random()
                if random_num < mutation_rate:
                    self.matrix[i][j] += random.gauss(0, 1) 

                    if self.matrix[i][j] < -1: self.matrix[i][j] = -1
                    if self.matrix[i][j] > 1: self.matrix[i][j] = 1

    def crossover(self, partner):
        """Двумерный одноточечный кроссовер весов с партнером."""
        child = Matrix(self.rows, self.cols)

        random_row = random.randint(0, self.rows - 1)
        random_col = random.randint(0, self.cols - 1)

        for i in range(self.rows):
            for j in range(self.cols):
                if i < random_row or (i == random_row and j <= random_col):
                    child.matrix[i][j] = self.matrix[i][j]
                else:
                    child.matrix[i][j] = partner.matrix[i][j]

        return child

    def transpose(self):
        """Транспонирование матрицы."""
        res = Matrix(self.cols, self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                res.matrix[j][i] = self.matrix[i][j]

        return res

    def clone(self):
        """Копирование значений матрицы."""
        res = Matrix(self.rows, self.cols)

        for i in range(self.rows):
            for j in range(self.cols):
                res.matrix[i][j] = self.matrix[i][j]

        return res


