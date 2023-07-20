import numpy as numpy
import math 

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    numpy.linalg.norm
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.x = y

    def print(self):
        print(f"[{self.x}, {self.y}]", end=' ')


def prox_index(points, x):
    dif = abs(points[0].x - x)
    index = 0
    for i in range(len(points)):
        if abs(points[i].x - x) < dif:
            dif = abs(points[i].x - x)
            index = i
    return index


def get_points(points, index, n):
    left = index
    right = index
    for i in range(n - 1):
        if i % 2 == 0:
            if left == 0:
                right += 1
            else:
                left -= 1
        else:
            if right == len(points) - 1:
                left -= 1
            else:
                right += 1
    return points[left:right + 1]


def newton_table(table):
    row_count = 2
    sub_table = []
    [sub_table.append([point.x, point.y]) for point in table]

    sub_table = list([list(row) for row in numpy.transpose(sub_table)])
    x_data = sub_table[0]
    for i in range(1, len(x_data)):
        sub_table.append([])
        y_row = sub_table[len(sub_table) - row_count]
        for j in range(0, len(x_data) - i):
            if y_row[j] is None and y_row[j + 1] is None:
                cur = 1
            elif y_row[j] is None:
                cur = y_row[j + 1] / (x_data[j] - x_data[j + i])
            elif y_row[j + 1] is None:
                cur = y_row[j] / (x_data[j] - x_data[j + i])
            else:
                cur = (y_row[j] - y_row[j + 1]) / (x_data[j] - x_data[j + i])
            sub_table[i + row_count - 1].append(cur)
    return sub_table


def newton(point_table, n, x):
    table = get_points(point_table, prox_index(point_table, x), n)
    subs = newton_table(table)
    return calc(subs, x)


def calc(table, x):
    y_x = 0.0
    x_data = table[0]
    for i in range(1, len(table)):
        member_val = table[i][0]
        for j in range(i - 1):
            member_val *= (x - x_data[j])
        y_x += member_val
    return y_x


def get_new_table(data):
    new_data = []
    for i in range(len(data)):
        new_data.append([])
        for j in range(len(data[i])):
            equalization_variable = math.log(data[i][j])
            new_data[i].append(abs(equalization_variable - data[i][j]))

    return new_data

# Производим двумерную интерполяцю
# nx / ny - степень интерполяции по осям Oх, Oу
def newton_2d_int(x, y, data, nx, ny, xp, yp):
    # new_data  = get_new_table(data)
    y_values = []
    for i in range(len(y)):
        x_values = []
        for j in range(len(x)):
            # x_values.append(Point(x[j], new_data[i][j]))
            x_values.append(Point(x[j], data[i][j]))
        y_values.append(Point(y[i], newton(x_values, nx, xp)))
    return newton(y_values, ny, yp)


def gauss_method(mtr, f):
    n = len(f)
    for i in range(n):
        for k in range(i + 1, n):
            c = -mtr[k][i] / mtr[i][i]
            for j in range(i, n):
                if i == j:
                    mtr[k][j] = 0
                else:
                    mtr[k][j] += c * mtr[i][j]
            f[k] += c * f[i]
    x = [0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        x[i] = f[i]
        for j in range(i + 1, n):
            x[i] -= mtr[i][j] * x[j]
        x[i] /= mtr[i][i]
    return x
