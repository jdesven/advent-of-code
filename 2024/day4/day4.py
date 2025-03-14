import numpy as np
import pandas as pd

df = pd.read_fwf('2024/input/day4_input.txt', widths = np.ones(140, dtype = int), header = None)

# part 1
count = 0
for i in range(len(df.columns)): # columns
    for j in range(len(df)): # rows
        for x_dir in [-1, 0, 1]:
            for y_dir in [-1, 0, 1]:
                word = []
                for char_num in range(4):
                    if 0 <= i + x_dir * char_num < 140 and 0 <= j + y_dir * char_num < 140:
                        word.append(df[i + x_dir * char_num][j + y_dir * char_num])
                if word == ['X', 'M', 'A', 'S']:
                    count += 1
print('ans1: ' + str(count))

# part 2
count = 0
for i in range(len(df.columns)): # columns
    for j in range(len(df)): # rows
        if df[i][j] == 'A':
            letters = np.array([])
            for x_dir in [-1, 1]:
                for y_dir in [-1, 1]:
                    if 0 <= i + x_dir < 140 and 0 <= j + y_dir < 140:
                        letters = np.append(letters, df[i + x_dir][j + y_dir])
            if np.count_nonzero(letters == 'M') == 2 and np.count_nonzero(letters == 'S') == 2 and letters[0] != letters[3]:
                count += 1
print('ans2: ' + str(count))