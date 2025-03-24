from pyhelper.pyimport import seperator_to_list
register_str, program_str = seperator_to_list('2024/input/day17_input.txt', seperator = '\n\n')
reg_a, reg_b, reg_c = seperator_to_list(register_str, seperator = '\n', cast = int, read_file = False, regex = '[0-9\n]')
program = seperator_to_list(program_str, seperator = ',', cast = int, read_file = False, regex = '[0-9,]')
        
def calc_output(reg_a, reg_b, reg_c, program):
    def get_combo_operand(operand):
        return {4: reg_a, 5: reg_b, 6: reg_c}[operand] if operand in (4, 5, 6) else operand
            
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

print(','.join([str(num) for num in calc_output(reg_a, reg_b, reg_c, program)]))