array = [2, 8, 9, 48, 8, 22, -12, 2]
complete_array = [val + 2 for val in array if val > 5]
set_array = set(complete_array)
print(array)
print(set_array)
