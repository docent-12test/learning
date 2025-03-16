

import numpy as np

from lib.ansi import red, green, blue


def times(a, b, dot:bool=False):
    green()
    print(a)
    blue()
    print(b)
    red()
    if dot:
        print(np.dot(a,b))
    else:
        print(a*b)
    print()


times(np.array([5]), np.array([2]))
times(np.array([5,2]), np.array([2]))
times(np.array([5,2]), np.array([2,3]))
times(np.array([5,2]), np.array([[2],[3]]))

times(np.random.random((4,3,2)), np.array([2]))
times(np.random.random((4,3,2)), np.arange(2))
