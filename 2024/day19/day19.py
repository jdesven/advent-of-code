from pyhelper.pyimport import lines_to_list, seperator_to_list
lines = lines_to_list('2024/input/day19_input.txt')
towels = seperator_to_list(lines[0], seperator = ', ', read_file = False)
patterns = lines[2:]

def count_combinations(pattern, towels):
    pattern_parts_counts = {pattern[:i]:0 if i > 0 else 1 for i in range(len(pattern) + 1)}
    for pattern_part in pattern_parts_counts:
        for towel in towels:
                if pattern_part + towel in pattern_parts_counts:
                     pattern_parts_counts[pattern_part + towel] += pattern_parts_counts[pattern_part] 
    return pattern_parts_counts[pattern]

print(sum([1 if count_combinations(pattern,towels) > 0 else 0 for pattern in patterns]))

print(sum([count_combinations(pattern,towels) for pattern in patterns]))