from pyhelper.pyimport import seperator_to_list_to_dict
from importlib import import_module
program = seperator_to_list_to_dict('2019/input/day19_input.txt', seperator = ',', cast = int)
intcode = getattr(import_module('2019.intcode.intcode'), 'intcode')

def check(pos):
    drone = intcode(program.copy(), [int(pos.real), int(pos.imag)])
    while True:
        out, _ = drone.calc_step()
        if out != None:
            return out
        
count = 0
for x in range(50):
    for y in range(50):
        if check(x + y*1j) == 1:
            count += 1
print(count)

pos = 0j
while True:
    if check(pos + 1) == 1:
        pos += 1
    else:
        pos += 1 + 1j
    if pos.real > 100 and pos.imag > 100:
        if check(pos - 99) == 1 and check(pos - 99 + 99j) == 1:
            break
print((int(pos.real) - 99) * 10000 + int(pos.imag))