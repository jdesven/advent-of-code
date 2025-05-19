from pyhelper.pyimport import lines_to_list

sequences = []
for secret_number in lines_to_list('2024/input/day22_input.txt', cast = int):
    sequence = [secret_number]
    for iteration in range(2000):
        secret_number = ((secret_number * 64) ^ secret_number) % 16777216
        secret_number = ((secret_number // 32) ^ secret_number) % 16777216
        secret_number = ((secret_number * 2048) ^ secret_number) % 16777216
        sequence.append(secret_number)
    sequences.append(sequence)
print(sum([sequence[-1] for sequence in sequences]))

sequences_bananas = [[num % 10 for num in sequence] for sequence in sequences]
sequences_differences = [[num_2 - num_1 for num_1, num_2 in zip(sequence, sequence[1:])] for sequence in sequences_bananas]
dict_sequences = {}
for i_sequence in range(len(sequences)):
    patterns_seen = set()
    pattern = tuple([0] + sequences_differences[i_sequence][:3])
    for i_num in range(3, len(sequence) - 1):
        pattern = tuple(pattern[1:] + tuple([sequences_differences[i_sequence][i_num]]))
        if pattern not in patterns_seen:
            if pattern not in dict_sequences.keys():
                dict_sequences[pattern] = [sequences_bananas[i_sequence][i_num + 1]]
            else:
                dict_sequences[pattern].append(sequences_bananas[i_sequence][i_num + 1])
            patterns_seen.add(pattern)
print(max([sum(bananas) for bananas in dict_sequences.values()]))