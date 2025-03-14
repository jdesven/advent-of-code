from pyhelper.pyimport import seperator_to_list_to_dict
from importlib import import_module
from itertools import count
program = seperator_to_list_to_dict('2019/input/day17_input.txt', seperator = ',', cast = int)
intcode = getattr(import_module('2019.intcode.intcode'), 'intcode')

robot = intcode(program.copy(), [])
pos = 0j
map = {}
while True:
    out, status = robot.calc_step()
    if out in [ord(char) for char in ('#', '.', '^')]:
        map[pos] = chr(out)
        pos += 1
    elif out == ord('\n'):
        pos = int(pos.imag) * 1j + 1j
    if status != None:
        break
crossing_points = [pos for pos in map.keys() if all(map.get(pos + dir) in ('#','^') for dir in [0, -1j, 1j, -1, 1])]
print(sum(int(pos.real) * int(pos.imag) for pos in crossing_points))

def find_functions(instructions, possible_functions):
    for A in [func for func in possible_functions if func[0] == instructions[0]]:
        for B in possible_functions:
            for C in ([func for func in possible_functions if func[-1] == instructions[-1]] if A[-1] != instructions[-1] else possible_functions):
                reconstruction = []
                main_routine = []
                while len(reconstruction) < len(instructions):
                    len_before_extending = len(reconstruction)
                    for func in [A, B, C]:
                        if tuple(instructions[len(reconstruction):len(reconstruction)+len(func)]) == func:
                            reconstruction.extend(func)
                            main_routine.append({A: 'A', B: 'B', C: 'C'}[func])
                    if len(reconstruction) == len_before_extending:
                        break
                if reconstruction == instructions:
                    return main_routine, A, B, C, 'n'

instructions = []
dir = -1j
pos = [pos for pos, val in map.items() if val == '^'][0]
while True:
    len_before_appending = len(instructions)
    for rot in [-1j, 1j]:
        if map.get(pos + dir * rot) == '#':
            instructions.append({-1j: 'L', 1j: 'R'}[rot])
            dir = dir * rot
    if len(instructions) == len_before_appending:
        break
    len_straight = next(i for i in count(1) if map.get(pos + dir * i) != '#')
    pos += dir * (len_straight - 1)
    instructions.append(len_straight - 1)
possible_functions = set()
for i_instruction in range(len(instructions)):
    for i_len in range(min(len(instructions) - i_instruction, 10)):
        possible_functions.add(tuple(instructions[i_instruction:i_instruction + i_len + 1]))
robot = intcode({**program.copy(), 0: 2}, [])
for func in find_functions(instructions, possible_functions):
    for i_instruction, instruction in enumerate(func, start = 1):
        for char in str(instruction):
            robot.inputs.append(ord(str(char)))
        robot.inputs.append(ord(',' if i_instruction < len(func) else '\n'))
while True:
    out, status = robot.calc_step()
    if out != None:
        last_out = out
    if status != None:
        print(last_out)
        break