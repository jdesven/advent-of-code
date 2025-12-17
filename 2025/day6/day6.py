from math import prod
input = [[num if num in ('*', '+') else int(num) for num in line.split(' ') if num != ''] for line in open("2025\input\day6_input.txt").read().split('\n')]

s = 0
for col in [[input[i][j] for i in range(len(input[0]))] for j in range(len(input))]:
    s += prod(col[0:-1]) if col[-1] == '*' else sum(col[0:-1])
print(s)