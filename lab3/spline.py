# Получение коэффициентов
import copy


def get_a(tl: list):
    arr_a = [0] * (len(tl) - 1)
    for i in range(len(tl) - 1):
        point = tl[i]
        arr_a[i] = point[1]

    return arr_a


def get_c(tl: list, c0=0):
    # Отсутствие изгибов в начале
    arr_c = [0] * (len(tl) - 1)
    ce = [0, 0]
    cn = [0, c0]
    h = [0, 0]

    for i in range(2, len(tl)):
        for j in range(2):
            h[j] = tl[i - j][0] - tl[i - j - 1][0]
        F = 3 * ((tl[i][1] - tl[i - 1][1]) / h[0] - (tl[i - 1][1] - tl[i - 2][1]) / h[1])
        ce.append(-h[0] / (h[1] * ce[i - 1] + 2 * sum(h)))
        cn.append((F - h[1] * cn[i - 1]) / (h[1] * ce[i - 1] + 2 * sum(h)))

    arr_c[-1] = cn[-1]
    for i in reversed(range(1, len(tl) - 1)):
        arr_c[i - 1] = ce[i] * arr_c[i] + cn[i]

    return arr_c


def get_b(tl: list, arr_c, cn=0):
    arr_b = [0] * len(tl)
    arr_c.append(cn)
    for i in range(1, len(tl)):
        h = (tl[i][0] - tl[i - 1][0])
        arr_b[i - 1] = (tl[i][1] - tl[i - 1][1]) / h - h / 3 * (arr_c[i] + 2 * arr_c[i - 1])
    h = (tl[-1][0] - tl[-2][0])
    arr_b[-1] = (tl[-1][1] - tl[-2][1]) / h - h / 3 * 2 * arr_c[-1]

    return arr_b


def get_d(tl: list, arr_c, cn=0):
    dN = 1
    arr_d = [0] * len(tl)
    arr_c.append(cn)
    for i in range(1, len(tl)):
        h = (tl[i][0] - tl[i - 1][0])
        arr_d[i - 1] = (arr_c[i] - arr_c[i - 1]) / (3 * h) * dN
    h = (tl[-1][0] - tl[-2][0])
    arr_d[-1] = -arr_c[-1] / (3 * h) * dN

    return arr_d


def get_index(tl: list, x: float):
    ind = 0
    while ind < len(tl) and tl[ind][0] < x:
        ind += 1
    if ind < len(tl) and tl[ind][0] > x:
        ind -= 1
    # Если нет подходящей внутренней точки
    if ind >= len(tl):
        ind = -1
    return ind


# Кубическая интерполяция
def spline_polynomial(tl, x, c0=0, cn=0):
    arr_a = get_a(tl)
    arr_c = get_c(tl, c0)
    arr_c2 = copy.deepcopy(arr_c)
    arr_b = get_b(tl, arr_c2, cn)
    arr_d = get_d(tl, arr_c2, cn)
    ind = get_index(tl, x)

    # print("a", arr_a)
    # print(arr_b)
    # print(arr_c)
    # print("d", arr_d)


    dx = x - tl[ind][0]
    # print(f"{arr_a[ind]} + {arr_b[ind]}*{dx} + {arr_c[ind]}*{dx}**2 + {arr_d[ind]} * {dx} ** 3 ")
    y = arr_a[ind] + arr_b[ind] * dx + arr_c[ind] * (dx ** 2) + arr_d[ind] * (dx ** 3)

    return {"res": y}
