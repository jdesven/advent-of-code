from pyhelper.pyimport import seperator_to_list_to_dict
from importlib import import_module
from numpy import sign
program = seperator_to_list_to_dict('2019/input/day13_input.txt', seperator = ',', cast = int)
intcode = getattr(import_module('2019.intcode.intcode'), 'intcode')

def calc_until_status(game):
    status = None
    out_list = []
    while status == None:
        out, status = game.calc_step()
        if out != None:
            out_list.append(out)
    screen = {}
    for i in range(0, len(out_list) - 1, 3):
        screen[out_list[i] + out_list[i + 1] * 1j] = out_list[i + 2]
        match out_list[i + 2]:
            case 3:
                tile_paddle = out_list[i] + out_list[i + 1] * 1j
            case 4:
                tile_ball = out_list[i] + out_list[i + 1] * 1j
    return (screen, tile_paddle, tile_ball) if status != 99 else (screen, 0, 0)

game = intcode(program.copy(), [])
screen, *_ = calc_until_status(game)
print(len([tile for tile in screen.values() if tile == 2]))

game = intcode(program.copy(), [0])
game.program[0] = 2
screen, tile_paddle, tile_ball = calc_until_status(game)
while game.program[game.ptr] != 99:
    game.inputs.append(sign(tile_ball.real - tile_paddle.real))
    screen_new, tile_paddle, tile_ball = calc_until_status(game)
    screen.update(screen_new)
print(screen[-1])