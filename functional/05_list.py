lijst = ['Homer', 'Bart', 'Lisa', 'Marge', 'Maggie']

print("Er zijn ",len(lijst), " namen in de lijst.")

for naam in lijst:
    print(naam)

lijst += ["Barny", 'Apu']

for naam in lijst:
    print(naam)
zoek = "Apu"
# zoek = input("Geef een naam in om te zoeken: ")

if zoek in lijst:
    print(zoek, " zit in de lijst.")
else:
    print(zoek, " zit niet in de lijst.")


print("Het eerste element :", lijst[0])
print("Het laatste element :", lijst[-1])
print("Alle andere elementen :", lijst[1:-1])
print("Alles behalve de eerste 2 :", lijst[2:])
print("Alles behalve de laatste 2 :", lijst[:-2])

print(sorted(lijst))
print(lijst)
lijst.sort()
print(lijst)

# comprehension

lijst2 = []
for naam in lijst:
    to_upper = naam.upper()
    lijst2.append(to_upper)

lijst3 = [naam.upper() for naam in lijst]


# Python
lijst.remove("Apu")      # verwijdert eerste voorkomens van waarde
print(lijst)
verwijderd = lijst.pop() # verwijdert en retourneert laatste
print(lijst)
tweede_weg= lijst.pop(1)

lijst.remove("Homer")
print(lijst)
lijst *= 2
print(lijst * 2)

lijst.remove("Lisa")
lijst.count("Apu")









