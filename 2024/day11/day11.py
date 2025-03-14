from math import log10, pow

with open('2024/input/day11_input.txt', 'r') as file:
    current_line = dict([int(num), 1] for num in file.read().split(' '))

for _ in range(75):
    next_line = {}
    for num, count in current_line.items():
        if num == 0:
            next_line[1] = count + next_line[1] if 1 in next_line else count
        else:
            num_len = int(log10(num)) + 1
            if num_len % 2 == 0:
                next_num = int(num / pow(10, num_len / 2)) 
                next_line[next_num] = count + next_line[next_num] if next_num in next_line else count
                next_num = int(num % pow(10, num_len / 2))
                next_line[next_num] = count + next_line[next_num] if next_num in next_line else count
            else:
                next_num = num * 2024
                next_line[next_num] = count + next_line[next_num] if next_num in next_line else count
    current_line = next_line
print(sum(next_line.values()))