from pyhelper.pyimport import grid_to_dict
from math import prod
grid = grid_to_dict("2022\input\day8_input.txt", cast = int)

print(sum(
    all(grid[key] < grid[pos] for key in [key for key in grid.keys() if key.imag == pos.imag and key.real < pos.real])\
    or all(grid[key] < grid[pos] for key in [key for key in grid.keys() if key.imag == pos.imag and key.real > pos.real])\
    or all(grid[key] < grid[pos] for key in [key for key in grid.keys() if key.imag < pos.imag and key.real == pos.real])\
    or all(grid[key] < grid[pos] for key in [key for key in grid.keys() if key.imag > pos.imag and key.real == pos.real])\
    for pos in grid.keys()))

def view_distance(grid, pos, dir):
    for i in range(1, 100):
        if pos + i * dir not in grid or grid[pos + i * dir] >= grid[pos]:
            return i - 1 if pos + i * dir not in grid else i

print(max(prod(view_distance(grid, pos, d) for d in (-1, 1, -1j, 1j)) for pos in grid))