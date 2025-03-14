from pyhelper.pyimport import seperator_to_list_to_dict
from importlib import import_module
program = seperator_to_list_to_dict('2019/input/day23_input.txt', seperator = ',', cast = int)
intcode = getattr(import_module('2019.intcode.intcode'), 'intcode')

computers = []
for address in range(50):
    computers.append(intcode(program.copy(), [address]))
address = 0
while True:
    if computers[address].ptr_inputs == 0 or len(computers[address].inputs) == computers[address].ptr_inputs:
        computers[address].inputs.append(-1)
    outs = []
    status = None
    while len(outs) < 3 and status != 3:
        out, status = computers[address].calc_step()
        if out != None:
            outs.append(out)
    if len(outs) == 3:
        if outs[0] == 255:
            print(outs[2])
            break
        else:
            computers[outs[0]].inputs.extend(outs[1:])
    address = 0 if address == 49 else (address + 1)

computers = []
for address in range(50):
    computers.append(intcode(program.copy(), [address]))
address = 0
prev_nat_y = None
while True:
    if address == 0:
        is_idle = True
    if computers[address].ptr_inputs == 0 or len(computers[address].inputs) == computers[address].ptr_inputs:
        computers[address].inputs.append(-1)
    outs = []
    status = None
    while len(outs) < 3 and status != 3:
        out, status = computers[address].calc_step()
        if out != None:
            outs.append(out)
    if len(outs) == 3:
        is_idle = False
        if outs[0] == 255:
            nat = outs[1:]
        else:
            computers[outs[0]].inputs.extend(outs[1:])
    if address == 49 and is_idle == True:
        if nat[1] == prev_nat_y:
            print(nat[1])
            break
        else:
            computers[0].inputs.extend(nat)
            prev_nat_y = nat[1]
    address = 0 if address == 49 else (address + 1)