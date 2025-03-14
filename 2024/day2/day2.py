with open('2024/input/day2_input.txt', 'r') as file:
    nums = [list(map(int,(line))) for line in[row.split(' ') for row in file.read().splitlines()]]

def test_if_safe(row):
    asc_desc_factor = 'asc' if row[0] < row[1] else 'desc'
    for j in range(len(row) - 1):
        if (asc_desc_factor == 'asc' and row[j] >= row[j + 1]) \
                or (asc_desc_factor == 'desc' and row[j] <= row[j + 1]) \
                or (abs(row[j] - row[j + 1]) > 3):
            return False
    return True

print(len([row for row in nums if test_if_safe(row) == True]))

print(len([row for row in nums if len([j for j in range(len(row)) if test_if_safe(row[:j] + row[j+1:]) == True]) > 0]))