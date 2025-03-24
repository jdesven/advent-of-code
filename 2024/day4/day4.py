from pyhelper.pyimport import grid_to_dict
grid = grid_to_dict('2024/input/day4_input.txt')

count = 0
for pos in grid:
    for dir in [-1 -1j, -1j, 1 - 1j, -1, 1, -1 + 1j, 1j, 1 + 1j]:
        word = []
        for char_num in range(4):
            word.append(grid.get(pos + dir * char_num))
        if word == ['X', 'M', 'A', 'S']:
            count += 1
print(count)

count = 0
for pos in [pos for pos in grid.keys() if grid[pos] == 'A']:
    letters = []
    for dir in (-1 - 1j, 1 - 1j, -1 + 1j, 1 + 1j):
        letters.append(grid.get(pos + dir))
    if letters.count('M') == 2 and letters.count('S') == 2 and letters[0] != letters[3]:
        count += 1
print(count)