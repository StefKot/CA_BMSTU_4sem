import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

class Task2:
    def __init__(self):
        self.table = {"x": 0, "y": 0, "z": 0, "w": 0}

    def ReadFile(self, params):
        file = params[0]

        with open(file, 'r') as f:
            lines = f.readlines()

        x = np.array([])
        y = np.array([])
        z = np.array([])
        w = np.array([])

        for line in lines:
            values = line.split()
            x = np.append(x, float(values[0]))
            y = np.append(y, float(values[1]))
            z = np.append(w, float(values[2]))
            w = np.append(w, float(values[3]))

        self.table = {"x": x, "y": y, "z": z, "w": w}

    def GenerateTable(self, params):
        n = int(params[0])
        m = int(params[1])

        x_arr = np.linspace(-10, 10, n)
        y_arr = np.linspace(-10, 10, m)

        delta = np.random.normal(scale=0.1, size=(n, m))

        Y, X = np.meshgrid(y_arr, x_arr)
        Z = 2*X**2 + np.exp(Y) - 1
        W = np.ones((n,m))

        x = X.ravel()
        y = Y.ravel()
        z = Z.ravel()
        w = W.ravel()
        
        self.table = {"x": x, "y": y, "z": z, "w": w}

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
        system = np.array([
            [
                np.sum(self.table["w"]*(self.table["x"])**4),
                np.sum(self.table["w"]*(self.table["x"])**3),
                np.sum(self.table["w"]*(self.table["x"])**2),
                np.sum(self.table["w"]*(self.table["y"])**2*(self.table["x"]**2)),
                np.sum(self.table["w"]*(self.table["y"])*(self.table["x"]**2)),
                np.sum(self.table["w"]*self.table["x"]**3*self.table["y"]),
            ],
            [
                np.sum(self.table["w"]*(self.table["x"])**3),
                np.sum(self.table["w"]*(self.table["x"])**2),
                np.sum(self.table["w"]*(self.table["x"])**1),
                np.sum(self.table["w"]*(self.table["y"])**2*(self.table["x"]**1)),
                np.sum(self.table["w"]*(self.table["y"])*(self.table["x"]**1)),
                np.sum(self.table["w"]*self.table["x"]**2*self.table["y"]),
            ],
            [
                np.sum(self.table["w"]*(self.table["x"])**2),
                np.sum(self.table["w"]*(self.table["x"])**1),
                np.sum(self.table["w"]),
                np.sum(self.table["w"]*(self.table["y"])**2),
                np.sum(self.table["w"]*(self.table["y"])),
                np.sum(self.table["w"]*self.table["x"]*self.table["y"]),
            ],
            [
                np.sum(self.table["w"]*(self.table["x"])**2*(self.table["y"])**2),
                np.sum(self.table["w"]*(self.table["x"])**1*(self.table["y"])**2),
                np.sum(self.table["w"]*(self.table["y"])**2),
                np.sum(self.table["w"]*(self.table["y"])**4),
                np.sum(self.table["w"]*(self.table["y"])**3),
                np.sum(self.table["w"]*self.table["x"]*self.table["y"]**3),
            ],
            [
                np.sum(self.table["w"]*(self.table["x"])**2*(self.table["y"])),
                np.sum(self.table["w"]*(self.table["x"])**1*(self.table["y"])),
                np.sum(self.table["w"]*(self.table["y"])**1),
                np.sum(self.table["w"]*(self.table["y"])**3),
                np.sum(self.table["w"]*(self.table["y"])**2),
                np.sum(self.table["w"]*self.table["x"]*self.table["y"]**2),
            ],
            [
                np.sum(self.table["w"]*(self.table["x"])**3*self.table["y"]),
                np.sum(self.table["w"]*(self.table["x"])**2*self.table["y"]),
                np.sum(self.table["w"]*(self.table["x"])**1*self.table["y"]),
                np.sum(self.table["w"]*(self.table["y"])**3*(self.table["x"]**1)),
                np.sum(self.table["w"]*(self.table["y"])**2*(self.table["x"]**1)),
                np.sum(self.table["w"]*self.table["x"]**2*self.table["y"]**2),
            ]
        ])

        result = np.array([
            np.sum(self.table["w"]*self.table["z"]*self.table["x"]**2),
            np.sum(self.table["w"]*self.table["z"]*self.table["x"]**1),
            np.sum(self.table["w"]*self.table["z"]),
            np.sum(self.table["w"]*self.table["z"]*self.table["y"]**2),
            np.sum(self.table["w"]*self.table["z"]*self.table["y"]**1),
            np.sum(self.table["w"]*self.table["z"]*self.table["y"]*self.table["x"]),
        ])


        kfs = np.linalg.solve(system, result)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # A = np.vstack([self.table["x"], self.table["y"], np.ones(len(self.table["x"]))]).T
        # coefficients, _, _, _ = np.linalg.lstsq(A, self.table["z"], rcond=None)
        # print(coefficients)
        # print(kfs)

        ax.scatter(self.table["x"], self.table["y"], self.table["z"])
        x_grid, y_grid = np.meshgrid(np.linspace(self.table["x"].min(), self.table["x"].max(), 100), np.linspace(self.table["y"].min(), self.table["y"].max(), 100))
        z_grid = kfs[0] * x_grid**2 + kfs[1] * x_grid + kfs[2] + kfs[3] * y_grid**2 + kfs[4] * y_grid + kfs[5]*x_grid*y_grid
        ax.plot_surface(x_grid, y_grid, z_grid, cmap='viridis')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()