"""

Левая часть СЛАУ:
[Σ(Pi*Xi^2)   Σ(Pi*Xi*Yi)  Σ(Pi*Xi)  Σ(Pi*Xi*Zi)]
[Σ(Pi*Xi*Yi)  Σ(Pi*Yi^2)   Σ(Pi*Yi)  Σ(Pi*Yi*Zi)]
[Σ(Pi*Xi)     Σ(Pi*Yi)     Σ(Pi)    Σ(Pi*Zi)]
[Σ(Pi*Xi*Zi)  Σ(Pi*Yi*Zi)  Σ(Pi*Zi)  Σ(Pi)]

Правая часть СЛАУ:
[-Σ(Pi*Xi*(Zi^2))]
[-Σ(Pi*Yi*(Zi^2))]
[-Σ(Pi*(Zi^2))]
[-Σ(Pi*(Zi))

"""

        # system = np.array([
        #     [
        #         np.sum(self.table["w"]*self.table["x"]**2),
        #         np.sum(self.table["w"]*self.table["x"]*self.table["y"]),
        #         np.sum(self.table["w"]*self.table["x"]),
        #         np.sum(self.table["w"]*self.table["x"]*self.table["z"])
        #     ],
        #     [
        #         np.sum(self.table["w"]*self.table["x"]*self.table["y"]),
        #         np.sum(self.table["w"]*self.table["y"]**2),
        #         np.sum(self.table["w"]*self.table["y"]),
        #         np.sum(self.table["w"]*self.table["y"]*self.table["z"])
        #     ],
        #     [
        #         np.sum(self.table["w"]*self.table["x"]),
        #         np.sum(self.table["w"]*self.table["y"]),
        #         np.sum(self.table["w"]),
        #         np.sum(self.table["w"]*self.table["z"])
        #     ],
        #     [
        #         np.sum(self.table["w"]*self.table["x"]*self.table["z"]),
        #         np.sum(self.table["w"]*self.table["y"]*self.table["z"]),
        #         np.sum(self.table["w"]*self.table["z"]),
        #         np.sum(self.table["w"])
        #     ]
        # ])

        # result = np.array([
        #     np.sum(self.table["w"]*self.table["x"]*self.table["z"]**2),
        #     np.sum(self.table["w"]*self.table["y"]*self.table["z"]**2),
        #     np.sum(self.table["w"]*self.table["z"]**2),
        #     np.sum(self.table["w"]*self.table["z"])
        # ])


import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# данные для построения полинома
x = np.array([1,2,3,4,5])
y = np.array([2,3,5,6,8])
z = np.array([1,2,3,4,5])

# определение коэффициентов полинома
A = np.vstack([x, y, np.ones(len(x))]).T
coefficients, _, _, _ = np.linalg.lstsq(A, z, rcond=None)
print(coefficients)

# создание модели 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# построение поверхности полинома
x_grid, y_grid = np.meshgrid(np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100))
z_grid = coefficients[0] * x_grid + coefficients[1] * y_grid + coefficients[2]
ax.plot_surface(x_grid, y_grid, z_grid, cmap='viridis')

# добавление меток на графике
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
