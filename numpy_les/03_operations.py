import numpy as np
from numpy_ex import basics

arr = np.arange(10, 20).reshape(2, 5)
basics.print_info(arr)

basics.print_info(2 * arr)
basics.print_info(2 * arr)
basics.print_info(arr * 5)
basics.print_info(arr * 5.0)
basics.print_info(arr / 3 - arr // 3)
basics.print_info(arr ** 3)
basics.print_info(3 ** arr)

basics.print_info(2 + arr)
basics.print_info(arr - 10)
basics.print_info(abs(arr - 100))
basics.print_info(-arr)
basics.print_info(np.square(arr), "kwadraat")
basics.print_info(np.sqrt(arr), "wortel")
basics.print_info(np.cbrt(arr), "3d machts wortel")
basics.print_info(arr ** 0.25, "4d machts wortel")
arr += 1
basics.print_info(arr, " +=")
arr -= 1
basics.print_info(arr, "-=")

print((15 ** 0.1) ** 10)
basics.print_info((arr ** 0.1) ** 10, "4d machts wortel")

##### grenzen van precisie: numpy versus python
factor = 2
count = 20
arr = np.arange(10, 20).reshape(2, 5)
for i in range(count):
    arr = arr ** (1 / factor)

for i in range(count):
    arr = arr ** factor

print(arr)

arr = np.arange(10, 20).reshape(2, 5)
l = arr.tolist()
for i in range(count):
    for y in range(len(l)):
        for x in range(len(l[y])):
            l[y][x] = l[y][x] ** (1 / factor)
for i in range(count):
    for y in range(len(l)):
        for x in range(len(l[y])):
            l[y][x] = l[y][x] ** factor

print(l)
#####


