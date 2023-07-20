import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Task1:
    def __init__(self):
        self.table = {"x": 0, "y": 0, "w": 0}

    def ReadFile(self, params):
        file = params[0]

        with open(file, 'r') as f:
            lines = f.readlines()

        x = np.array([])
        y = np.array([])
        w = np.array([])

        for line in lines:
            values = line.split()
            x = np.append(x, float(values[0]))
            y = np.append(y, float(values[1]))
            w = np.append(w, float(values[2]))

        self.table = {"x": x, "y": y, "w": w}

    def GenerateTable(self, params):
        n = int(params[0])

        delta = np.random.normal(scale=0.1, size=n)

        x = np.linspace(-20, 20, n)
        y = np.cos(x/3) + delta
        w = 1/np.abs(delta)

        self.table = {"x": x, "y": y, "w": w}

    def EditWeights(self, params):
        for i in range(len(self.table["w"])):
            old_w = self.table["w"][i]
            print(f"Изменить w={old_w:.3f} на ", end="")
            new_w = input()
            if new_w == "":
                new_w = old_w
            else:
                new_w = float(new_w)
            self.table["w"][i] = new_w

    def PrintTable(self, params):
        df = pd.DataFrame(self.table)
        print(df)

    def GetGraph(self, params):
        n = int(params[0])

        system = np.zeros((n,n))
        xs = list(reversed([np.sum(self.table["x"]**k * self.table["w"]) for k in range((n-1)*2+1)]))
        for i in range(len(system)):
            for j in range(len(system)):
                system[i, j] = xs[i+j]

        xys = list(reversed([np.sum(self.table["y"]*self.table["x"]**k * self.table["w"]) for k in range(n)]))
        result = np.zeros(n)
        for i in range(len(result)):
            result[i] = xys[i]

        kfs = np.linalg.solve(system, result)

        x2 = np.linspace(self.table["x"][0], self.table["x"][-1], 300)
        y2 = np.zeros(len(x2))
        for i, kf in enumerate(list(reversed(kfs))):
            y2 += kf * x2**i

        plt.scatter(self.table["x"], self.table["y"])
        plt.plot(x2, y2)
        plt.show()