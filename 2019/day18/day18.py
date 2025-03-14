from pyhelper.pyimport import grid_to_dict
lowercase_letters = [chr(char) for char in range(ord('a'), ord('a') + 26)]
uppercase_letters = [chr(char) for char in range(ord('A'), ord('A') + 26)]
map = grid_to_dict('2019/input/day18_input.txt', ['.', '@'] + lowercase_letters + uppercase_letters)

key_to_key = {}
for pos, key in [(pos, key) for pos, key in map.items() if key in lowercase_letters + ['@']]:
    pos_seen = set([pos])
    paths = [[pos]]
    distance = 1
    key_to_key[key] = {}
    while len(paths) > 0:
        paths_next = []
        for path in paths:
            pos = path[0]
            for dir in (-1, 1, -1j, 1j):
                if pos + dir in map and pos + dir not in pos_seen:
                    paths_next.append([pos + dir] + path[1:]) if len(path) > 1 else paths_next.append([pos + dir])
                    pos_seen.add(pos + dir)
                    if map[pos + dir] in uppercase_letters:
                        paths_next[-1].append(map[pos + dir])
                    if map[pos + dir] in lowercase_letters:
                        paths_next[-1].append(map[pos + dir])
                        key_to_key[key][map[pos+dir]] = ([distance] + path[1:]) if len(path) > 1 else [distance]
        distance += 1
        paths = paths_next

paths = [['@', 0, set('@')]]
lengths = []
while len(paths) > 0:
    paths_next = []
    for pos, distance, seen in paths:
        for destination, keys_needed in key_to_key[pos].items():
            if destination not in seen and all([key.lower() in seen for key in keys_needed[1:]]):
                paths_next.append([destination, distance + keys_needed[0], seen.union(set([destination]))])
            pass
    for _, distance, seen in paths_next:
        if len(seen) == len(key_to_key):
            lengths.append(distance)
    paths = []
    for pos, distance, seen in paths_next:
        if distance == min([c_distance for c_pos, c_distance, c_seen in paths_next if (c_pos, c_seen) == (pos, seen)]):
            paths.append([pos, distance, seen])
print(min(lengths))

middle = int(max([pos.real for pos in map.keys()]) / 2) + 1 + int(max([pos.imag for pos in map.keys()]) / 2) * 1j + 1j
for x in (-1, 0, 1):
    for y in (-1j, 0, 1j):
        pos = middle + x + y
        match (x, y):
            case (-1, -1j):
                map[pos] = '@1'
            case (1, -1j):
                map[pos] = '@2'
            case (-1, 1j):
                map[pos] = '@3'
            case (1, 1j):
                map[pos] = '@4'
            case _:
                map.pop(pos, None)

key_to_key = {}
for pos, key in [(pos, key) for pos, key in map.items() if key in lowercase_letters + ['@1', '@2', '@3', '@4']]:
    pos_seen = set([pos])
    paths = [[pos]]
    distance = 1
    key_to_key[key] = {}
    while len(paths) > 0:
        paths_next = []
        for path in paths:
            pos = path[0]
            for dir in (-1, 1, -1j, 1j):
                if pos + dir in map and pos + dir not in pos_seen:
                    paths_next.append([pos + dir] + path[1:]) if len(path) > 1 else paths_next.append([pos + dir])
                    pos_seen.add(pos + dir)
                    if map[pos + dir] in uppercase_letters:
                        paths_next[-1].append(map[pos + dir])
                    if map[pos + dir] in lowercase_letters:
                        paths_next[-1].append(map[pos + dir])
                        key_to_key[key][map[pos+dir]] = ([distance] + path[1:]) if len(path) > 1 else [distance]
        distance += 1
        paths = paths_next

paths = [[['@1', '@2', '@3', '@4'], 0, set(['@1', '@2', '@3', '@4'])]]
lengths = []
while len(paths) > 0:
    paths_next = []
    for pos_list, distance, seen in paths:
        for i_pos, pos in enumerate(pos_list):
            for destination, keys_needed in key_to_key[pos].items():
                if destination not in seen and all([key.lower() in seen for key in keys_needed[1:]]):
                    pos_list_next = [destination if i_pos == i_c_pos else c_pos for i_c_pos, c_pos in enumerate(pos_list)]
                    paths_next.append([pos_list_next, distance + keys_needed[0], seen.union(set([destination]))])
    for _, distance, seen in paths_next:
        if len(seen) == len(key_to_key):
            lengths.append(distance)
    paths = []
    for path in paths_next:
        if path not in paths:
            paths.append(path)
print(min(lengths))