from re import match
num_ranges = [[int(i) for i in r.split('-')] for r in open("2025\input\day2_input.txt").read().split(',')]

print(sum([sum([num for num in range(a, b + 1) if match(r'^(\d+)\1$', str(num))]) for a, b in num_ranges]))

print(sum([sum([num for num in range(a, b + 1) if match(r'^(\d+)\1+$', str(num))]) for a, b in num_ranges]))