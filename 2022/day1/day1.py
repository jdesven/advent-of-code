from pyhelper.pyimport import seperator_to_list
elves = sorted([sum(list(map(int,elf.split('\n')))) for elf in seperator_to_list("2022\input\day1_input.txt", '\n\n')], reverse = True)

print(elves[0])

print(sum(elves[:3]))