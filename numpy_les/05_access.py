import numpy as np

arr = np.arange(10)
print(arr[1])
print(arr[2:5])
print(arr[2:8:3])
print(arr[-1:-8:-2])
print(arr[[1, 4]] )
print(arr[[1, -3, 3, -1]] )


arr = np.arange(24).reshape(4,6) *3
print(arr)

print(arr[1,])
print(arr[1,3])

print(arr[:,3])
print(arr[3,:])
print(arr[3,:] % 2  == 1)


arr = np.arange(24).reshape(4,6) *3
arr = np.apply_along_axis(np.mean, axis= 1,arr= arr)
print(arr)
arr = np.arange(24).reshape(4,6) *3
arr = np.apply_along_axis(np.mean, axis= 0,arr= arr)
print(arr)


arr = np.arange(24).reshape(4,6) *3

arr = np.apply_over_axes(np.sum, arr, [0])
print(arr)

arr = np.arange(24).reshape(4,6) *3
arr = np.apply_over_axes(np.sum, arr, [1])
print(arr)