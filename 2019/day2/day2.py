from pyhelper.pyimport import seperator_to_list_to_dict
program = seperator_to_list_to_dict('2019/input/day2_input.txt', seperator = ',', cast = int)
from importlib import import_module
intcode = getattr(import_module('2019.intcode.intcode'), 'intcode')

def run_until_terminate(com):
    last_status = None
    while last_status != 99:
        _, last_status = com.calc_step()

com = intcode({**program, 1: 12, 2: 2}, [])
run_until_terminate(com)
print(com.program[0])

for noun in range(100):
    for verb in range(100):
        com = intcode({**program, 1: noun, 2: verb}, [])
        run_until_terminate(com)
        if com.program[0] == 19690720:
            print(100 * noun + verb)