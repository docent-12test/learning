import numpy as np
from numpy_ex import basics

arr = np.array([2, 4, -11, 5, 20, 42, 13])
basics.print_info(arr)

arr = np.array([[2, 4, -11, 5, 20, 42, 13], [3, 4, 5, 5, 2, 4, 1]])
basics.print_info(arr)

arr = np.array([[[29, 97],
                 [43, 15],
                 [86, 53],
                 [55, 50]],

                [[18, 23],
                 [38, 99],
                 [27, 59],
                 [40, 87]],

                [[0, 75],
                 [98, 22],
                 [12, 65],
                 [53, 70]]])
basics.print_info(arr)

arr = np.array([[[29, 97],
                 [43, 15],
                 [86, 53],
                 [55, 50]],

                [[18, 23],
                 [38, 99],
                 [27, 59],
                 [40, 87]],

                [[0, 75],
                 [98, 22],
                 [12, 65],
                 [53, 70]]], dtype=np.int8)
basics.print_info(arr)