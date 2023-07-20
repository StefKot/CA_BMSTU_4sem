from text import *
from task1 import Task1
from task2 import Task2

task1 = Task1()
task2 = Task2()
just_table = {1: task1.ReadFile, 2: task1.GenerateTable, 3: task1.EditWeights, 4: task1.PrintTable, 5: task1.GetGraph,
              6: task2.ReadFile, 7: task2.GenerateTable, 8: task2.EditWeights, 9: task2.PrintTable, 10: task2.GetGraph}

if __name__ == "__main__":
    while True:
        print(line)
        print(menu)
        n = int(input(n_input))
        params = input(params_input).split()
        just_table[n](params)