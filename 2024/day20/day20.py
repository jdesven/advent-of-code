with open('2024/input/day20_input.txt', 'r') as file:
    map = set()
    for i_line, line in enumerate(file.read().splitlines()):
        for i_char, char in enumerate(line):
            match char:
                case '.':
                    map.add(i_char + i_line * 1j)
                case 'S':
                    start_point = i_char + i_line * 1j
                case 'E':
                    end_point = i_char + i_line * 1j

def count_cheats(cheat_length):
    count = 0
    for pos_start in correct_path:
        for x in range(-cheat_length, cheat_length + 1):
            for y in range(-cheat_length, cheat_length + 1):
                pos_end = pos_start + x + y*1j
                if pos_end in correct_path:
                    dist = abs(x) + abs(y)
                    if dist <= cheat_length and correct_path[pos_end] - correct_path[pos_start] - dist >= 100:
                        count += 1
    return count

paths = [[start_point]]
while len(paths) > 0:
    next_paths = []
    for path in paths:
        for dir in [-1, 1, -1j, 1j]:
            next_step = path[-1] + dir
            if next_step == end_point:
                correct_path = {}
                for i_pos, pos in enumerate(path + [next_step]):
                    correct_path[pos] = i_pos
            elif next_step in map and next_step != (path[-2] if len(path) > 1 else 0):
                next_paths.append(path + [next_step])
    paths = next_paths

# part 1
print('ans1: ' + str(count_cheats(2)))

# part 2
print('ans2: ' + str(count_cheats(20)))