def find_interval(table, n, xo):
    x = [table[i][0] for i in range(len(table))]
    if xo < x[0]:
        return 0, n
    elif xo > x[-1]:
        return len(table) - 1 - n, len(table) - 1
    else:
        i = 0
        while x[i] < xo:
            i += 1
        start = i - n // 2 - 1
        end = i + n // 2 + (n % 2) - 1
        if end > len(x) - 1:
            start -= end - len(x) + 1
            end = len(x) - 1
        elif start < 0:
            end += -start
            start = 0
        return start, end
            

def diff_newton(x, y, n):
    res_table = []
    res_table.append(y)

    for i in range(n):
        curr_col = res_table[i]
        new_col = []
        for j in range(len(curr_col) - 1):
            new_elem = round((curr_col[j + 1] - curr_col[j]) / (x[j + i + 1] - x[j]), 5)
            new_col.append(new_elem)
        res_table.append(new_col)
    return res_table

def get_value(x, diff, xo):
    res = 0
    for i in range(len(diff)):
        term = diff[i][0]
        for j in range(i):
            term *= (xo - x[j])
        res += term
    return res

def newton_method(table, xo, n):
    start, end = find_interval(table, n, xo)
    x = [table[i][0] for i in range(start, end + 1)]
    y = [table[i][1] for i in range(start, end + 1)]
    res_table = diff_newton(x, y, n)
    #print(res_table)
    return get_value(x, res_table, xo)

def diff_hermite(x, y, y1, n):
    res_table = []
    res_table.append(y)
    for i in range(n):
        curr_col = res_table[i]
        new_col = []
        for j in range(len(curr_col) - 1):
            if (x[j] == x[j + i + 1]):
                new_elem = y1[j // 2]
            else:
                new_elem = round((curr_col[j + 1] - curr_col[j]) / (x[j + i + 1] - x[j]), 5)
            new_col.append(new_elem)
        res_table.append(new_col)
    return res_table

def hermit_method(table, xo, n):
    start, end = find_interval(table, n // 2, xo)
    table = table[start : end + 1]
    x = []
    y = []
    y1 = []
    for i in range (len(table)):
        for j in range(2):
            x.append(table[i][0])
            y.append(table[i][1])
        y1.append(table[i][2])
    if n / 2 == 1:
        x.pop()
        y.pop()
    res_table = diff_hermite(x, y, y1, n)
    # print("hermit_method tab", res_table)
    return get_value(x, res_table, xo)