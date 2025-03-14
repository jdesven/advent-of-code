from pyhelper.pyimport import seperator_to_list_to_dict
program = seperator_to_list_to_dict('2019/input/day9_input.txt', seperator = ',', cast = int)
from importlib import import_module
intcode = getattr(import_module('2019.intcode.intcode'), 'intcode')

def run_until_terminate(com):
    last_status = None
    while last_status != 99:
        out, last_status = com.calc_step()
        if out != None:
            print(out)

run_until_terminate(intcode(program.copy(), [1]))
run_until_terminate(intcode(program.copy(), [2]))