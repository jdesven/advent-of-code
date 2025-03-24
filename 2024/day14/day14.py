from math import prod
from pyhelper.pyimport import lines_to_list, seperator_to_list

rows = lines_to_list('2024/input/day14_input.txt', regex = '[-0-9, ]')
input = [seperator_to_list(row.replace(' ', ','), seperator = ',', cast = int, read_file = False) for row in rows]

def calc(time):
    sum_quadrant = [0, 0, 0, 0]
    for pos_x, pos_y, dir_x, dir_y in input:
        pos = [(pos_x + time * dir_x) % 101, (pos_y + time * dir_y) % 103]
        if pos[0] != 50 and pos[1] != 51:
            sum_quadrant[(1 if pos[0] > 50 else 0) + (2 if pos[1] > 51 else 0)] += 1
    return prod(sum_quadrant)

print(calc(100))

calcs = [0] * 10000
for i in range(10000):
    calcs[i] = calc(i)
print(calcs.index(min(calcs)))