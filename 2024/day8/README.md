[Link to puzzle](https://adventofcode.com/2024/day/8)
## Introduction

Finding the efficient solution to a problem involving a grid usually boils down to minimizing the amount of times this grid needs to be iterated over. The solution to this puzzle sees every grid position only once, while making sure that it retains all the neccesary information to calculate the positions of the antinodes.

The solution starts with an import of the input, and converting this text file to a `numpy.ndarray` using `np.loadtxt()`. This two-dimensional array allows for easy use of (x,y) coordinates.

```python
import numpy as np

map = np.array([list(line) for line in np.loadtxt('2024/input/day8_input.txt', dtype = str, comments = None)])
```

## Pre-processing

By making lists of antenna coordinates grouped by antenna frequencies, we can calculate the positions of antinodes formed by all possible combinations of antennas of one frequency. To do so, we first need to create an array `chars` that maps an integer index to every unique antenna frequency. Then, we loop over every position in the grid, and save every antenna coordinate in the array that has the index that corresponds to the antenna frequency. This create a array of arrays `coords_per_char` where every inner array represents to coordinates of one antenna frequency.

Using these combinations, we are able to calculate the positions of all antinodes caused by the antenna positions. Note that we have only looped over the coordinates of the map once.

```python
chars = np.unique(map[map != '.'].flatten())
coords_per_char = []
for i in range(len(chars)):
    coords_per_char.append([])
for y in range(len(map)):
    for x in range(len(map[0])):
        if map[y][x] != '.':
            coords_per_char[np.where(chars == map[y][x])[0][0]].append([x, y])
```

## Puzzle part 1

Using `itertools.combinations`, we are able to find all combinations of two antenna positions of the same frequency. For every combination, we then calculate the [relative position vector](https://en.wikipedia.org/wiki/Position_(geometry)#Relative_position) `pos_diff` of the two antenna coordinates. By subtracting the relative position from one of the antenna positions, we find the position where the distance to one antenna is exactly twice the distance to the second antenna - i.e. an antinode. We add these positions to the list of antinodes `antinodes`, after making sure that the found antinode is within the boundaries of the map. By counting the amount of unique antinode positions in this list, we find the solution to the first puzzle part.

> Note that we transform the list `antinode` to an array _after_ we have calculated all antinode positions. Since we individually append every antinode position to `antinode`, every iteration would otherwise result in a full reallocation of the array.

```python
from itertools import combinations

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
```

An important note to mention here is that there is a hypothetical situation where the above approach would fail. When the antinode is positioned in between the two antennas - for example in the situation `A.#...A` where `A` represent the antennas and `#` represents the antinode - then this antinode would not be picked up on using the relative position vector method. Incidentally, no such situations are present in the puzzle input, so the solution holds true.

## Puzzle part 2

To account for resonant harmonics, we multiply the relative position vector `pos_diff` with any integer `mul` that produces a position that is still within the boundaries of the map. Note that `mul` can also be 0, since a resonant harmonic can also occur on an antenna. We do not have to do this for both antenna positions of the combination, since either calculation using this approach results in the same list of antinode coordinates. Since it is initially unknown how many integer multiplications fit within the boundaries of the map, we use two `while` loops that loop from 0 to negative and positive infinity, respectively, until we find an antinode that lies outside of the boundaries of the map.

This approach breaks down when the coordinates of the relative position vector have a [greatest common divisor](https://en.wikipedia.org/wiki/Greatest_common_divisor) (GCD) larger than 1. For example, when one antenna is located at (0,0) and one antenna at (2,2), we only find the resonant harmonics of (4,4), (6,6), (...), whereas the resonant harmonics of (3,3), (5,5), (...) would also satisfy the given definition. To account for this, we divide the coordinates of the relative position vector (2,2) by their GCD (2), such that we receive the reduced relative position vector `pos_fidd_gcd`, in this example equal to (1,1). However, as it turns out, the puzzle input produces no relative position vectors with GCDs larger than 1, so we would have received the correct answer either way.

```python
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
```