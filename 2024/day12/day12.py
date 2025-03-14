import numpy as np
 
rows = [line for line in np.loadtxt('2024/input/day12_input.txt', dtype = str)]
map = {}
for i_row, row in enumerate(rows):
    for i_char in range(len(row)):
        map[i_char + i_row * 1j] = rows[i_row][i_char]

# part 1
price = 0
map_seen = set()
for pos_start, letter in map.items():
    if pos_start not in map_seen:
        perimeter = 0
        pos_region = [pos_start]
        map_seen.add(pos_start)
        for pos in pos_region:
            for dir in [1, -1, 1j, -1j]:
                if map.get(pos + dir) != letter:
                    perimeter += 1
                elif pos + dir not in map_seen:
                    pos_region.append(pos + dir)
                    map_seen.add(pos + dir)
        price += len(pos_region) * perimeter
print('ans1: ' + str(price))

# part 2
price = 0
map_seen = set()
for pos_start, letter in map.items():
    if pos_start not in map_seen:
        pos_region = [pos_start]
        map_seen.add(pos_start)
        for pos in pos_region:
            for dir in [1, -1, 1j, -1j]:
                if map.get(pos + dir) == letter and pos + dir not in map_seen:
                    pos_region.append(pos + dir)
                    map_seen.add(pos + dir)
        corners = 0
        for pos in pos_region:
            for x in [-1, 1]:
                for y in [-1j, 1j]:
                    if (map.get(pos + x) != letter and map.get(pos + y) != letter) or (map.get(pos + x) == letter and map.get(pos + y) == letter and map.get(pos + x + y) != letter):
                        corners += 1
        price += len(pos_region) * corners
print('ans2: ' + str(price))