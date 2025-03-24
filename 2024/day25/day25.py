from pyhelper.pyimport import seperator_to_list

schematics = seperator_to_list('2024/input/day25_input.txt', '\n\n')

keys = set()
locks = set()
for schematic in schematics:
    heights = []
    for pin in range(5):
        heights.append(len([line for line in schematic.splitlines() if line[pin] == '#']) - 1)
    keys.add(tuple(heights)) if schematic[0] == '.' else locks.add(tuple(heights))

count = 0
for lock in locks:
    for key in keys:
        if all(lock[pin] + key[pin] <= 5 for pin in range(5)):
            count += 1
print(count)