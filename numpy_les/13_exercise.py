import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

#N = input("Enter a number: ")
N = 2
print(N)

O = N * 4

z, y, x = np.ogrid[:O,:O, :O]

print(x//4)
d = (((x//N)%2) +((y//N)%2)+((z//N)%2) ) %2

print(x)
print(y)
print(z)

print(d)

x, y, z = np.indices(d.shape)

# Haal enkel de coördinaten op waar de waarde 1 is
x_points = x[d == 1]
y_points = y[d == 1]
z_points = z[d == 1]

# Creëer een 3D scatter-plot om de punten te visualiseren
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Teken enkel de punten waar waarde 1 is
ax.scatter(x_points, y_points, z_points, c='b', marker='s', label='Value = 1', alpha=0.5)

# Styling van de as
ax.set_xlabel('X-as')
ax.set_ylabel('Y-as')
ax.set_zlabel('Z-as')
ax.set_title('3D Binaire Kubus')

plt.show()


class aaa:
    def __init__(self):
        self.x = 10
        self._x = 5
        self.__y__ = 1

y =aaa()
print(y.x)
print(y._x)
print(y.__y__)
