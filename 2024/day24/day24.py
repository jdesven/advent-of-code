with open('2024/input/day24_input.txt', 'r') as file:
    initial_string, gates_string = file.read().split('\n\n')
initial = [[gate.split(': ')[0], int(gate.split(': ')[1])] for gate in initial_string.splitlines()]
gates = [gate.split(' ') for gate in gates_string.replace(' ->', '').splitlines()]

def calc_bitwise_z(initial, gates):
    gates_status = {}
    for gate, status in initial:
        gates_status[gate] = status
    while len(gates_status) < len(gates) + len(initial):
        for in_1, cond, in_2, out in gates:
            if in_1 in gates_status and in_2 in gates_status:
                match cond:
                    case 'OR':
                        gates_status[out] = 1 if gates_status[in_1] == 1 or gates_status[in_2] == 1 else 0
                    case 'AND':
                        gates_status[out] = 1 if gates_status[in_1] == 1 and gates_status[in_2] == 1 else 0
                    case 'XOR':
                        gates_status[out] = 1 if gates_status[in_1] != gates_status[in_2] else 0
    return ''.join([str(gates_status[1]) for gates_status in sorted(gates_status.items(), reverse = True) if gates_status[0][0] == 'z'])

# part 1
print('ans1: ' + str(int(calc_bitwise_z(initial, gates), 2)))