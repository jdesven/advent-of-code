from pyhelper.pyimport import lines_to_list_of_list
input = [[[int(num) for num in elf.split('-')] for elf in row] for row in lines_to_list_of_list("2022\input\day4_input.txt", seperator = ',')]

print(sum((row[0][0] <= row[1][0] and row[0][1] >= row[1][1]) or (row[0][0] >= row[1][0] and row[0][1] <= row[1][1]) for row in input))

print(sum((row[0][0] <= row[1][0] and row[0][1] >= row[1][0]) or (row[1][0] <= row[0][0] and row[1][1] >= row[0][0]) for row in input))