import re

with open('2024/input/day17_input.txt', 'r') as file:
    register_str, program_str = file.read().split('\n\n')
reg_a, reg_b, reg_c = [int(num) for num in re.sub('[^0-9\n]','',register_str).splitlines()]
program = [int(num) for num in re.sub('[^0-9,]','',program_str).split(',')]
        
def calc_output(reg_a, reg_b, reg_c, program):
    def get_combo_operand(operand):
        match operand:
            case 4:
                return reg_a
            case 5:
                return reg_b
            case 6:
                return reg_c
            case _:
                return operand
            
    pointer = 0
    output = []
    while pointer < len(program):
        match program[pointer]:
            case 0:
                reg_a = int(reg_a / (2 ** get_combo_operand(program[pointer + 1])))
            case 1:
                reg_b = program[pointer + 1] ^ reg_b
            case 2:
                reg_b = get_combo_operand(program[pointer + 1]) % 8
            case 4:
                reg_b = int(reg_b ^ reg_c)
            case 5:
                output.append(get_combo_operand(program[pointer + 1]) % 8)
            case 6:
                reg_b = int(reg_a / (2 ** get_combo_operand(program[pointer + 1])))
            case 7:
                reg_c = int(reg_a / (2 ** get_combo_operand(program[pointer + 1])))
        if program[pointer] == 3 and reg_a != 0:
            pointer = program[pointer + 1]
        else:
            pointer += 2
    return output

# part 1
print('ans1: ' + ','.join([str(num) for num in calc_output(reg_a, reg_b, reg_c, program)]))