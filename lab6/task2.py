a0, a1, a2 = 1, 2, 3


def second_runge_(y, h):
    res = [None, None]
    temp = left_side_diff(y, h)
    for i in range(2, len(y)):
        res.append(2 * temp[i] - ((y[i] - y[i - 2]) / (2 * h)))
    res[4] += 0.1
    return res

def get_table():
    x_tbl = [1, 2, 3, 4, 5, 6]
    y_tbl = [0.571, 0.889, 1.091, 1.231, 1.333, 1.412]
    return x_tbl, y_tbl

rec = 0.183
def f(x):
    return a0 * x / (a1 + a2 * x)


def df(x):
    return (a0 * (a1 + a2 * x) - a0 * x * a2) / ((a1 + a2 * x) ** 2)


def left_side_diff(y, h):
    res = [None]
    for i in range(1, len(y)):
        res.append((y[i] - y[i - 1]) / h)
    return res


def right_side_diff(y, h):
    res = []
    for i in range(len(y) - 1):
        res.append((y[i + 1] - y[i]) / h)
    res.append(None)
    return res


def center_diff(y, h):
    res = [None]
    for i in range(1, len(y) - 1):
        res.append((y[i + 1] - y[i - 1]) / (2 * h))
    res.append(None)
    return res


def second_diff(y, h):
    res = [None]
    for i in range(1, len(y) - 1):
        res.append((y[i - 1] - 2 * y[i] + y[i + 1]) / h**2)
    res.append(None)
    return res

def second_runge(y, h):
    res = [None, None]
    temp = left_side_diff(y, h)
    for i in range(2, len(y)):
        res.append(2 * temp[i] - ((y[i] - y[i - 2]) / (2 * h)))
    return res


def nu(y_val):
    return 1 / y_val


def ksi(x_val):
    return 1 / x_val


def align_vars_diff(xs, ys):
    res = []
    for i in range(len(ys) - 1):
        eta_ksi_diff = (nu(ys[i + 1]) - nu(ys[i])) / (ksi(xs[i + 1]) - ksi(xs[i]))
        y = ys[i]
        x = xs[i]
        res.append(eta_ksi_diff * y**2 / x**2)
    res.append(None)
    return res


def print_res_line(text, res):
    print("{:<20}".format(text), end="")
    for i in res:
        if (i != None):
            print("{: <15.4f}".format(i), end="")
        else:
            print("{: <15}".format("None"), end="")
    print()


hx = 1
x, y = get_table()
print_res_line("x:", x)
print_res_line("y:", y)
print_res_line("y':", [df(i) for i in x])
print_res_line("Left side:", left_side_diff(y, hx))
print_res_line("Right side:", right_side_diff(y, hx))
print_res_line("Center differences:", center_diff(y, hx))
print_res_line("Runge second:", second_runge_(y, hx))
print_res_line("Diff second:", second_diff(y, hx))
print_res_line("Aligning:", align_vars_diff(x, y))
