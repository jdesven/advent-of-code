from pyhelper.pyimport import grid_to_complex_set
map_input = grid_to_complex_set('2019/input/day24_input.txt', '#')

map = map_input.copy()
maps_seen = set([frozenset(map)])
while True:
    map_next = set()
    for y in range(5):
        for x in range(5):
            pos = x + y * 1j
            neighbors = 0
            for dir in (-1, 1, -1j, 1j):
                if pos + dir in map:
                    neighbors += 1
            if neighbors == 1 or (pos not in map and neighbors == 2):
                map_next.add(pos)
    map = frozenset(map_next)
    if map in maps_seen:
        break
    else:
        maps_seen.add(map)
print(sum([pow(2,(int(pos.real) + int(pos.imag) * 5)) for pos in map]))

minutes = 200
map_list = [set()] * minutes
if 2 + 2j in map:
    map.remove(2 + 2j)
map_list[0] = map_input
for minute in range(minutes):
    map_list_next = [set() for _ in range(minutes + 1)]
    for depth in range (-1 * int(minutes / 2), int(minutes / 2) + 1):
        for y in range(5):
            for x in range(5):
                if not (x == y == 2):
                    pos = x + y * 1j
                    neighbors = 0
                    for dir in (-1, 1, -1j, 1j):
                        if pos + dir in map_list[depth]:
                            neighbors += 1
                    if x == 0 and 1 + 2j in map_list[depth -1]:
                        neighbors += 1
                    if x == 4 and 3 + 2j in map_list[depth -1]:
                        neighbors += 1
                    if y == 0 and 2 + 1j in map_list[depth -1]:
                        neighbors += 1
                    if y == 4 and 2 + 3j in map_list[depth -1]:
                        neighbors += 1
                    if pos == 2 + 1j:
                        neighbors += len([pos for pos in map_list[depth + 1] if int(pos.imag) == 0])    
                    if pos == 2 + 3j:
                        neighbors += len([pos for pos in map_list[depth + 1] if int(pos.imag) == 4])    
                    if pos == 1 + 2j:
                        neighbors += len([pos for pos in map_list[depth + 1] if int(pos.real) == 0])    
                    if pos == 3 + 2j:
                        neighbors += len([pos for pos in map_list[depth + 1] if int(pos.real) == 4])                       
                    if neighbors == 1 or (pos not in map_list[depth] and neighbors == 2):
                        map_list_next[depth].add(pos)
    map_list = map_list_next
print(sum([len(depth) for depth in map_list]))