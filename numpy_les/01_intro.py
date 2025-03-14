
import numpy as np
from numpy_ex import basics

arr = np.array([2, 4, -11, 5, 20, 42, 13])
basics.print_info(arr)

arr = np.array([2, 4, -11, 5, 20, 42, 13])
basics.print_info(arr)

arr = np.array([[2, 4, -11, 5, 20, 42, 13], [3, 4, 5, 5, 2, 4, 1]])
basics.print_info(arr)

print(type(arr.mean()))
basics.dump(arr)