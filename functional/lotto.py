"""
Opgave:
    De lotto is een kansspel met COUNT ballen met een waarde tussen 1 en RANGE.
    De kans dat jouw 6 kruisjes overeenkomen met de wekelijkse trekking is:
        CHANCE = RANGE! / (COUNT! * (RANGE-COUNT)!)
        Met x! = x * (x-1) * (x-2) * ... * 3 * 2 * 1

    Schrijf een programma dat
       1/ een lotto formulier invult: 6 verschillende getallen tussen 1 en RANGE.
       2/ opeenvolgende trekkingen genereert tot een trekking overeenkomt met de cijfers op het formulier.
       3/ afdrukt hoeveel pogingen nodig zijn om de trekking te winnen.
       4/ beoordeelt of dat aantal pogingen beter is dan de geschatte kans.

    Hints:
        math.factorial(x): x!
        random.sample(range(1, RANGE), COUNT): COUNT verschillende willekeurige getallen tussen 1 en RANGE:
"""

import random
from math import factorial as fac

RANGE = 45
COUNT = 6
CHANCE = fac(RANGE) // (fac(COUNT) * fac(RANGE - COUNT))

WINNERS = sorted(random.sample(range(1, RANGE + 1), COUNT))

print(f"Deze lotto trekt {COUNT} ballen met waardes tussen 1 en {RANGE}")
print(f"Je hebt 1 kans op {CHANCE:,} om te winnen")

i = 0
while True:
    i += 1
    ATTEMPT = sorted(random.sample(range(1, RANGE + 1), COUNT))
    if ATTEMPT == WINNERS:
        break
print(f"Gewonnen na {i:,} pogingen!")
print(f"Beter dan verwacht: {i < CHANCE}")
