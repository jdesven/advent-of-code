with open('2024/input/day25_input.txt', 'r') as file:
    schematics = file.read().split('\n\n')

keys = set()
locks = set()
for schematic in schematics:
    heights = []
    for pin in range(5):
        heights.append(len([line for line in schematic.splitlines() if line[pin] == '#']) - 1)
    if schematic[0] == '.':
        keys.add(tuple(heights))
    else:
        locks.add(tuple(heights))

count = 0
# part 1
for lock in locks:
    for key in keys:
        fits = True
        for pin in range(5):
            if lock[pin] + key[pin] > 5:
                fits = False
        if fits == True:
            count += 1
print(count)