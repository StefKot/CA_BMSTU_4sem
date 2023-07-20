from in_out import *
from matplotlib import pyplot as plt
from scipy.misc import derivative
import numpy as np


infinity = None


# x1 = xi-1
# x2 = xi
def H(x1, x2):
    return x2 - x1


# расчет коэффициента А
def A(x):
    return x


def C(c_i, ksi_i, teta_i):
    return ksi_i * c_i + teta_i


# расчет всех значений коэффициентов A
def calc_values_a(values_y):

    values_a = list()
    for i in range(len(values_y) - 1):
        values_a.append(A(values_y[i]))
    return values_a
    # return values_y[:-1]


# y1 = yi-2
# y2 = yi-1
# y3 = yi
# h1 = hi-1
# h2 = hi
def fi(y1, y2, y3, h1, h2):
    return 3 * ((y3 - y2) / h2 - (y2 - y1) / h1)


# функция ksi - расcчтывает значение ksi i-го элемента
# ksi_i+1 = -h_i / (h_i-1  * ksi_i-1 * (h_i - h_i-1))
# ksi_i = -h_i-1 / (h_i  * ksi_i + 2 * (h_i-1 - h_i))
# ksi1 = ksi_i-1
# h1 = h_i-1
# h2 = h_i
def ksi(ksi1, h1, h2):
    return - h2 / (h1 * ksi1 + 2 * (h2 + h1))


# fi - значение из функции fi()
# teta - teta_i-1
# ksi - ksi_i-1
# h1 - h_i-1
# h2 - h_i
def teta(fi, teta_i, ksi_i, h1, h2):
    return (fi - h1 * teta_i) / (h1 * ksi_i + 2 * (h2 + h1))


def calc_values_h(values_x):

    h_values = list()
    for i in range(1, len(values_x)):
        h_values.append(H(values_x[i], values_x[i - 1]))

    return h_values


def calc_values_c(values_x, values_y, start, end):

    sizeX = len(values_x)

    cValues = [0] * (sizeX - 1)
    cValues[0] = start
    cValues[1] = start

    ksiValues = [start, start]
    tetvalues_a = [start, start]

    for i in range(2, sizeX):
        h2 = values_x[i] - values_x[i - 1]       # hi
        h1 = values_x[i - 1] - values_x[i - 2]   # hi-1

        fiCur = fi(values_y[i - 2], values_y[i - 1], values_y[i], h1, h2)
        ksiCur = ksi(ksiValues[i - 1], h1, h2)
        tetaCur = teta(fiCur, tetvalues_a[i - 1], ksiValues[i - 1], h1, h2)

        ksiValues.append(ksiCur)
        tetvalues_a.append(tetaCur)

    cValues[-1] = end

    for i in range(sizeX - 2, 0, -1):
        cValues[i - 1] = C(cValues[i], ksiValues[i], tetvalues_a[i])

    return cValues


# y1 = y_i-1
# y2 = y_i
# hi
# c1 = c_i+1
# c2 = c_i
def B(y1, y2, c1, c2, hi):
    return (y2 - y1) / hi - (hi * (c2 + 2 * c1) / 3)


def D(c1, c2, hi):
    return (c1 - c2) / (3 * hi)


def calc_values_b(values_x, values_y, cValues):

    bValues = list()

    for i in range(1, len(values_x) - 1):
        hi = values_x[i] - values_x[i - 1]
        bValues.append(B(values_y[i - 1], values_y[i], cValues[i - 1], cValues[i], hi))

    hi = values_x[-1] - values_x[-2]
    bValues.append(B(values_y[-2], values_y[-1], 0, cValues[-1], hi))

    return bValues


def calc_values_d(values_x, cValues):

    dValues = []

    size = len(values_x)

    for i in range(1, size - 1):
        hi = values_x[i] - values_x[i - 1]
        dValues.append(D(cValues[i], cValues[i - 1], hi))

    hi = values_x[-1] - values_x[-2]
    dValues.append(D(0, cValues[-1], hi))

    return dValues


def calculateCoefsSpline(values_x, values_y, start, end):

    values_a = calc_values_a(values_y)
    cValues = calc_values_c(values_x, values_y, start, end)
    bValues = calc_values_b(values_x, values_y, cValues)
    dValues = calc_values_d(values_x, cValues)

    return values_a, bValues, cValues, dValues


def finedIndex(values_x, x):

    size = len(values_x)
    index = 1

    while index < size and values_x[index] < x:
        index += 1

    return index - 1


def countPolynom(x, values_x, index, coefs):

    h = x - values_x[index]
    y = 0

    for i in range(4):
        y += coefs[i][index] * (h ** i)

    return y


def printSplineFunct(table, x, start, end):

    values_x = [i.getX() for i in table]
    values_y = [i.getY() for i in table]

    index = finedIndex(values_x, x)
    coeffs = calculateCoefsSpline(values_x, values_y, start, end)

    print("x = {:.6g}".format(x))

    print("Ф(x) = {:.6g}".format(coeffs[0][index]), end=" ")
    for i in range(1, len(coeffs)):
        print("+ {:.6f}".format(coeffs[i][index]), "* (x -", values_x[index], end=") ")

    y = countPolynom(x, values_x, index, coeffs)
    print("= {:.6f}".format(y))


