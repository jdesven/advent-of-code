from pyhelper.pyimport import grid_to_dict
map = grid_to_dict('2024/input/day10_input.txt', cast = int)

score = 0
for pos_start in [pos_start for pos_start, val_start in map.items() if val_start == 0j]:
    positions = {pos_start}
    for i in range(1, 10):
        positions_next = set()
        for pos in positions:
            for dir in (-1, 1, -1j, 1j):
                if map.get(pos + dir) == i:
                    positions_next.add(pos + dir)
        positions = positions_next
    score += len(positions)
print(score)

score = 0
for pos_start in [pos_start for pos_start, val_start in map.items() if val_start == 0j]:
    positions = [pos_start]
    for i in range(1, 10):
        positions_next = []
        for pos in positions:
            for dir in (-1, 1, -1j, 1j):
                if map.get(pos + dir) == i:
                    positions_next.append(pos + dir)
        positions = positions_next
    score += len(positions)
print(score)