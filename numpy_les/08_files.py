
import numpy as np

a = np.random.random((1000,1000))
b = np.ones((1000,1000))
np.save("d:\\temp\\a.npy", a)
np.savez("d:\\temp\\a_b", a, b)
np.savez_compressed("d:\\temp\\a_b_zipped.npz", a, b)
res = np.load("d:\\temp\\a_b_zipped.npz")
print(res.files)
print(res["arr_0"])
print(res["arr_1"])


np.savez_compressed("d:\\temp\\a_b_zipped.npz", xx=a, yy=b)
res = np.load("d:\\temp\\a_b_zipped.npz")
print(res)

