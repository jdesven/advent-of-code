from pyhelper.pyimport import lines_to_list_of_list
from pyhelper.pyalgorithm import breadth_first_search
input = [int(x) + int(y) * 1j for x, y in lines_to_list_of_list('2024/input/day18_input.txt', ',')]

def make_map(bytes):
    input_set = set(input[:bytes])
    map = set()
    for x in range(71):
        for y in range(71):
            if x + y * 1j not in input_set:
                map.add(x + y * 1j)
    return map

map = make_map(1024)
print(len(breadth_first_search(map, 0j, 70 + 70j)) - 1)

lower_bound = 1024
upper_bound = len(input)
while upper_bound > lower_bound + 1:
    mid_point = int((lower_bound + upper_bound) / 2)
    if len(breadth_first_search(make_map(mid_point), 0j, 70 + 70j)) == 0:
        upper_bound = mid_point
    else:
        lower_bound = mid_point
print(str(int(input[upper_bound - 1].real)) + ',' + str(int(input[upper_bound - 1].imag)))