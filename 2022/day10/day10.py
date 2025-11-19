from pyhelper.pyimport import lines_to_list
instructions = [line if line == 'noop' else int(line[line.index(' ') + 1:]) for line in lines_to_list("2022\input\day10_input.txt")]

x = 1
cycle = 1
signal_strengths = []
for instruction in instructions:
    for _ in range(1 if instruction == 'noop' else 2):
        if cycle % 40 == 20:
            signal_strengths.append(x * cycle)
        cycle += 1
    if instruction != 'noop':
        x += instruction
print(sum(signal_strengths))

x = 1
cycle = 0
image = [['-']*40 for _ in range(6)]
for instruction in instructions:
    for _ in range(1 if instruction == 'noop' else 2):
        image[int(cycle / 40)][cycle % 40] = '██' if abs(cycle % 40 - x) <= 1 else '░░'
        cycle += 1
    if instruction != 'noop':
        x += instruction
for row in image:
    print(''.join(row))