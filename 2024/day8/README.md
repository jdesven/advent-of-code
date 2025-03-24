[Link to puzzle](https://adventofcode.com/2024/day/8)
## Introduction

Finding the efficient solution to a problem involving a grid usually boils down to minimizing the amount of times this grid needs to be iterated over. The solution to this puzzle sees every grid position only once, while making sure that it retains all the neccesary information to calculate the positions of the antinodes.

The solution starts with an import of the input into a dictionary of complex coordinates. More information on the use of complex coordinates can be found [here](https://github.com/jdesven/advent-of-code/blob/main/documentation/complex2dplane.md).

```python
from pyhelper.pyimport import grid_to_dict
map = grid_to_dict('2024/input/day8_input.txt')
```

## Pre-processing

By making lists of antenna coordinates grouped by antenna frequencies, we can calculate the positions of antinodes formed by all possible combinations of antennas of one frequency. To do so, we first need to create an dictionary `coords_per_char` that maps a character to all positions in which this character resides. Using these combinations, we are able to calculate the positions of all antinodes caused by the antenna positions. Note that we have only looped over the coordinates of the map once.

```python
chars = set(val for val in map.values() if val != '.')
coords_per_char = {char: set(pos for pos, val in map.items() if val == char) for char in chars}
```

## Puzzle part 1

Using `itertools.combinations`, we are able to find all combinations of two antenna positions of the same frequency. For every combination, we then calculate the [relative position vector](https://en.wikipedia.org/wiki/Position_(geometry)#Relative_position) `pos_diff` of the two antenna coordinates. By subtracting the relative position from one of the antenna positions, we find the position where the distance to one antenna is exactly twice the distance to the second antenna - i.e. an antinode. We add these positions to the set of antinodes `antinodes`, after making sure that the found antinode is within the boundaries of the map. By counting the amount of antinode positions in this list, we find the solution to the first puzzle part.

```python
from itertools import combinations

antinodes = set()
for char, positions in coords_per_char.items():
    for coord_1, coord_2 in list(combinations(positions, 2)):
        pos_diff = coord_1 - coord_2
        for antinode in (coord_1 + pos_diff, coord_2 - pos_diff):
            if antinode in map.keys():
                antinodes.add(antinode)
print(len(antinodes))
```

An important note to mention here is that there is a hypothetical situation where the above approach would fail. When the antinode is positioned in between the two antennas - for example in the situation `A.#...A` where `A` represent the antennas and `#` represents the antinode - then this antinode would not be picked up on using the relative position vector method. Incidentally, no such situations are present in the puzzle input, so the solution holds true.

## Puzzle part 2

To account for resonant harmonics, we multiply the relative position vector `pos_diff` with some integer `mul` that produces a position that is still within the boundaries of the map. Note that `mul` can also be 0, since a resonant harmonic can also occur on an antenna. We do not have to do this for both antenna positions of the combination, since either calculation using this approach results in the same list of antinode coordinates. Since it is initially unknown how many integer multiplications fit within the boundaries of the map, we use two `while` loops that loop from 0 to negative and positive infinity, respectively, until we find an antinode that lies outside of the boundaries of the map.

This approach breaks down when the coordinates of the relative position vector have a [greatest common divisor](https://en.wikipedia.org/wiki/Greatest_common_divisor) (GCD) larger than 1. For example, when one antenna is located at (0,0) and one antenna at (2,2), we only find the resonant harmonics of (4,4), (6,6), (...), whereas the resonant harmonics of (3,3), (5,5), (...) would also satisfy the given definition. To account for this, we divide the coordinates of the relative position vector (2,2) by their GCD (2), such that we receive the reduced relative position vector `pos_diff_gcd`, in this example equal to (1,1). However, as it turns out, the puzzle input produces no relative position vectors with GCDs larger than 1, so we would have received the correct answer either way.

```python
from math import gcd

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
```