from pyhelper.pyimport import grid_to_complex_set
map = grid_to_complex_set('2019/input/day24_input.txt', '#')

hashes_seen = set([hash(frozenset(map))])
while True:
    map_next = set()
    for y in range(5):
        for x in range(5):
            pos = x + y * 1j
            neighbors = 0
            for dir in (-1, 1, -1j, 1j):
                if pos + dir in map:
                    neighbors += 1
            if (pos in map and neighbors == 1) or (pos not in map and neighbors in (1, 2)):
                map_next.add(pos)
    map = map_next
    if hash(frozenset(map)) in hashes_seen:
        break
    else:
        hashes_seen.add(hash(frozenset(map)))
print(sum([pow(2,(int(pos.real) + int(pos.imag) * 5)) for pos in map]))