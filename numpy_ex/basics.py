"""
Basic functionalities of numpy
"""
import ctypes

import numpy as np


def print_info(array: np.array):
    """
    Prints detailed information about the given numpy array, such as its shape,
    data type, number of dimensions, size, memory usage, transposed array, various
    aggregated and statistical values, as well as sorting and searching operations.

    This function is intended for debugging or display purposes, providing an
    extensive overview of the properties and operations performed on the input array.

    :param arr: A numpy array subject to inspection.
    :type arr: np.array
    """
    print(f"value: {array}")
    print(f"shape : {array.shape}")
    print(f"dtype : {array.dtype}")
    print(f"ndim : {array.ndim}")
    print(f"size : {array.size}")
    print(f"itemsize : {array.itemsize}")
    print(f"nbytes : {array.nbytes}")
    print(f"data : {array.data}")
    print(f"sum() : {array.sum()}")
    print(f"max() : {array.max()}")
    print(f"min() : {array.min()}")
    print(f"mean() : {array.mean()}")
    print(f"std() : {array.std()}")
    print(f"any() : {array.any()}")
    print(f"all() : {array.all()}")
    print(f"flatten : {array.flatten()}")
    print(f"argmax() : {array.argmax()}")
    print(f"argmin() : {array.argmin()}")
    print(f"T : {array.T}")


def dump(array: np.array):
    buffer = np.array([byte for byte in array.data.tobytes()])
    print(buffer.reshape(array.nbytes//array.itemsize, array.itemsize, ))


def change(array:np.array):
    print(f"sort() : {array.sort()}")
    print(f"value: {array}")
    print(f" : {array.sort(axis=0)}")
    print(f" : {array.sort(axis=1)}")
    print(f" : {array.sort(axis=None)}")
    print(f" : {array.argsort()}")
    print(f" : {array.argsort(axis=0)}")
    print(f" : {array.argsort(axis=1)}")
    print(f" : {array.argsort(axis=None)}")
    print(f" : {array.searchsorted(1)}")
    print(f" : {array.searchsorted([1, 2])}")
    print(f" : {array.searchsorted([1, 2], side='right')}")
    print(f" : {array.searchsorted([1, 2], side='left')}")
    print(f" : {array.searchsorted([1, 2], sorter=None)}")
    print(f" : {array.searchsorted([1, 2], sorter=np.array([1, 0]))}")
    print(f" : {array.searchsorted([1, 2], sorter=np.array([1, 0]), side='right')}")
    print(f" : {array.searchsorted([1, 2], sorter=np.array([1, 0]), side='left')}")


if __name__ == "__main__":
    raise NotImplementedError(__file__)
