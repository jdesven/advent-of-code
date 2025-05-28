from pyhelper.pyimport import seperator_to_list, grid_to_dict
map_str, instructions_str = seperator_to_list('2024/input/day15_input.txt', '\n\n')
map = grid_to_dict(map_str, relevant_chars = {'.', '@', 'O'}, read_file = False)
instructions = [{'>': 1, '<': -1, '^': -1j, 'v': 1j}[char] for char in instructions_str.replace('\n','')]

def slide(map, pos_robot, dir):
    next_pos = pos_robot + dir
    affected_pos = [pos_robot]
    while next_pos in map:
        affected_pos.append(next_pos)
        if map[next_pos] == '.':
            for pos in affected_pos[-1:0:-1]:
                map[pos] = map[pos - dir]
            map[affected_pos[0]] = '.'
            pos_robot = pos_robot + dir
            break
        else:
            next_pos += dir
    return map, pos_robot

pos_robot = [pos for pos, val in map.items() if val == '@'][0]
for dir in instructions:
    map, pos_robot = slide(map, pos_robot, dir)
print(sum(100 * int(pos.imag) + int(pos.real) for pos in map if map[pos] == 'O'))

map = grid_to_dict(map_str.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.'), relevant_chars = {'.', '@', '[', ']'}, read_file = False)
pos_robot = [pos for pos, val in map.items() if val == '@'][0]
for dir in instructions:
    if dir in (-1, 1):
        map, pos_robot = slide(map, pos_robot, dir)
    else:
        can_move = True
        affected_pos = []
        row_pos = set([pos_robot])
        while len(row_pos) > 0:
            next_row_pos = set()
            for pos in row_pos:
                if pos + dir not in map:
                    can_move = False
                    next_row_pos = []
                    break
                elif map[pos + dir] != '.':
                    next_row_pos.add(pos + dir)
                    if map[pos + dir] == '[':
                        next_row_pos.add(pos + dir + 1)
                    if map[pos + dir] == ']':
                        next_row_pos.add(pos + dir - 1)
            affected_pos.extend(list(row_pos))
            row_pos = next_row_pos
        if can_move:
            for pos in affected_pos[-1:0:-1]:
                map[pos + dir] = map[pos]
                map[pos] = '.'
            pos_robot = pos_robot + dir
print(sum(100 * int(pos.imag) + int(pos.real) for pos in map if map[pos] == '['))