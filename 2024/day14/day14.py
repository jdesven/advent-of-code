import re
from math import prod

with open('2024/input/day14_input.txt', 'r') as file:
    txt = file.read().splitlines()
input = [[int(num) for num in row] for row in [row.split(',')[1:5] for row in [re.sub(r'=',',',re.sub(r'[^-0-9=,]','',line)) for line in txt]]]

# part 1
sum_quadrant = [0, 0, 0, 0]
for i in range(len(input)):
    pos = [(input[i][0] + 100 * input[i][2]) % 101, (input[i][1] + 100 * input[i][3]) % 103]
    if pos[0] < 50 and pos[1] < 51:
        sum_quadrant[0] += 1
    elif pos[0] > 50 and pos[1] < 51:
        sum_quadrant[1] += 1
    elif pos[0] < 50 and pos[1] > 51:
        sum_quadrant[2] += 1
    elif pos[0] > 50 and pos[1] > 51:
        sum_quadrant[3] += 1
print('ans1: ' + str(prod(sum_quadrant)))