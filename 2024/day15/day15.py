from pyhelper.pyimport import seperator_to_list, grid_to_dict
map_str, instructions_str = seperator_to_list('2024/input/day15_input.txt', '\n\n')
map = grid_to_dict(map_str, relevant_chars = {'.', '@', 'O'}, read_file = False)
instructions = [{'>': 1, '<': -1, '^': -1j, 'v': 1j}[char] for char in instructions_str.replace('\n','')]

pos_robot = [pos for pos, val in map.items() if val == '@'][0]
for dir in instructions:
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
print(sum([100 * int(pos.imag) + int(pos.real) for pos in map if map[pos] == 'O']))