import numpy as np

map = np.array([np.array(list(line)) for line in np.loadtxt('2024/input/day6_input.txt', dtype = str, comments = None)])

# part 1
pos = np.array([np.where(map == '^')[1][0], np.where(map == '^')[0][0]])
seen_pos = {tuple(pos)}
dir = np.array([0, -1])
guard_has_escaped = False
while guard_has_escaped == False:
    if (0 <= pos[0] + dir[0] < len(map[0]) and 0 <= pos[1] + dir[1] < len(map)):
        match map[pos[1] + dir[1]][pos[0] + dir[0]]:
            case '#':
                dir = np.matmul(np.array([[0, -1], [1, 0]]), dir)
            case '.' | '^':
                pos = pos + dir
                seen_pos.add(tuple(pos))
    else:
        guard_has_escaped = True
print('answ1: ' + str(len(seen_pos)))

# part 2
count = 0
for obs_x in range(len(map[0])):
    for obs_y in range(len(map)):
        pos_dir = np.array([np.where(map == '^')[1][0], np.where(map == '^')[0][0], 0, -1])
        if map[obs_y][obs_x] == '.':
            map[obs_y][obs_x] = '#'
            escaped_or_looping = False
            seen_pos_dir = {tuple(pos_dir)}
            while escaped_or_looping == False:
                if (0 <= pos_dir[0] + pos_dir[2] < len(map[0]) and 0 <= pos_dir[1] + pos_dir[3] < len(map)):
                    match map[pos_dir[1] + pos_dir[3]][pos_dir[0] + pos_dir[2]]:
                        case '#':
                            pos_dir[2:] = np.matmul(np.array([[0, -1], [1, 0]]), pos_dir[2:])
                        case '.' | '^':
                            pos_dir[:2] = np.array([pos_dir[0] + pos_dir[2], pos_dir[1] + pos_dir[3]])
                            if tuple(pos_dir) in seen_pos_dir:
                                escaped_or_looping = True
                                map[obs_y][obs_x] = '.'
                                count += 1
                            seen_pos_dir.add(tuple(pos_dir))
                else:
                    escaped_or_looping = True
                    map[obs_y][obs_x] = '.'
print('answ1: ' + str(count))