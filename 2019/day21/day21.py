from pyhelper.pyimport import seperator_to_list_to_dict
from importlib import import_module
program = seperator_to_list_to_dict('2019/input/day21_input.txt', seperator = ',', cast = int)
intcode = getattr(import_module('2019.intcode.intcode'), 'intcode')

# J IF A is NOT
#   NOT A J
# J IF B is NOT
#   NOT B T
#   OR T J
# J IF C is NOT
#   NOT C T
#   OR T J
# dont J if D is NOT
#   AND D J

# dont J if E and H are NOT
#   NOT T T
#   OR E T
#   OR H T
#   AND T J

def run(instructions):
    springdroid = intcode(program.copy(), [])
    for instruction in instructions:
        for char in instruction:
            springdroid.inputs.append(ord(char))
        springdroid.inputs.append(ord('\n'))
    status = None
    while status == None:
        out, status = springdroid.calc_step()
        if out != None:
            last_out = out
    print(last_out)

run(['NOT A J', 'NOT B T', 'OR T J', 'NOT C T', 'OR T J', 'AND D J', 'WALK'])

run(['NOT A J', 'NOT B T', 'OR T J', 'NOT C T', 'OR T J', 'AND D J', 'NOT T T', 'OR E T', 'OR H T', 'AND T J','RUN'])