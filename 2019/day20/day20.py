from pyhelper.pyimport import grid_to_dict
capital_letters = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
grid = grid_to_dict('2019/input/day20_input.txt', set(['.'] + capital_letters))

teleports = {}
for pos, char in grid.items():
    if grid.get(pos) in capital_letters:
        for dir in [1, -1, 1j, -1j]:
            if grid.get(pos - dir) in capital_letters and grid.get(pos + dir) == '.':
                label = (grid[pos - dir] + grid[pos]) if dir in [1, 1j] else (grid[pos] + grid[pos - dir])
                if label == 'AA':
                    starting_pos = pos + dir
                elif label == 'ZZ':
                    ending_pos = pos + dir
                else:
                    teleports[pos + dir] = label
teleport_reverse = {}
for pos, label in teleports.items():
    if label not in teleport_reverse:
        teleport_reverse[label] = set([pos])
    else:
        teleport_reverse[label].add(pos)

positions_seen = set([starting_pos])
positions = [starting_pos]
steps = 0
while ending_pos not in positions_seen:
    positions_next = []
    for pos in positions:
        for dir in (-1j, 1j, -1, 1):
            next_pos = pos + dir
            if grid.get(next_pos) == '.' and next_pos not in positions_seen:
                positions_next.append(next_pos)
                positions_seen.add(next_pos)
        if pos in teleports:
            teleport_destination = [loc for loc in teleport_reverse[teleports[pos]] if loc != pos][0]
            positions_next.append(teleport_destination)
            positions_seen.add(teleport_destination)
    positions = positions_next
    steps += 1
print(steps)


positions_seen = set((0, starting_pos))
positions = [(0, starting_pos)]
steps = 0
map_dim = (max([int(coord.real) for coord in grid.keys()]), max([int(coord.imag) for coord in grid.keys()]))
while (0, ending_pos) not in positions_seen:
    positions_next = []
    for pos in positions:
        for dir in (-1j, 1j, -1, 1):
            next_pos = pos[1] + dir
            if grid.get(next_pos) == '.' and (pos[0], next_pos) not in positions_seen:
                positions_next.append((pos[0], next_pos))
                positions_seen.add((pos[0], next_pos))
        if pos[1] in teleports:
            level_change = -1 if int(pos[1].real) in (2, map_dim[0] - 2) or int(pos[1].imag) in (2, map_dim[1] - 2) else 1
            if not (pos[0] == 0 and level_change == -1):
                teleport_destination = [loc for loc in teleport_reverse[teleports[pos[1]]] if loc != pos[1]][0]
                if (pos[0] + level_change, teleport_destination) not in positions_seen:
                    positions_next.append((pos[0] + level_change, teleport_destination))
                    positions_seen.add((pos[0] + level_change, teleport_destination))
    positions = positions_next
    steps += 1
print(steps)