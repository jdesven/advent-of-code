from math import log10
from pyhelper.pyimport import seperator_to_list

def calc(iterations):
    current_line = {num: 1 for num in seperator_to_list('2024/input/day11_input.txt', seperator = ' ', cast = int)}
    for _ in range(iterations):
        next_line = {}
        for num, count in current_line.items():
            if num == 0:
                next_line[1] = count + next_line[1] if 1 in next_line else count
            else:
                num_len = int(log10(num)) + 1
                if num_len % 2 == 0:
                    for next_num in int(num / 10**(num_len / 2)), int(num % 10**(num_len / 2)):
                        next_line[next_num] = count + next_line[next_num] if next_num in next_line else count
                else:
                    next_num = num * 2024
                    next_line[next_num] = count + next_line[next_num] if next_num in next_line else count
        current_line = next_line
    return sum(next_line.values())

print(calc(25))

print(calc(75))