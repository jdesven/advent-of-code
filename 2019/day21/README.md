[Link to puzzle](https://adventofcode.com/2019/day/17)\
[Link to Intcode](https://github.com/jdesven/advent-of-code/tree/main/2019/intcode)

## Import

```python
from pyhelper.pyimport import seperator_to_list_to_dict
from importlib import import_module
program = seperator_to_list_to_dict('2019/input/day21_input.txt', seperator = ',', cast = int)
intcode = getattr(import_module('2019.intcode.intcode'), 'intcode')
```

## Calculation

The set of instructions is converted to ASCII integers using `ord()`, and then stored in the input list of the springdroid. We then run the springdroid until it return a status, which indicates that the springdroid has completed its mission. The springdroid reports the amount of hull damage in the last output before returning a status. This is the answer to the puzzle.

```python
def run(instructions):
    springdroid = intcode(program.copy(), [])
    for instruction in instructions:
        for char in instruction:
            springdroid.inputs.append(ord(char))
        springdroid.inputs.append(ord('\n'))
    status = None
    while status == None:
        out, status = springdroid.calc_step()
        if out != None:
            last_out = out
    print(last_out)
```

## Solutions

The jumping distance of the springdroid is four spaces. The best course of action is to jump if `A`, `B` or `C` is a hole. This ensures that the springdroid jumps as early as possible. Jumping as early is possible is a good idea, because if it doesn't, the springdroid might miss its only chance of jumping over a hole. Take for example the situation `###.#...#`. The springdroid _must_ jump while standing on the first position, because jumping in any other position results in falling in a hole. The only exception to this rule is when the `D` position is also a hole. In that case the droid would fall into a hole when it would jump, so if this condition holds true then the droid will never jump. As a list of instructions, these rules can be written as:

1. Jump if `A`, `B` or `C` is a hole [...]
    1. `NOT A J`
    2. `NOT B T`
    3. `OR T J`
    4. `NOT C T`
    5. `OR T J`
2. [...] except if `D` is also a hole.
    1. `AND D J`
3. WALK

```python
run(['NOT A J', 'NOT B T', 'OR T J', 'NOT C T', 'OR T J', 'AND D J', 'WALK'])
```

In part two of the puzzle, the robot can see up to 9 tiles away. There is a situation where the instructions of part one of the puzzle will still fail. Namely, if the springdroid jumps, lands on `D`, and sees that `E` is also a hole, then it must always jump immediately again. However, if `H` is also a hole, then the springdroid will land in a hole. In part one, it was impossible to account for this situation, since we could only see up to four positions away. Now that our vision is extended to up to nine tiles, we add the extra rule that the droid will not jump if both `E` and `H` are holes

1. Jump if `A`, `B` or `C` is a hole [...]
    1. `NOT A J`
    2. `NOT B T`
    3. `OR T J`
    4. `NOT C T`
    5. `OR T J`
2. [...] except if `D` is also a hole [...]
    1. `AND D J`
3. [...] or if both `E` and `H` are holes.
    1. `NoT T T`
    2. `OR E T`
    3. `OR H T`
    4. `AND T J` 
4. RUN

```python
run(['NOT A J', 'NOT B T', 'OR T J', 'NOT C T', 'OR T J', 'AND D J', 'NOT T T', 'OR E T', 'OR H T', 'AND T J','RUN'])
```