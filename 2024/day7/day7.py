from itertools import combinations_with_replacement
from sympy.utilities.iterables import multiset_permutations
from math import log
from pyhelper.pyimport import lines_to_list, seperator_to_list

tests = [(int(line[:line.index(':')]), tuple(seperator_to_list(line[line.index(':') + 2:], seperator = ' ', cast = int, read_file = False))) for line in lines_to_list('2024/input/day7_input.txt')]

total = 0
for answer, numbers in tests:
    answer_found = False
    for combination in list(combinations_with_replacement(['+', '*'], len(numbers) - 1)):
        for permutation in multiset_permutations(combination):
            if answer_found == False:
                calculation = numbers[0]
                for i_operator, operator in enumerate(permutation, start = 1):
                    if operator == '+':
                        calculation += numbers[i_operator]
                    elif operator == '*':
                        calculation *= numbers[i_operator]
                if calculation == answer:
                    answer_found = True
                    total += calculation
print(total)

total = 0
for answer, numbers in tests:
    answer_found = False
    for combination in list(combinations_with_replacement(['+', '*', '|'], len(numbers) - 1)):
        for permutation in list(multiset_permutations(combination)):
            if answer_found == False:
                calculation = numbers[0]
                for i_operator, operator in enumerate(permutation, start = 1):
                    if operator == '|':
                        calculation = 10**int(log(numbers[i_operator], 10) + 1) * calculation + numbers[i_operator]
                    elif operator == '+':
                        calculation += numbers[i_operator]
                    elif operator == '*':
                        calculation *= numbers[i_operator]
                if calculation == answer:
                    answer_found = True
                    total += calculation
print(total)