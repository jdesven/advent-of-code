with open('2024/input/day15_input.txt', 'r') as file:
    map_str, instructions_str = file.read().split('\n\n')
map = {}
for i_line, line in enumerate(map_str.split('\n')):
    for i_char, char in enumerate([char for char in line if char != '#']):
        if char != '#':
            map[i_line * 1j + i_char] = char
            if char =='@':
                pos_robot = i_line * 1j + i_char
instructions = [{'>': 1, '<': -1, '^': -1j, 'v': 1j}[char] for char in instructions_str.replace('\n','')]

# part 1
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
print('ans1: ' + str(sum([100 * int(pos.imag) + int(pos.real) for pos in map if map[pos] == 'O'])))