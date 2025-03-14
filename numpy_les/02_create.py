import numpy as np
from numpy_ex import basics


arr = np.zeros((3, 4))
basics.print_info(arr)

arr = np.ones(3)
basics.print_info(arr)

arr = np.ones((3,1), dtype=np.bool)
basics.print_info(arr)

arr = np.arange(10)
basics.print_info(arr)

arr = np.arange(10, dtype=np.float32)
basics.print_info(arr)

arr = np.arange(4, 10)
basics.print_info(arr)

arr = np.arange(4, 30, 3)
basics.print_info(arr)

arr = np.arange(0, 2, 0.25)
basics.print_info(arr)

arr = np.arange(0, 10, 0.25).reshape(10,4)
basics.print_info(arr)

arr = np.random.randint(1,42, (10,6) )
basics.print_info(arr)

arr = np.random.random((10,6) )
basics.print_info(arr)



