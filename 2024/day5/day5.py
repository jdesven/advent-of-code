from pyhelper.pyimport import lines_to_list, seperator_to_list

txt = lines_to_list('2024/input/day5_input.txt')
txt_rules = [seperator_to_list(line, seperator = '|', cast = int, read_file = False) for line in txt[:txt.index('')]]
txt_tests = [seperator_to_list(line, seperator = ',', cast = int, read_file = False) for line in txt[txt.index('') + 1:]]

total = 0
for test in txt_tests:
    if all(not(rule[0] in test and rule[1] in test and test.index(rule[0]) > test.index(rule[1])) for rule in txt_rules):
        total += test[int((len(test) - 1) / 2)]
print(total)

total = 0
for test in txt_tests:
    if any(rule[0] in test and rule[1] in test and test.index(rule[0]) > test.index(rule[1]) for rule in txt_rules):
        while any(rule[0] in test and rule[1] in test and test.index(rule[0]) > test.index(rule[1]) for rule in txt_rules):
            for rule in txt_rules:
                if rule[0] in test and rule[1] in test:
                    indices = test.index(rule[0]), test.index(rule[1])
                    if rule[0] in test and rule[1] in test and indices[0] > indices[1]:
                        test[indices[0]], test[indices[1]] = test[indices[1]], test[indices[0]]
        total += test[int((len(test) - 1) / 2)]
print(total)