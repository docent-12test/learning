import numpy as np
from numpy_ex import basics


arr = np.arange(20, 10, -1)
print(arr)
np.random.shuffle(arr)
print(arr)

arr = np.arange(20, 10, -1)
print(arr)
print(np.random.permutation(arr))


arr.sort()
print(arr)
arr = np.arange(-5, 19).reshape(4, 6)
basics.print_info(np.sin(arr), "sin")
basics.print_info(np.cos(arr), "cos")
basics.print_info(np.cosh(arr), "cosh")




