with open('2024/input/day19_input.txt', 'r') as file:
    towels_string, patterns_string = file.read().split('\n\n')
towels = towels_string.split(', ')
patterns = patterns_string.split('\n')

def count_combinations(pattern, towels):
    pattern_parts_counts = {pattern[:i]:0 if i > 0 else 1 for i in range(len(pattern) + 1)}
    for pattern_part in pattern_parts_counts:
        for towel in towels:
                if pattern_part + towel in pattern_parts_counts:
                     pattern_parts_counts[pattern_part + towel] += pattern_parts_counts[pattern_part] 
    return pattern_parts_counts[pattern]

#part 1
print('ans1: ' + str(sum([1 if count_combinations(pattern,towels) > 0 else 0 for pattern in patterns])))

# part 2
print('ans2: ' + str(sum([count_combinations(pattern,towels) for pattern in patterns])))