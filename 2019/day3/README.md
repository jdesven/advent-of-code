[Link to puzzle](https://adventofcode.com/2019/day/3)
## Import

```python
from pyhelper.pyimport import lines_to_list_of_list
wires = lines_to_list_of_list('2019/input/day3_input.txt', seperator = ',')
```

## Solution
We start by defining a function `calculate_path` that creates a dictionary `path` with positions as keys, and how many steps it took to reach this position as values. We represent the coordinates as complex coordinates. The reason for doing so is further explained [here](https://github.com/jdesven/Advent-of-Code/blob/main/documentation/complex2dplane.md). For every instruction in the wire input, we add the coordinate to `path` if it does not yet contain that coordinate. We do not want to overwrite the coordinate past the first encounter, since we are looking for the shortest distances.

```python
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
```

We then calculate the paths `path_1` and `path_2` using this function. For every coordinate in `path_1`, we check if this coordinate is also in `path_2` and if so, add this point to `crossing_points`.

The answer to the first question is found by calculating the distances of the crossing points to the center, and taking the minimum.

```python
distances_to_center = [abs(int(crossing_point[0].real)) + abs(int(crossing_point[0].imag)) for crossing_point in crossing_points]
print(min(distances_to_center))
```

The answer to the second question is found by adding the lengths of the wires at the position of the crossing points, and again taking the minimum.

```python
distances_travelled = [crossing_point[1] + crossing_point[2] for crossing_point in crossing_points]
print(min(distances_travelled))
```