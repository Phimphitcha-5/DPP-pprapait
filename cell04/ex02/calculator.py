num1 = int(input('Give me the first number:'))
num2 = int(input('Give me the second number:'))
print('Thank you!')

def calc():
    add = num1 + num2
    print(f'{num1} + {num2} = {add}')
    minus = num1 - num2
    print(f'{num1} - {num2} = {minus}')
    mul = num1 * num2
    print(f'{num1} x {num2} = {mul}')
    div = num1/num2
    print(f'{num1} / {num2} = {div}')

calc()
