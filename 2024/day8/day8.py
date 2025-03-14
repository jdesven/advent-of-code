import numpy as np
from itertools import combinations

map = np.array([list(line) for line in np.loadtxt('2024/input/day8_input.txt', dtype = str, comments = None)])

chars = np.unique(map[map != '.'].flatten())
coords_per_char = []
for i in range(len(chars)):
    coords_per_char.append([])
for y in range(len(map)):
    for x in range(len(map[0])):
        if map[y][x] != '.':
            coords_per_char[np.where(chars == map[y][x])[0][0]].append([x, y])

antinodes = []
for char in coords_per_char:
    coords_combinations = list(combinations(char, 2))
    for coords_combination in coords_combinations:
        pos_diff = np.subtract(coords_combination[0], coords_combination[1])
        for antinode in [np.add(coords_combination[0], pos_diff), np.subtract(coords_combination[1], pos_diff)]:
            if 0 <= antinode[0] < len(map[0]) and 0 <= antinode[1] < len(map):
                antinodes.append(antinode)
antinodes = np.unique(np.array(antinodes), axis = 0)
print(len(antinodes))

antinodes = []
for char in coords_per_char:
    coords_combinations = np.array(list(combinations(char, 2)))
    for coords_combination in coords_combinations:
        pos_diff = np.subtract(coords_combination[0], coords_combination[1])
        pos_diff_gcd = np.divide(pos_diff, np.gcd.reduce(pos_diff))
        antinode = coords_combination[0]
        mul = 0
        while 0 <= antinode[0] < len(map[0]) and 0 <= antinode[1] < len(map):
            antinodes.append(antinode)
            mul -= 1
            antinode = np.add(coords_combination[0], np.multiply(pos_diff,mul))
        antinode = coords_combination[0]
        mul = 0
        while 0 <= antinode[0] < len(map[0]) and 0 <= antinode[1] < len(map):
            antinodes.append(antinode)
            mul += 1
            antinode = np.add(coords_combination[0], np.multiply(pos_diff,mul))
antinodes = np.unique(np.array(antinodes), axis = 0)
print(len(antinodes))