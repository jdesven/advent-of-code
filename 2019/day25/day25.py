from pyhelper.pyimport import seperator_to_list_to_dict
from importlib import import_module
program = seperator_to_list_to_dict('2019/input/day25_input.txt', seperator = ',', cast = int)
intcode = getattr(import_module('2019.intcode.intcode'), 'intcode')

droid = intcode(program, [])
while True:
    status = None
    outs = []
    while status == None:
        out, status = droid.calc_step()
        if out != None:
            outs.append(out)
    print(''.join([chr(out) for out in outs]))

    print('Options: north, south, east, west, take <name>, drop <name>, inv')
    for char in input():
        droid.inputs.append(ord(char))
    droid.inputs.append(ord('\n'))