from math import sqrt, cos, pi
from addition import newton_2d_int, gauss_method


def read_data(filename):
    res = []
    with open(filename) as f:
        f.read(3)
        x = list(map(float, f.readline().split()))
        y = list()
        f.readline()
        for line in f:
            res.append([0 for i in range(len(x))])
            data = list(map(float, line.split()))
            y_cur = data[0]
            y.append(y_cur)
            for i in range(len(x)):
                x_cur = x[i]
                res[-1][i] = data[i + 1]
    return res, x, y

def P(x, n):
    p = [1, x]
    for i in range(2, n + 1):
        p.append(((2 * i - 1) * x * p[i - 1] - (i - 1) * p[i - 2]) / i)

    return p[n]

def dP(x, n):
    return (n / (1 - x ** 2)) * (P(x, n - 1) - x * P(x, n))


def solve_Newton(i, n, eps = 1e-8):
    xn = cos(pi * ((4 * i - 1) / (4 * n + 2)))
    xn1 = xn - P(xn, n) / dP(xn, n)
    while abs(xn1 - xn) > eps:
        xn = xn1
        xn1 -= P(xn, n) / dP(xn, n)
    print(xn1)
    return xn1

def get_legendre_nodes(n):
    nodes = []
    for i in range(1, n+1):
        nodes.append(solve_Newton(i, n))

    return nodes

def get_A_coeffs(t, n):
    mtr = [[0 for j in range(n)] for i in range(n)]
    right = [0 for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mtr[i][j] = t[j] ** i
    for i in range(n):
        if i % 2 == 0:
            right[i] = 2 / (i + 1)
    return gauss_method(mtr, right)


def integrate_gauss(func, a, b, n):
    res = 0
    t = get_legendre_nodes(n)
    A = get_A_coeffs(t, n)
    for i in range(len(t)):
        x = (b - a) / 2 * t[i] + (a + b) / 2
        res += A[i] * func(x)
    res *= (b - a) / 2
    return res


def integrate_simpson(func, a, b, n):
    h = (b - a) / n
    res = 0
    x = lambda j: a + j * h
    for i in range((n - 2) // 2 + 1):
        res += func(x(2 * i)) + 4 * func(x(2 * i + 1)) + func(x(2 * i + 2))
    res *= h / 3
    return res


# интегрируем первый интеграл по симпсону, второй - по гауссу
def double_integral(func, a, b, phi, xsi, n):
    F = lambda x: integrate_simpson(lambda y: func(x, y), phi(x), xsi(x), n)
    return integrate_gauss(F, a, b, n)


def f_interp(x, y, n):
    return newton_2d_int(x_val, y_val, table, n, n, x, y)



table, x_val, y_val = read_data("data.txt")


# функции которыми мы ограничиваем область интегрирования

# ограничения по x
a = 0
b = 1
# ограничения по y
c = lambda x: 0      # y = 0
d = lambda x: 1 - x  # y = 1 - x
for n in range(1, 6):
    res = double_integral(lambda x, y: f_interp(x, y, n), a, b, c, d, 20)
    print(f"n = {n}, res = {res}")
