with open('2024/input/day21_input.txt', 'r') as file:
    codes = file.read().splitlines()

num_keypad = {0 if num == 1 else 'A' if num == 2 else num - 2 : (num % 3) + int(num / 3) * 1j  for num in range(1, 12)}
dir_keypad = {dir : (dir_i % 3) + int(dir_i / 3) * 1j + (1 if dir in ['^', 'A'] else 0) for dir_i, dir in enumerate(['<', 'v', '>', '^', 'A'])}