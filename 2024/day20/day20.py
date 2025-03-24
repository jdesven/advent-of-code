from pyhelper.pyimport import grid_to_dict
from pyhelper.pyalgorithm import breadth_first_search
map = grid_to_dict('2024/input/day20_input.txt', relevant_chars = {'.', 'S', 'E'})

start_point = [pos for pos, val in map.items() if val == 'S'][0]
end_point = [pos for pos, val in map.items() if val == 'E'][0]
correct_path = {pos: i for i, pos in enumerate(breadth_first_search(map.keys(), start_point, end_point))}

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

print(count_cheats(2))

print(count_cheats(20))