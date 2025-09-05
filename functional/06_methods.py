powers = [1, 4, 9, 16, 25]


print("start list")
for i in range(len(powers)):
    print(powers[i])
print("einde list")

powers.append(36)

print("start list")
for i in range(len(powers)):
    print(powers[i])
print("einde list")



def print_list_1():
    print("start list")
    for i in range(len(powers)):
        print(powers[i])
    print("einde list")

print_list_1()

powers.append(49)

print_list_1()

fibonacci = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

print_list_1()

def print_list_2(input_list):
    print("start list")
    for i in range(len(input_list)):
        print(input_list[i])
    print("einde list")

print_list_2(fibonacci)
print_list_2(powers)
print_list_2(["Homer", "Marge", "Bart", "Lisa"])


def print_list_3(input_list, label):
    print("start lijst: ", label)
    for i in range(len(input_list)):
        print(input_list[i])
    print("einde list")

print_list_3(powers, "machten")