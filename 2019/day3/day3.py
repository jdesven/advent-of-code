from pyhelper.pyimport import lines_to_list_of_list
wires = lines_to_list_of_list('2019/input/day3_input.txt', seperator = ',')

def calculate_path(wire):
    path = {}
    location = 0j
    location_i = 0
    for instruction in wire:
        dir = {'L': -1 + 0j, 'U': -1j, 'R': 1 + 0j, 'D': 1j}[instruction[0]]
        for i in range(1, int(instruction[1:]) + 1):
            location_i += 1
            if location + i * dir not in path:
                path[location + i * dir] = location_i
        location = location + int(instruction[1:]) * dir
    return path

crossing_points = set()
path_1 = calculate_path(wires[0])
path_2 = calculate_path(wires[1])
for location, i_location in path_1.items():
    if location in path_2:
        crossing_points.add((location, i_location, path_2[location]))

distances_to_center = [abs(int(crossing_point[0].real)) + abs(int(crossing_point[0].imag)) for crossing_point in crossing_points]
print(min(distances_to_center))

distances_travelled = [crossing_point[1] + crossing_point[2] for crossing_point in crossing_points]
print(min(distances_travelled))