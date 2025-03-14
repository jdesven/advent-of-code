from pyhelper.pyimport import seperator_to_list_to_dict
from pyhelper.pytransform import coord_dict_to_nested_list
from importlib import import_module
program = seperator_to_list_to_dict('2019/input/day11_input.txt', seperator = ',', cast = int)
intcode = getattr(import_module('2019.intcode.intcode'), 'intcode')

def paint_map(robot):
    pos = 0j
    dir = -1j
    map = {}
    output_step = 0
    status = None
    while status != 99:
        out, status = robot.calc_step()
        if out != None:
            match output_step:
                case 0:
                    map[pos] = out
                    output_step = 1
                case 1:
                    dir = dir * (-1j if out == 0 else 1j)
                    pos += dir
                    robot.inputs.append(map[pos] if pos in map else 0)
                    output_step = 0
    return map

map = paint_map(intcode(program.copy(), [0]))
print(len(map))

map = paint_map(intcode(program.copy(), [1]))
map_to_list = [['#' if num == 1 else ' ' for num in row] for row in coord_dict_to_nested_list(map, 0)]
for row in map_to_list:
    print(row)