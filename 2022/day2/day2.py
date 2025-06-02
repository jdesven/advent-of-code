from pyhelper.pyimport import seperator_to_list
input = seperator_to_list("2022\input\day2_input.txt", '\n')
guide = [(ord(opponent) - 65, ord(you) - 88) for opponent, you in [nums.split(' ') for nums in input]]

print(sum([you + 1 + ((you - opponent + 1) % 3) * 3 for opponent, you in guide]))

print(sum([result * 3 + (opponent + result - 1) % 3 + 1 for opponent, result in guide]))