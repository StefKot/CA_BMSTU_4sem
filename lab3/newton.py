import copy

EPS = 1e-6


def search_index(table, x, n):
    index = 0

    for i in table:
        if i[0] > x:
            break
        index += 1

    if index >= len(table) - n:
        return len(table) - n - 1

    l_border = index
    r_border = index

    while n > 0:
        if r_border - index == index - l_border:
            if l_border > 0:
                l_border -= 1
            else:
                r_border += 1
        else:
            if r_border < len(table) - 1:
                r_border += 1
            else:
                l_border -= 1
        n -= 1

    return l_border


def divided_difference(x0, y0, x1, y1):
    if abs(x0 - x1) > 1e-10:
        return (y0 - y1) / (x0 - x1)


def newton_polynomial(tl, n, x):
    table = copy.deepcopy(tl)
    index = search_index(table, x, n)
    np = table[index][1]
    kt = []
    kt_i2 = []

    for i in range(n):
        kt_i = []
        for j in range(n - i):
            table[index + j][1] = divided_difference(
                table[index + j][0], table[index + j][1],
                table[index + j + i + 1][0], table[index + j + 1][1])
            kt_i.append(table[index + j][1])
        kt.append(kt_i)

        mult = 1
        for j in range(i + 1):
            mult *= (x - table[index + j][0])

        mult *= table[index][1]
        kt_i2.append(table[index][1])
        np += mult
    kt.insert(0, kt_i2)

    return {"res": np, "kt": kt}
