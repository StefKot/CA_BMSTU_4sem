from numpy import linspace
from prettytable import PrettyTable
from tools import Point

epsilon = 1e-6


def read_table(file_name):
    data_table = []
    file = open(file_name)

    for line in file.readlines():
        row = list(map(float, line.split(" ")))
        data_table.append(Point(row[0], row[1]))

    file.close()
    return data_table


def print_table(point_table):
    header = ["|{:^15s}|{:^15s}|{:^15s}|".format("№", "X", "Y")]
    separator = "+{:-^15s}+{:-^15s}+{:-^15s}+".format("", "", "")
    rows = []
    for i, point in enumerate(point_table):
        row = "|{:^15d}|{:^15.3f}|{:^15.3f}|".format(i+1, point.x, point.y)
        rows.append(row)

    print(separator)
    print("\n".join(header + [separator] + rows))
    print(separator)


def print_subtable(subtable):
    table = PrettyTable()

    column_names = ["X"] + ["Y'{}".format(i - 1) for i in range(2, len(subtable))]
    table.field_names = column_names

    for row in subtable:
        table_row = ["{:.4f}".format(row[0])]
        table_row += ["{:.4f}".format(val) if val != float('inf') else 'inf' for val in row[1:]]
        table.add_row(table_row)

    print(table)


def f(x):
    return x**3
