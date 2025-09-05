def double_list(input_list):
    dl = [value * 2 for value in input_list]
    return dl


l = [1,2,3,4,5]
print(double_list(l))


def split_odd_even(input_list):
    even = [v for v in input_list if v % 2 == 0]
    odd = [v for v in input_list if v % 2 != 0]
    return even, odd

even_values, odd_values = split_odd_even(l)

print(even_values)
print(odd_values)
