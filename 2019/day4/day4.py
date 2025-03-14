with open('2019/input/day4_input.txt', 'r') as file:
    range_min, range_max = [int(num) for num in file.read().split('-')]

nums = [[num] for num in range(1, 10)]
for i in range(5):
    nums_next = []
    for num in nums:
        if len(num) == 5 and len(num) == len(set(num)):
            nums_next.append(num + [num[-1]])
        else:
            for j in range(num[-1],10):
                nums_next.append(num + [j])
    nums = nums_next

nums_joined = [int("".join(map(str, num))) for num in nums]
print(len([num for num in nums_joined if range_min <= num <= range_max]))

nums_joined = [int("".join(map(str, num))) for num in nums if 2 in {char:num.count(char) for char in num}.values()]
print(len([num for num in nums_joined if range_min <= num <= range_max]))