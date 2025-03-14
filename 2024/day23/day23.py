from itertools import combinations

with open('2024/input/day23_input.txt', 'r') as file:
    input = [line.split('-') for line in file.read().splitlines()]

connections = {}
for com in [com for connection in input for com in connection]:
    connections[com] = set()
for com_1, com_2 in input:
    connections[com_1].add(com_2)
    connections[com_2].add(com_1)

# part 1
sequences = set()
for com_1, com_1_connections in [connection for connection in connections.items() if connection[0][0] == 't']:
    for com_2 in com_1_connections:
        for com_3 in [connection for connection in connections[com_2] if connection in com_1_connections]:
            sequences.add(frozenset([com_1, com_2, com_3]))
print('ans1: ' + str(len(sequences)))

# part 2
set_size = max([len(values) for values in connections.values()])
largest_set = []
while largest_set == []:
    for com, com_connections in connections.items():
        if len(com_connections) >= set_size:
            for combination in combinations(com_connections, set_size):
                combination_is_connected = True
                for com_1 in combination:
                    for com_2 in combination:
                        if com_1 != com_2 and com_2 not in connections[com_1]:
                            combination_is_connected = False
                if combination_is_connected == True:
                    largest_set = sorted(list(combination) + [com])
    set_size -= 1
print('ans2: ' + ','.join(largest_set))