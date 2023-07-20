import numpy as np
from newton import newton_polynomial
from spline import spline_polynomial


type_tp = "ind"


# x - [], y - [], z - [].
# Поиск индекса в массиве x. и
# f - [zi][yi][xi]
def read_table(f_name):
    file = open(f_name, "r")
    inp = file.readlines()
    arr_x = []
    arr_y = []
    arr_z = []
    arr_f = []
    arr_fi = []
    a_inp = ""
    for line in inp:
        # Проверка на z
        if "z=" in line:
            arr_z.append(int(line.split("z=")[1]))
            if len(arr_fi) != 0:
                arr_f.append(arr_fi)
                arr_fi = []
        elif "y\\x" in line:
            if len(arr_y) == 0:
                for y in line.split()[1:]:
                    arr_y.append(int(y))
        else:
            # Если пустая строка
            if len(line.split()) == 0:
                continue
            if len(arr_x) < len(arr_y):
                arr_x.append(int(line.split()[0]))
            # Получение значений f по x в y
            arr_fk = list(map(int, line.split()[1:]))
            arr_fi.append(arr_fk)
    arr_f.append(arr_fi)
    # print("x", arr_x)
    # print("y", arr_y)
    # print("z", arr_z)
    # print("f", arr_f)
    # F zyx
    return {"x": arr_x, "y": arr_y, "z": arr_z, "f": arr_f}


def interp_xyz(table, type_polin="newton", x0=1.5, y0=1.5, z0=1.5):
    nx = 3
    ny = 3
    nz = 3
    arr_f = np.array(table["f"])
    new = np.zeros(shape=arr_f.shape[1:3])
    # print(table)
    for i, y in enumerate(table["y"]):
        for j, z in enumerate(table["z"]):
            # table["x"], f[x', y, z] ... - matrix
            # y_ind = table["y"].index(y)
            # z_ind = table["z"].index(z)
            # print(arr_f[:, 0, 0], len(arr_f[:, 0, 0]))
            # print(arr_f[0][0][:], len(arr_f[0][0][:]))
            # matrix = np.stack((table["x"], arr_f[:, y_ind, z_ind]), axis=1)
            # matrix = np.stack((table["x"], arr_f[z_ind][y_ind][:]), axis=1)
            # print(table["x"], arr_f)
            matrix = np.stack((table["x"], arr_f[:, y, z]), axis=1)
            if type_polin == "newton" or type_polin == "mix":
                new[i][j] = newton_polynomial(matrix, nx, x0)["res"]
            elif type_polin == "spline":
                new[i, j] = spline_polynomial(matrix, x0)["res"]

    new2 = np.zeros(shape=arr_f.shape[1:2])
    for i, z in enumerate(table["z"]):
        # table["y"], f[y', z] ... - matrix
        # z_ind = table["z"].index(z)
        # matrix = np.stack((table["y"], new[:, z_ind]), axis=1)
        matrix = np.stack((table["y"], new[:, z]), axis=1)
        if type_polin == "newton":
            new2[i] = newton_polynomial(matrix, ny, y0)["res"]
        elif type_polin == "spline" or type_polin == "mix":
            new2[i] = spline_polynomial(matrix, y0)["res"]
    # table["z"], new2[z'] - matrix (new2 - list)
    matrix = np.stack((table["z"], new2), axis=1)
    if type_polin == "newton" or type_polin == "mix":
        res = newton_polynomial(matrix, nz, z0)["res"]
    elif type_polin == "spline":
        res = spline_polynomial(matrix, z0)["res"]
    else:
        res = None

    res = round(res, 3)
    return res


def func(x, y, z):
    # if z == 0:
    #     return 1e7
    # else:
    #     return (x**2 + y**2) / z
    if x + y == 0:
        return 1e7
    else:
        return 1. / (x + y) - z


def generate():
    x_range = [-5, 5, 20]
    y_range = [-3, 4, 50]
    z_range = [-1, 2, 30]
    arr_x = []
    arr_y = []
    arr_z = []
    for i in range(x_range[2]):
        arr_x.append(x_range[0] + i * (x_range[1] - x_range[0]) / x_range[2])
    for i in range(y_range[2]):
        arr_y.append(y_range[0] + i * (y_range[1] - y_range[0]) / y_range[2])
    for i in range(z_range[2]):
        arr_z.append(z_range[0] + i * (z_range[1] - z_range[0]) / z_range[2])
    f = []
    # print(arr_x)
    # print(arr_y)
    # print(arr_z)
    for z in arr_z:
        arr_xyi = []
        for y in arr_y:
            arr_xi = []
            for x in arr_x:
                arr_xi.append(func(x, y, z))
                # print(x, y, z)
            arr_xyi.append(arr_xi)
        f.append(arr_xyi)
    return {"x": arr_x, "y": arr_y, "z": arr_z, "f": f}