def spline(table, x, start, end):
    values_x = [i.getX() for i in table]
    values_y = [i.getY() for i in table]

    coeffs = calculateCoefsSpline(values_x, values_y, start, end)

    index = finedIndex(values_x, x)

    y = countPolynom(x, values_x, index, coeffs)

    return y


# нахождение индекса ближайшей точки по значению к искомой
def getIndex(points, x):

    dif = abs(points[0].getX() - x)
    index = 0
    for i in range(len(points)):
        if abs(points[i].getX() - x) < dif:
            dif = abs(points[i].getX() - x)
            index = i
    return index


# взятие рабочих ближайших точек для расчетов
def getWorkingPoints(points, index, n):
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


# Расчет полином Ньютона м результаты в виде таблицы всех данных f(xi .... xn)
def NewtonMethod(point_table):

    countOfRowsOfTableData = 2
    table_of_sub = []
    [table_of_sub.append([point.getX(), point.getY()]) for point in point_table]

    table_of_sub = list([list(row) for row in np.transpose(table_of_sub)])
    XRow = table_of_sub[0]

    # Добавление столбцов (строк в моей реализации)
    for countOfArgs in range(1, len(XRow)):
        table_of_sub.append([])
        curYRow = table_of_sub[len(table_of_sub) - countOfRowsOfTableData]

        # Добавление очередного элемента
        for j in range(0, len(XRow) - countOfArgs):
            if curYRow[j] == infinity and curYRow[j + 1] == infinity:
                cur = 1
            elif curYRow[j] == infinity:
                cur = curYRow[j + 1] / (XRow[j] - XRow[j + countOfArgs])
            elif curYRow[j + 1] == infinity:
                cur = curYRow[j] / (XRow[j] - XRow[j + countOfArgs])
            else:
                cur = (curYRow[j] - curYRow[j + 1]) / (XRow[j] - XRow[j + countOfArgs])
            table_of_sub[countOfArgs + countOfRowsOfTableData - 1].append(cur)

    return table_of_sub


def newtonPolynom(point_table, n, x):

    working_table = getWorkingPoints(point_table, getIndex(point_table, x), n)
    subs = NewtonMethod(working_table)
    return calcApproximateValue(subs, n, x)


def findDerivativeNewtonPolynom(point_table, n, x):

    def aprox_func(x):
        return newtonPolynom(point_table, n, x)

    y_derivative_n_2 = derivative(aprox_func, x, n=2, dx=1e-6)

    return y_derivative_n_2


# Расчет конечного результат по полиному Ньютона
def calcApproximateValue(table_of_sub, n, x):

    countOfArgs = 2

    if table_of_sub[1][0] == infinity:
        sum = table_of_sub[1][1]
    else:
        sum = table_of_sub[1][0]

    mainPart = 1

    for i in range(n - 1):
        if table_of_sub[0][i] == infinity:
            print(3)
            mainPart *= x
        else:
            mainPart *= (x - table_of_sub[0][i])

        if table_of_sub[i + countOfArgs][0] != infinity:
            sum += mainPart * table_of_sub[i + countOfArgs][0]

    return sum


def main():

    data_table = read_table("./data.txt")
    print_table(data_table)

    degree = 4
    x_value = float(input("Enter the value of x: "))

    start_1 = 0
    end_1 = 0
    start_2 = 0
    end_2 = 0
    start_3 = 0
    end_3 = 0

    y_values = [list(), list(), list(), list()]

    if degree < len(data_table):
        print("\nNewton polynomial of degree 3: ", newtonPolynom(data_table, degree + 1, x_value), "\n")

        start_2 = findDerivativeNewtonPolynom(data_table, degree + 1, data_table[0].x)
        start_3 = findDerivativeNewtonPolynom(data_table, degree + 1, data_table[0].x)
        end_3 = findDerivativeNewtonPolynom(data_table, degree + 1, data_table[-1].x)
    else:
        print("Cannot compute Newton polynomial of degree", degree, "as there are only", len(data_table), "points")

    print("Spline with start=0 and end=0:          ", spline(data_table, x_value, start_1, end_1))
    print("Spline with start=0 and end=P''(xn):    ", spline(data_table, x_value, start_2, end_2))
    print("Spline with start=P''(x0) and end=P''(xn): ", spline(data_table, x_value, start_3, end_3), "\n")

    x_values = np.linspace(data_table[0].x, data_table[-1].x, 100)

    if degree < len(data_table):
        for x_i in x_values:
            y_values[3].append(newtonPolynom(data_table, degree + 1, x_i))

    for x_i in x_values:
        y_values[0].append(spline(data_table, x_i, start_1, end_1))

    for x_i in x_values:
        y_values[1].append(spline(data_table, x_i, start_2, end_2))

    for x_i in x_values:
        y_values[2].append(spline(data_table, x_i, start_3, end_3))

    plt.plot(x_values, y_values[0], '-', color='g')
    plt.plot(x_values, y_values[1], '-', color='r')
    plt.plot(x_values, y_values[2], '-', color='b')

    if degree < len(data_table):
        plt.plot(x_values, y_values[3], ':', color='r')

    plt.show()


if __name__ == "__main__":

    main()
    