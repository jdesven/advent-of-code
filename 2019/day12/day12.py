from pyhelper.pyimport import lines_to_list_of_list
from numpy import sign
from math import lcm
input = lines_to_list_of_list('2019/input/day12_input.txt', seperator = ',', cast = int, regex = '[-0-9,]')
class planet:
    def __init__(self, pos):
        self.pos = pos
        self.dir = [0, 0, 0]

def calc_step(planets):
    for p1 in planets:
        for p2 in [p for p in planets if p != p1]:
            for coord in range(3):
                p1.dir[coord] += int(sign(p2.pos[coord] - p1.pos[coord]))
    for p in planets:
        p.pos = [p.pos[i] + p.dir[i] for i in range(3)]
    
planets = [planet(input[i].copy()) for i in range(len(input))]
for step in range(1000):
    calc_step(planets)
print(sum([sum([abs(num) for num in p.pos]) * sum([abs(num) for num in p.dir]) for p in planets]))

steps_until_loop = {}
planets = [planet(input[i].copy()) for i in range(len(input))]
coords_init = [p.pos for p in planets]
amount_steps = 0
while len(steps_until_loop) < 3:
    calc_step(planets)
    amount_steps += 1
    for coord in range(3):
        if ([p.pos[coord] for p in planets] == [coords[coord] for coords in coords_init]
            and [p.dir[coord] for p in planets] == [0] * len(planets)
            and coord not in steps_until_loop
        ):
            steps_until_loop[coord] = amount_steps
print(lcm(*steps_until_loop))