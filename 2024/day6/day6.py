from pyhelper.pyimport import grid_to_dict
map = grid_to_dict('2024/input/day6_input.txt', {'.', '#', '^'})

pos = [pos for pos, val in map.items() if val == '^'][0]
seen_pos = {pos}
dir = -1j
while pos + dir in map:
    match map[pos + dir]:
        case '#':
            dir = dir * 1j
        case '.' | '^':
            pos = pos + dir
            seen_pos.add(pos)
print(len(seen_pos))

count = 0
pos_init = [pos for pos, val in map.items() if val == '^'][0]
for pos in [pos for pos in map.keys() if pos in seen_pos]:
    pos_dir = (pos_init, -1j)
    map_modified = {**map, pos: '#'}
    escaped_or_looping = False
    seen_pos_dir = set()
    while pos_dir[0] + pos_dir[1] in map_modified and pos_dir not in seen_pos_dir:
        seen_pos_dir.add(pos_dir)
        if map_modified[pos_dir[0] + pos_dir[1]] == '#':
            pos_dir = (pos_dir[0], pos_dir[1] * 1j)
        else:
            pos_dir = (pos_dir[0] + pos_dir[1], pos_dir[1])
    if pos_dir in seen_pos_dir:
        count += 1
print(count)