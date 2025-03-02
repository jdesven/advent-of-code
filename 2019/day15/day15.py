from pyhelper.pyimport import seperator_to_list_to_dict
from importlib import import_module
program = seperator_to_list_to_dict('2019/input/day15_input.txt', seperator = ',', cast = int)
intcode = getattr(import_module('2019.intcode.intcode'), 'intcode')

def find_path(pos, map):
    paths = [[pos]]
    while True:
        next_paths = []
        for path in paths:
            for dir in (-1j, 1j, -1, 1):
                if path[-1] + dir not in map.keys():
                    return path + [path[-1] + dir]
                elif map[path[-1] + dir] == '.' and path[-1] + dir not in path:
                    next_paths.append(path + [path[-1] + dir])
        paths = next_paths
        if len(paths) == 0:
            return []
                
map = {0j: '.'}
pos = 0j
droid = intcode(program.copy(), [])
while True:
    path = find_path(pos, map)
    if path == []:
        break
    dirs = [path[i + 1] - path[i] for i in range(0, len(path) - 1)]
    droid.inputs.extend([{-1j: 1, 1j: 2, -1: 3, 1: 4}[dir] for dir in dirs])
    status = None
    while status == None:
        out, status = droid.calc_step()
        if out != None:
            last_out = out
    match last_out:
        case 0:
            pos = path[-2]
            map[path[-1]] = '#'
        case 1:
            pos = path[-1]
            map[pos] = '.'
        case 2:
            pos = path[-1]
            map[pos] = '.'
            pos_oxygen = path[-1]
     
paths = [pos_oxygen]
positions_seen = set([pos_oxygen])
path_len = 0
while 0j not in positions_seen:
    next_paths = []
    for path in paths:
        for dir in (-1j, 1j, -1, 1):
            if map.get(path + dir) == '.' and path + dir not in positions_seen:
                next_paths.append(path + dir)
                positions_seen.add(path + dir)
    paths = next_paths
    path_len += 1
print(path_len)

minutes = 0
pos_filled = set([pos_oxygen])
pos_to_check = set([pos_oxygen])
while len(pos_to_check) > 0:
    pos_to_check_next = set()
    for pos in pos_to_check:
        for dir in (-1j, 1j, -1, 1):
            if map.get(pos + dir) == '.' and pos + dir not in pos_filled:
                pos_to_check_next.add(pos + dir)
    pos_to_check = pos_to_check_next
    pos_filled.update(pos_to_check)
    if len(pos_to_check) > 0:
        minutes += 1
print(minutes)