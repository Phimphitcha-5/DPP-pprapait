num_round = int(input('Enter a number less than 25: '))
if num_round > 25:
    print('Error')
elif num_round <= 25:
    for time in range(num_round,26):
        print(f'Inside the loop, my variable is {time}')
