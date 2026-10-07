num = 0
while num <= 10:
    print(f'Table {num}:',end=' ')
    mult = 0
    while mult <= 10:
        print(num * mult,end=' ')
        mult += 1
    print()
    num += 1
