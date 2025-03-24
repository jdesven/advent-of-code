from itertools import combinations
from pyhelper.pyimport import lines_to_list_of_list
input = lines_to_list_of_list('2024/input/day23_input.txt', seperator = '-')

connections = {com: set() for com in set([com for comm in input for com in comm])}
for com_1, com_2 in input:
    connections[com_1].add(com_2)
    connections[com_2].add(com_1)

sequences = set()
for com_1, com_1_connections in [connection for connection in connections.items() if connection[0][0] == 't']:
    for com_2 in com_1_connections:
        for com_3 in [connection for connection in connections[com_2] if connection in com_1_connections]:
            sequences.add(frozenset([com_1, com_2, com_3]))
print(len(sequences))

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
print(','.join(largest_set))