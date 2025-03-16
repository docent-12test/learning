import time

import numpy as np

### order parameter in array

N = 10000

arr_c = np.array(np.random.rand(N, N), order='C')
arr_f = np.array(np.random.rand(N, N), order='F')

# Rijen lezen (row-major is sneller voor C-orde)
start = time.time()
for row in arr_c:
    row.sum()
print("Itereren over rijen (C-order):", time.time() - start)

start = time.time()
for row in arr_f:
    row.sum()
print("Itereren over rijen (F-order):", time.time() - start)

# Kolommen lezen (column-major is sneller voor F-orde)
start = time.time()
for col in arr_c.T:  # Transponeren voor kolomwerking
    col.sum()
print("Itereren over kolommen (C-order):", time.time() - start)

start = time.time()
for col in arr_f.T:  # Transponeren voor kolomwerking
    col.sum()
print("Itereren over kolommen (F-order):", time.time() - start)
exit()
arr = np.zeros((3, 4))
basics.print_info(arr)

