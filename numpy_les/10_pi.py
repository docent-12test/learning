import numpy as np
from matplotlib import pyplot as plt

N = 20000
N2 = N//2


# Maak een raster van coördinaten
y, x = np.ogrid[:N+1, :N+1]

# Bereken de afstand van elk punt tot het middelpunt
distance_squared = (x - N//2) ** 2 + (y - N//2) ** 2
arr = distance_squared <= N2 ** 2


print("testing")
SAMPLES = 1000000
samples = np.random.randint(0, N,(SAMPLES,3) )

SKIP = SAMPLES // 100
res = np.zeros((SAMPLES-SKIP))

hits, total = 0, 0
for sample in samples:
    total+=1
    if arr[sample[0],sample[1]]:
        hits+=1

    if total > SKIP:
        res[total-1-SKIP] = hits/total * 4
print(hits)
print(total)
print(hits/total * 4)


x = np.arange(SAMPLES-SKIP)
# 500 punten gelijkmatig verdeeld tussen 0 en 10
# Plot de gegevens
plt.plot(x, res, label='pi benadering')
y=np.full(SAMPLES-SKIP, np.pi)
plt.plot(x, y )
plt.show()



