import re
from pyhelper.pyimport import seperator_to_list, lines_to_list
init_stacks_str, cmds_str = seperator_to_list("2022\input\day5_input.txt", seperator = '\n\n')

init_stacks_rows = lines_to_list(init_stacks_str, read_file = False)
init_stacks = [[] for _ in range((len(init_stacks_rows[0]) + 1) // 4)]
for line in reversed(init_stacks_rows[:-1]):
    for i_char, char in enumerate(line):
        if char not in (' ', '[', ']'):
            init_stacks[(i_char - 1) // 4].append(char)
cmds = [[int(char) for char in re.findall(r"\d+", line)] for line in lines_to_list(cmds_str, read_file = False)]

def calc(part):
    stacks = [row.copy() for row in init_stacks]
    for times, start, end in cmds:
        stacks[end - 1].extend(reversed(stacks[start - 1][-times:]) if part == 1 else stacks[start - 1][-times:])
        del stacks[start - 1][-times:]
    print(''.join(stack[-1] for stack in stacks))

calc(1)
calc(2)