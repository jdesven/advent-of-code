from pyhelper.pyimport import lines_to_list
from itertools import product
codes_input = lines_to_list('2024/input/day21_input.txt')

def get_paths(pos):
    paths_dict = {}
    for digit_from in pos.keys():
        for digit_to in pos.keys():
            horizontal_movements = int(pos[digit_to].real) - int(pos[digit_from].real)
            vertical_movements = int(pos[digit_to].imag) - int(pos[digit_from].imag)
            path_hor = ''.join((['<'] if horizontal_movements < 0 else ['>']) * abs(horizontal_movements))
            path_ver = ''.join((['^'] if vertical_movements < 0 else ['v']) * abs(vertical_movements))
            paths = [path_hor + path_ver + 'A', path_ver + path_hor + 'A'] if (len(path_hor) > 0 and len(path_ver) > 0) else [path_hor + path_ver + 'A']
            if pos == pos_digits:
                paths_dict[(digit_from, digit_to)] = [path for path in paths if not (int(pos[digit_from].imag) == 3 and int(pos[digit_to].real) == 0 and path[0] == '<') and not (int(pos[digit_from].real) == 0 and int(pos[digit_to].imag) == 3 and path[0] == 'v')]
            else:
                paths_dict[(digit_from, digit_to)] = [path for path in paths if not (int(pos[digit_from].imag) == 0 and int(pos[digit_to].real) == 0 and path[0] == '<') and not (int(pos[digit_from].real) == 0 and int(pos[digit_to].imag) == 0 and path[0] == '^')]
    return paths_dict

pos_digits = {char: i_char % 3 + i_char // 3 * 1j for i_char, char in enumerate(['7', '8', '9','4', '5', '6', '1', '2', '3', '_', '0', 'A']) if char != '_'}
paths_digits = get_paths(pos_digits)
pos_directions = {char: i_char % 3 + i_char // 3 * 1j for i_char, char in enumerate(['_', '^', 'A', '<', 'v', '>']) if char != '_'}
paths_directions = get_paths(pos_directions)

complexities = 0
for code_input in codes_input:
    codes = [code_input]
    for i in range(3):
        codes_new = []
        lib_to_use = paths_digits if i == 0 else paths_directions
        for code in codes:
            adjacent_chars = zip('A' + code, code)
            routes_per_char = [lib_to_use[adjacent_char] for adjacent_char in adjacent_chars]
            paths = [''.join(subroute) for subroute in product(*routes_per_char)]
            codes_new.extend(paths)
        min_len = min(map(len, codes_new))
        codes = [code for code in codes_new if len(code) == min_len]
    complexities += len(codes[0]) * int(code_input[:3])
print(complexities)