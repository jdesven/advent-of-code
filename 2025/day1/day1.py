input = [50] + open("2025\input\day1_input.txt").read().split('\n')

for i in range(1, len(input)):
    input[i] = input[i - 1] + (int(input[i][1:]) * (1 if input[i][0] == 'R' else -1))

print([num % 100 for num in input].count(0))

print(sum((1 + abs(b - a) // 100) if b % 100 == 0
    else (abs(b - a) // 100) if a % 100 == 0
    else abs(b // 100 - a // 100)
    for a, b in zip(input, input[1:])
))