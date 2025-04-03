"""
Schrijf een programma dat
    - de gebruiker laat raden naar een willekeurig getal tussen 1 en N
    - als het getal < 1 of > N is dan krijgt de gebruiker een melding
    - zolang het niet geraden is, geeft de computer een hint (hoge of lager)
    - als het getal geraden is dan wint de gebruiker
    - print het aantal pogingen

"""
from random import randint

N = 10
SECRET = randint(1, N)
print(f"Het getal is {SECRET}")

attempt = 0
while True:
    attempt += 1
    number = int(input(f"Geef een getal tussen 1 en {N}: "))
    if number == SECRET:
        break
    if number < 1 or number > N:
        print("Het getal moet tussen 1 en", N, "bevatten")
        continue
    if number > SECRET:
        print("Het getal is lager")
    elif number < SECRET:
        print("Het getal is hoger")

print(f"Aantal pogingen {attempt:,}")
