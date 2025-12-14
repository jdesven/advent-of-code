ranges, ingredients = open("2025\input\day5_input.txt").read().split('\n\n')
ranges = sorted([[int(n) for n in r.split('-')] for r in ranges.split()])
ingredients = [int(n) for n in ingredients.split()]

print(sum(any(s <= ingredient <= e for s, e in ranges) for ingredient in ingredients))

ranges = [ranges[0]] + [ranges[i] for i in range(1, len(ranges)) if ranges[i][1] > ranges[i - 1][1]]
amount = ranges[0][1] - ranges[0][0] + 1
for i in range(1, len(ranges)):
    if ranges[i][0] > ranges[i - 1][1]:
        amount += ranges[i][1] - ranges[i][0] + 1
    else:
        amount += ranges[i][1] - ranges[i - 1][1]
print(amount)