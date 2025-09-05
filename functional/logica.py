bits_4 = [ [(i//4)%2, (i//2)%2, i%2] for i in range(16)]
print(bits_4)

for bits in bits_4:
    b1, b2, b3 = bits
    print(f"{bits} => {b1 and b2 or b3=}")