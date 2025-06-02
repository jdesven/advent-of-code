from pyhelper.pyimport import lines_to_list_of_list
rucksacks = lines_to_list_of_list("2022\input\day3_input.txt", seperator = '')

letters = [[l for l in r[:len(r) // 2] if l in r[len(r) // 2:]][0] for r in rucksacks]
print(sum([ord(l) - (96 if ord(l) > 90 else 38) for l in letters]))

letters = [[l for l in g[0] if l in g[1] and l in g[2]][0] for g in zip(*[iter(rucksacks)] * 3)]
print(sum([ord(l) - (96 if ord(l) > 90 else 38) for l in letters]))