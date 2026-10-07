num_1 = int(input('Enter the first number: '))
print(num_1)
num_2 = int(input('Enter the second number: '))
print(num_2)
result = num_1 * num_2
print(f'{num_1} x {num_2} = {result}')
if result < 0:
    print('This number is negative')
elif result > 0:
    print('This number is positive')
elif result == 0:
    print('This number is both positive and negative')
