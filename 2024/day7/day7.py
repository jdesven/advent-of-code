import numpy as np
from itertools import combinations_with_replacement
from sympy.utilities.iterables import multiset_permutations
from math import log

with open('2024/input/day7_input.txt', 'r') as file:
    txt = np.array(file.read().splitlines())
tests = [int(row.split(':')[0]) for row in txt]
nums = [np.array(list(map(int, row.split(' ')))) for row in np.array([row.split(':')[1][1:] for row in txt])]

# part 1
total = 0
for i_test, test in enumerate(tests):
    answer_found = False
    combinations = list(combinations_with_replacement(['+', '*'], len(nums[i_test]) - 1))
    for combination in combinations:
        permutations = list(multiset_permutations(combination))
        for permutation in permutations:
            if answer_found == False:
                calculation = nums[i_test][0]
                for i_operator, operator in enumerate(permutation):
                    match operator:
                        case '+':
                            calculation += nums[i_test][i_operator + 1]
                        case '*':
                            calculation *= nums[i_test][i_operator + 1]
                if calculation == test:
                    answer_found = True
                    total += calculation
print('ans1: ' + str(total))

# part 1
total = 0
for i_test, test in enumerate(tests):
    answer_found = False
    combinations = list(combinations_with_replacement(['+', '*', '|'], len(nums[i_test]) - 1))
    for combination in combinations:
        permutations = list(multiset_permutations(combination))
        for permutation in permutations:
            calculation = nums[i_test][0]
            num_next = nums[i_test][1]
            for i_operator, operator in enumerate(permutation):
                if answer_found == False:
                    match operator:
                        case '|':
                            calculation = 10**int(log(num_next, 10)+1)*calculation+num_next
                            if i_operator + 1 < len(permutation):
                                num_next = nums[i_test][i_operator + 2]
                        case '+':
                            calculation += num_next
                            if i_operator + 1 < len(permutation):
                                num_next = nums[i_test][i_operator + 2]
                        case '*':
                            calculation *= num_next
                            if i_operator + 1 < len(permutation):
                                num_next = nums[i_test][i_operator + 2]
            if calculation == test:
                answer_found = True
                total += calculation
print('ans1: ' + str(total))