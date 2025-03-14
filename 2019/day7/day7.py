from itertools import permutations
from pyhelper.pyimport import seperator_to_list_to_dict
input_program = seperator_to_list_to_dict('2019/input/day7_input.txt', seperator = ',', cast = int)
from importlib import import_module
intcode = getattr(import_module('2019.intcode.intcode'), 'intcode')

outs = []
for phase_settings in permutations([0, 1, 2, 3, 4]):
    amps = [intcode(input_program.copy(), [phase_setting] if i > 0 else [phase_setting, 0]) for i, phase_setting in enumerate(phase_settings)]
    for i in range(5):
        status = None
        while status == None:
            out, status = amps[i].calc_step()
            if out != None:
                if i == 4:
                    outs.append(out)
                else:
                    amps[i+1].inputs.append(out)
print(max(outs))

outs = []
for phase_settings in permutations([5, 6, 7, 8, 9]):
    amps = [intcode(input_program.copy(), [phase_setting] if i > 0 else [phase_setting, 0]) for i, phase_setting in enumerate(phase_settings)]
    i_amp = 0
    status = None
    while not (status == 99 and i_amp == 0):
        status = None
        while status == None:
            out, status = amps[i_amp].calc_step()
            if out != None:
                amps[i_amp+1].inputs.append(out) if i_amp < 4 else amps[0].inputs.append(out)
        i_amp = (i_amp + 1 if i_amp < 4 else 0)
    outs.append(amps[0].inputs[-1])
print(max(outs))