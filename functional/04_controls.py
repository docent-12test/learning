
i = 1
while i <= 10:
    print(i)
    i += 1


i = 1
while i <= 10:
    if i % 2 == 0:
        print(i)
    i += 1



while True:
    i = int(input("Geef een getal tussen 1 en 10: "))
    if i < 1 or i > 10:
        print("Het getal moet tussen 1 en 10 bevatten")
        continue
    print(f"Het getal is {i}")
    break

for i in range(10):
    print(i)
    