"""
NumPy (kort voor "Numerical Python") is een populaire open-source bibliotheek in Python, ontworpen om efficiënte
berekeningen te doen met grote datasets. Het is vooral nuttig voor wetenschappelijk rekenen, data-analyse en
machine learning.

- NumPy werkt vaak samen met andere bibliotheken zoals:
- **Pandas** (voor tabular data)
- **Matplotlib** (voor visualisatie)
- **Scikit-learn** (voor machine learning)

Het is een essentieel hulpmiddel in de meeste data-analysetools in Python.

Je kunt NumPy installeren via pip:
pip install numpy

Waarom NumPy gebruiken?
- Snelheid: NumPy berekent wiskundige operaties veel sneller dan de ingebouwde Python datastructuren
            dankzij optimalisaties op basis van C en Fortran.
- Geoptimaliseerd voor Datawetenschap: Veel bibliotheken en frameworks bouwen voort op NumPy, waardoor het een
                                       essentiële tool is voor iedereen die met data of wetenschap werkt.
- Gebruiksvriendelijk: NumPy biedt krachtige tools die eenvoudig zijn te begrijpen en te gebruiken.


Belangrijkste Kenmerken van NumPy
1. N-Dimensionale Arrays (`ndarray`)
    - De kern van NumPy is de `ndarray`, een efficiënte datastructuur die je toelaat om arrays met meerdere dimensies
        te maken en te manipuleren.
    - Arrays in NumPy zijn veel sneller en efficiënter dan traditionele Python-lijsten omdat ze continu in het geheugen
      worden opgeslagen en geoptimaliseerd zijn voor wiskundige bewerkingen.

2. Snelle Wiskundige Operaties
    - NumPy ondersteunt wiskundige operaties zoals optellen, aftrekken, matrixvermenigvuldiging, en lineaire algebra.
    - Bij arrays kan NumPy 'elementgewijze operaties' uitvoeren (bijv. twee arrays optellen) zonder trage Python-loops
    - Biedt ingebouwde functies zoals `sum`, `mean`, `std`, etc.

3. Broadcasting
    - NumPy kan wiskundige operaties uitvoeren op arrays van verschillende vormen en groottes door broadcasting,
      wat betekent dat kleinere arrays automatisch worden uitgebreid om de bewerking soepel mogelijk te maken.

4 Geavanceerde Functionaliteiten**
    - **Indexeren en Slicen**: Je kunt subarrays selecteren en manipuleren.

"""

import numpy as np
from numpy_ex import basics

# basis concept is een n-dimensionele-array
#  1D: [ 1,2,3]
#      dimensie 1: 3
#      => rij (list)
# basis constructie
arr = np.array([1, 2, 3])
print(arr)
print(arr.ndim)
print(arr.shape)

#  2D: [ [10, 20, 30, 40], [ 100,1000, 10_000, 100_000]]
#      dimensie 1: 4
#      dimensie 2: 2
#      => tabel 4 * 2 : (list of list)

arr = np.array([[10, 20, 30, 40], [100, 1000, 10_000, 100_000]])
print(arr)
print(arr.ndim)
print(arr.shape)

#  3D: [ [ [1, 2, 3, 4], [2, 3, 4, 5] ],  [ [1, 2, 3, 4], [2, 3, 4, 5] ], [ [1, 2, 3, 4], [2, 3, 4, 5] ] ]
#      dimensie 1: 4
#      dimensie 2: 2
#      dimensie 3: 3
#      => blok: 3 * 2 * 4  (list of list of list)

arr = np.array([[[1, 2, 3, 4], [2, 3, 4, 5]], [[1, 2, 3, 4], [2, 3, 4, 5]], [[1, 2, 3, 4], [2, 3, 4, 5]]])
print(arr)
print(arr.ndim)
print(arr.shape)

# Dimensies moeten overal correct zijn: arrays are homogeneous
try:
    arr = np.array([[[1, 2, 3], [2, 3, 4, 5]], [[1, 2, 3, 4], [2, 3, 4, 5]], [[1, 2, 3, 4], [2, 3, 4, 5]]])
except Exception as e:
    print(e)

# Vaste grootte: de vorm of grootte aanpassen creëert een nieuwe array.
# Belangrijk voor geheugenbeheer bij grote arrays

arr = np.array([[1, 2, 3],
                [4, 5, 6]])
print(arr)
print(f"arr id: {id(arr)}")
new_row = np.array([7, 8, 9])
print(f"new_row id : {id(new_row)}")
arr = np.vstack([arr, new_row])
print(f"arr id: {id(arr)}")

# Alle elementen hebben hetzelfde datatype
#    Gehele getallen: int8, int16, int32, int64
#    Positieve getallen: uint8, uint16, uint32, uint64
#    Floats: float16, float32, float64, float128
#    Complex: complex64, complex128
#    Boolean: bool_
#
arr = np.array([[1, 2, 3],
                [4, 5, 6]])
print(arr)
print(arr.dtype)

arr = np.array([[1, 2, 3],
                [4, 5, 6.0]])
print(arr)
print(arr.dtype)

arr = np.array([[1, 2, 3],
                [4, 5, '6']])
print(arr)
print(arr.dtype)

# Wees zuinig
arr = np.array([[1, 2, 3],
                [4, 5, 6]])
basics.print_info(arr)

arr = np.array([[1, 2, 3],
                [4, 5, 6]], dtype=np.int8)
basics.print_info(arr)

arr = np.array([[1, 2, 3],
                [4, 5, 6]], dtype=np.bool_)
basics.print_info(arr)

# basis functies:
arr = np.array([[1, 2, 3],
                [4, 5, 6]])
print(f"value: {arr}")
print(f"shape : {arr.shape}")
print(f"dtype : {arr.dtype}")
print(f"ndim : {arr.ndim}")
print(f"size : {arr.size}")
print(f"itemsize : {arr.itemsize}")
print(f"nbytes : {arr.nbytes}")
print(f"data : {arr.data}")
print(f"sum() : {arr.sum()}")
print(f"max() : {arr.max()}")
print(f"min() : {arr.min()}")
print(f"mean() : {arr.mean()}")
print(f"std() : {arr.std()}")
print(f"any() : {arr.any()}")
print(f"all() : {arr.all()}")
print(f"flatten : {arr.flatten()}")
print(f"argmax() : {arr.argmax()}")
print(f"argmin() : {arr.argmin()}")
