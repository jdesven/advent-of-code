import numpy as np

with open('2024/input/day5_input.txt', 'r') as file:
    txt = np.array(file.read().splitlines())
txt_rules = [np.array(row).astype(int) for row in np.asarray(np.char.split(txt[0:np.where(txt == '')[0][0]],'|'))]
txt_tests = [np.array(row).astype(int) for row in np.asarray(np.char.split(txt[np.where(txt == '')[0][0] + 1::],','))]

# part 1
total = 0
for test in txt_tests:
    is_valid = True
    for rule in txt_rules:
        if rule[0] in test and rule[1] in test and is_valid == True:
            if np.where(test == rule[0])[0] > np.where(test == rule[1])[0]:
                is_valid = False
    if is_valid == True:
        total += test[int((test.size - 1) / 2)]
print('ans1: ' + str(total))

# part 2
total = 0
for test in txt_tests:
    is_valid = False
    is_initially_false = False
    while is_valid == False:
        is_valid = True
        for rule in txt_rules:
            if rule[0] in test and rule[1] in test:
                if np.where(test == rule[0])[0] > np.where(test == rule[1])[0]:
                    test = np.insert(np.delete(test, np.where(test == rule[0])[0]), np.where(test == rule[1])[0], rule[0])
                    is_valid = False
                    is_initially_false = True
    if is_initially_false == True:
        total += test[int((test.size - 1) / 2)]
print('ans2: ' + str(total))