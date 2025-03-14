[Link to puzzle](https://adventofcode.com/2019/day/17)\
[Link to Intcode](https://github.com/jdesven/advent-of-code/tree/main/2019/intcode)

## Import

```python
from pyhelper.pyimport import seperator_to_list_to_dict
from importlib import import_module
program = seperator_to_list_to_dict('2019/input/day17_input.txt', seperator = ',', cast = int)
intcode = getattr(import_module('2019.intcode.intcode'), 'intcode')
```

## Solution part 1
We let the Intcode `robot` calculate steps until it returns a status. During runtime, any outputs are saved to `map` with complex coordinates as keys and the contents of the positions as values. More information on the use of complex numbers as coordinates can be found [here](https://github.com/jdesven/Advent-of-Code/blob/main/documentation/complex2dplane.md). If the output is any character other than `\n`, the output is saved to `map` and the position is shifted one position to the right. In the complex plane, this equals `pos += 1`. If the output is `\n`, then only the complex part of `pos` is kept and `1j` is added. That result is essentially equal to a newline.

Crossing points are points where both the point itself, as well as all of the non-diagonal neighbors of that point equal scaffolding `#`. The solution to the first part of the puzzle is the sum of the product of the real and imaginary parts of these coordinates.

```python
robot = intcode(program.copy(), [])
pos = 0j
map = {}
while True:
    out, status = robot.calc_step()
    if out in [ord(char) for char in ('#', '.', '^')]:
        map[pos] = chr(out)
        pos += 1
    elif out == ord('\n'):
        pos = int(pos.imag) * 1j + 1j
    if status != None:
        break
crossing_points = [pos for pos in map.keys() if all(map.get(pos + dir) in ('#','^') for dir in [0, -1j, 1j, -1, 1])]
print(sum(int(pos.real) * int(pos.imag) for pos in crossing_points))
```

## Solution part 2

As a first step, we will need to find the sequence `sequence` that `robot` needs to traverse to reach the end. We do this by alternating between two steps, until `robot` reaches a point where turning left or right does not reveal a new scaffolding position. This would indicate that `robot` has found the end of the path.

1. First, we check if a new scaffolding position is found if `robot` turns either left or right with `map.get(pos + dir * rot) == '#':`. If either is possible, then rotate `robot` in this direction and add this rotation to `instructions`. If rotating is not possible (i.e. `len(instructions)` has not changed since trying to rotate), then `robot` has reached the end of the path.
2. Second, we calculate the length `len_straight` that `robot` can take in direction `dir` without falling off the scaffolding. We do this by using the `itertools` function `count`, which creates an iterator over an infinite list of ascending integers. By taking the first integer that does not contain scaffolding, we count the steps that `robot` can take without falling off. We add this length to `instructions`.

```python
from itertools import count

instructions = []
dir = -1j
pos = [pos for pos, val in map.items() if val == '^'][0]
while True:
    len_before_appending = len(instructions)
    for rot in [-1j, 1j]:
        if map.get(pos + dir * rot) == '#':
            instructions.append({-1j: 'L', 1j: 'R'}[rot])
            dir = dir * rot
    if len(instructions) == len_before_appending:
        break
    len_straight = next(i for i in count(1) if map.get(pos + dir * i) != '#')
    pos += dir * (len_straight - 1)
    instructions.append(len_straight - 1)
```

After breaking the `while`-loop, we obtain the full list `instructions`. However, the list is too long to load into the Intcode memory. Therefore, we need to find the movement functions `A`, `B` and `C` to break up `instructions` into repeating patterns.

We will loop over all sensible combinations of `A`, `B` and `C` until we find the combination that can recreate `instructions`. To do so, we must first contruct the set `possible_functions`, which consists of all possible list slices inside `instructions`. By choosing to store this into a set, we make sure that every unique slice is only stored once. We iterate over every position in `instructions`, and add all possible slices inside `instructions` that start with this position and end at any point after this position. Since the memory of a movement function can be at most 20 characters (including seperation commas),  slices cannot be longer than 10 characters.

``` python
possible_functions = set()
for i_instruction in range(len(instructions)):
    for i_len in range(min(len(instructions) - i_instruction, 10)):
        possible_functions.add(tuple(instructions[i_instruction:i_instruction + i_len + 1]))
```

Next, we must find the movement functions `A`, `B`, and `C`, that can fully reconstruct `instructions`. We will use a function `find_functions` for this, such that we can easily halt our search the moment we find the correct combination.

Not all combinations of `A`, `B` and `C` are sensible when trying to find the combination that can reconstruct `instructions`. There are two filters than we can apply to reduce the number of combinations that we need to try significantly, thus reducing runtime.

1. We can say that the deconstructed `instructions` must start with function `A`, since it is initially arbitrary which list slice is stored in which movement function. This must mean that the first character of `instructions` must also be the first character of `A`. Therefore, only list slices that start with the first character in `instructions` are valid candidates for `A`. We cannot say that this also applies to any other characters, since `A` can be one character long.
2. Using the same train of thought, we know that at least one movement function must end with the last character of `instructions`. If `A` already satisfies this condition, then there is nothing to gain. If this not the case, then we can reduce the candidates of either `B` or `C` by limiting either to only candidates that end with the last character of `instructions`. We choose `C`, but it is an arbitrary choice.

We loop over all sensible combinations of `A`, `B` and `C` and check if we can reconstruct `instructions` into the function `reconstruction`. If at any point we have tried to append `A`, `B` and `C`, but none of them would continue the sequence like `instructions` does, then we break out of the loop and try some other combination. If the length of `reconstruction` equals `instructions`, then we have found the correct movement functions. We return the sequence of movement functions, the movement functions themselves, and finally the 'n' instruction to indicate that we do not wish to output any camera feed.

```python
def find_functions(instructions, possible_functions):
    for A in [func for func in possible_functions if func[0] == instructions[0]]:
        for B in possible_functions:
            for C in ([func for func in possible_functions if func[-1] == instructions[-1]] if A[-1] != instructions[-1] else possible_functions):
                reconstruction = []
                main_routine = []
                while len(reconstruction) < len(instructions):
                    len_before_extending = len(reconstruction)
                    for func in [A, B, C]:
                        if tuple(instructions[len(reconstruction):len(reconstruction)+len(func)]) == func:
                            reconstruction.extend(func)
                            main_routine.append({A: 'A', B: 'B', C: 'C'}[func])
                    if len(reconstruction) == len_before_extending:
                        break
                if reconstruction == instructions:
                    return main_routine, A, B, C, 'n'
```

With a function in place to calculate the movement functions, all that remains is to initialize `robot` and run it. We initialize a new `robot` and append the return variables of `find_functions()` to `robot.inputs`. Notice that we ordered the return statements of `find_functions()` in the order that the inputs of `robot` expect. Since numbers over 9 contain more than one unicode character, we must also iterate over the characters inside the instructions themselves, and add the unicode code of each individual character as a new input to `robot`. After each instruction, we add a comma, or a newline if the instruction is the last instruction of the function.

We then calculate steps in `robot` using `robot.calc_step()`, until `robot` return a `status`. The last `out` before returning a `status` is the answer to the second puzzle part.

```python
robot = intcode({**program.copy(), 0: 2}, [])
for func in find_functions(instructions, possible_functions):
    for i_instruction, instruction in enumerate(func, start = 1):
        for char in str(instruction):
            robot.inputs.append(ord(str(char)))
        robot.inputs.append(ord(',' if i_instruction < len(func) else '\n'))
while True:
    out, status = robot.calc_step()
    if out != None:
        last_out = out
    if status != None:
        print(last_out)
        break
```