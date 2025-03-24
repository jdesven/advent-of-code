from itertools import combinations
from math import gcd
from pyhelper.pyimport import grid_to_dict
map = grid_to_dict('2024/input/day8_input.txt')

chars = set(val for val in map.values() if val != '.')
coords_per_char = {char: set(pos for pos, val in map.items() if val == char) for char in chars}

antinodes = set()
for char, positions in coords_per_char.items():
    for coord_1, coord_2 in list(combinations(positions, 2)):
        pos_diff = coord_1 - coord_2
        for antinode in (coord_1 + pos_diff, coord_2 - pos_diff):
            if antinode in map.keys():
                antinodes.add(antinode)
print(len(antinodes))

antinodes = set()
for char, positions in coords_per_char.items():
    for coord_1, coord_2 in list(combinations(positions, 2)):
        pos_diff = coord_1 - coord_2
        pos_diff_gcd = pos_diff / gcd(int(pos_diff.real), int(pos_diff.imag))
        for mul_dir in (-1, 1):
            mul = 0
            while coord_1 + pos_diff_gcd * mul in map.keys():
                antinodes.add(coord_1 + pos_diff_gcd * mul)
                mul += mul_dir
print(len(antinodes))