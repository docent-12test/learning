from datetime import datetime

import numpy as np
from numpy_ex import basics
from numpy_ex.basics import print_info

"""
arr = numpy.array(object, dtype=None, copy=True, order='K', subok=False, ndmin=0, like=None)

object: Invoerobject dat naar een array wordt geconverteerd   (Verplicht)
 dtype: Specificeer het datatype van de array (None => automatisch)
  copy: Kopie maken of niet (in plaats van originele data aanpassen) (True) 
 order: | opslagvolgorde: 'C', 'F', 'A' of 'K'  ('K')
 ndmin: | Minimaal aantal dimensies (0)
 subok: | Subklassen behouden? (False)
  like: | Aanpassen volgens ander array-achtig object | `None` |
"""

### dtype
arr = np.array([[1, 2, 3], [4, 5, 6]])
basics.print_info(arr)

arr = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int8)
basics.print_info(arr)

### copy  (obsolete)
### order (expert level)  zie later
### ndmin
arr = np.array([[1, 2, 3], [4, 5, 6]])
basics.print_info(arr)

arr = np.array([[1, 2, 3], [4, 5, 6]], ndmin=3)
basics.print_info(arr)

### subok
# Matrix is subclass van ndarray met o.a. overload van __mult__()
mat = np.matrix([[1, 2], [3, 4]])
arr = np.array(mat, subok=False)
print(type(arr))
arr = np.array(mat, subok=True)
print(type(arr))

### create met standaard vorm / waarden
arr = np.zeros((3, 4))
basics.print_info(arr, "zeros")

arr = np.ones(3)
basics.print_info(arr, "ones")

arr = np.ones((3, 1), dtype=np.bool)
basics.print_info(arr, "ones 2D")

arr = np.full((3, 4), 7)
basics.print_info(arr, "full 2D waarde 7")

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

arr = np.linspace(1., 4., 6)
basics.print_info(arr, "linspace")

arr = np.arange(0, 10, 0.25).reshape(10, 4)
basics.print_info(arr)

arr = np.random.randint(1, 42, (10, 6))
basics.print_info(arr)

arr = np.random.random((10, 6))
basics.print_info(arr)

arr = np.eye(3)
basics.print_info(arr)

arr = np.eye(3, 5)
basics.print_info(arr)

arr = np.diag([1, 2, 3])
basics.print_info(arr)

arr = np.array([[1, 2], [3, 4]])
arr = np.diag(arr)

# alloceer array zonder initialisation
arr = np.empty((3, 4), dtype=np.int8)
basics.print_info(arr)

#
# size = 10000
# count = 10
# print(datetime.now())
# for i in range(count):
#     arr = np.random.random((size,size) )
# print(datetime.now())
# for i in range(count):
#     arr = [[random.random() for _ in range(size)] for _ in range(size)]
# print(datetime.now())

size = 10_000
count = 100
value = 5.1
print(datetime.now())
for i in range(count):
    arr = np.full((size, size), value)
print(arr)
print(datetime.now())
for i in range(count):
    # arr = [[5 for _ in range(size)] for _ in range(size)]
    arr = [[5.1] * size for _ in range(size)]

# print(arr)
print(datetime.now())
