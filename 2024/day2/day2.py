from pyhelper.pyimport import lines_to_list_of_list
nums = lines_to_list_of_list("2024\input\day2_input.txt", ' ', int)

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