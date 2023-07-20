import math
from scipy.special import erfi
import numpy as np
import matplotlib.pyplot as plt

def func(x):
    return (math.exp(-x**2/2) * ((1 + math.exp(x**2/2) * x) * erfi(1/math.sqrt(2)) - (1 + math.sqrt(math.e)) * erfi(x/math.sqrt(2))))/erfi(1/math.sqrt(2))

def polynom(x, a, b, c):
    return 1 - x + a * (x - x**2) + b * (x**2 - x**3) + c * (x**3 - x**4)

x = np.linspace(-1, 1, 100)

a = -3*x**2+2*x-2
b = -4*x**3 + 3*x**2 - 6*x + 2 
c = -5*x**4+4*x**3-12*x**2+6*x
f = 4*x - 1

r1 = -6*x+2
r2 = -12*x**2 + 6*x - 6
r3 = -20*x**3+12*x**2-24*x+6

system = np.array([
    [
        np.sum(a*r1),
        np.sum(b*r1),
        np.sum(c*r1),
    ],
    [
        np.sum(a*r2),
        np.sum(b*r2),
        np.sum(c*r2),
    ],
    [
        np.sum(a*r3),
        np.sum(b*r3),
        np.sum(c*r3),
    ]
])

result = np.array([
    np.sum(f*r1),
    np.sum(f*r2),
    np.sum(f*r3)
])


kfs = np.linalg.solve(system, result)

y = np.vectorize(func)(x)
y2 = np.vectorize(polynom)(x, kfs[0], kfs[1], kfs[2])

plt.plot(x, y)
plt.plot(x, y2)
plt.show()

print(kfs)