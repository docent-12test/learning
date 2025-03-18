from lib.ansi import red, green, blue, yellow, print_red
from lib.psystem import print_dict
import numpy as np

freq = {
"Do C": 261.63 ,
"Re D": 293.66 ,
"Mi E": 329.63 ,
"Fa F": 349.23 ,
"Sol G": 392.0 ,
"La A": 440.0 ,
"Si B": 493.88
}

print_dict(freq, "frequencies")


red()
o4 = [(4, key, value) for key, value in freq.items()]
print(o4)

green()
octave4 = np.array(o4)
# tuples worden lists, alles wordt string
print(octave4)

yellow()
octave4 = np.array(o4, dtype=[('octave', 'i2'), ('key', 'S6'), ('freq', 'f4')])
print(octave4)

blue()
print(octave4['freq'])


res = octave4.copy()
for i in range(1,5):
    print(i)
    lower = octave4.copy()
    higher = octave4.copy()
    lower['freq'] /= 2**i
    lower['octave'] -= i

    higher['freq'] *= 2**i
    higher['octave'] += i
    res = np.vstack((lower, res, higher))
    print(res )
print("FINAL")
print(res)
print(res.shape)

res = res.flatten()

for record in res:
    print(record)


