from pyhelper.pyimport import lines_to_list_of_list
nums = lines_to_list_of_list("2024\input\day1_input.txt", '   ', int)

nums_left = sorted([row[0] for row in nums])
nums_right = sorted([row[1] for row in nums])

print(sum([abs(nums_left[i] - nums_right[i]) for i in range(len(nums))]))

print(sum([nums_left[i] * nums_right.count(nums_left[i]) for i in range(len(nums))]))