with open('2024/input/day18_input.txt', 'r') as file:
    input = [int(line[0]) + int(line[1]) * 1j for line in [line.split(',') for line in file.read().splitlines()]]

def bfs_shortest_path(bytes):
    map = {}
    for x in range(71):
        for y in range(71):
            map[x + y * 1j] = '.'
    for coord in input[:bytes]:
        map[coord] = '#'

    coords_seen = {0 + 0j}
    potential_paths = [[0 + 0j]]
    path_i = 0
    while path_i < len(potential_paths):
        path = potential_paths[path_i]
        for dir in [-1, 1, -1j, 1j]:
            next_pos = path[-1] + dir
            if next_pos == 70 + 70j:
                solution = set(path)
                path_i = len(potential_paths)
            elif map.get(next_pos) == '.' and next_pos not in coords_seen:
                coords_seen.add(next_pos)
                potential_paths.append(path + [next_pos])
        path_i += 1
    return solution if 'solution' in locals() else set()

# part 1
print('ans1: ' + str(len(bfs_shortest_path(1024))))

# part 2
lower_bound = 1024
upper_bound = len(input)
while upper_bound > lower_bound + 1:
    mid_point = int((lower_bound + upper_bound) / 2)
    if len(bfs_shortest_path(mid_point)) == 0:
        upper_bound = mid_point
    else:
        lower_bound = mid_point
print('ans2: ' + str(int(input[upper_bound - 1].real)) + ',' + str(int(input[upper_bound - 1].imag)))