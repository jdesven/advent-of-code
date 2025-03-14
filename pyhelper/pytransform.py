def coord_dict_to_nested_list(input_dict: dict, empty_char):
    nested_list = []
    for y in range(min([int(num.imag) for num in input_dict.keys()]), max([int(num.imag) for num in input_dict.keys()]) + 1):
        x_range = range(min([int(num.real) for num in input_dict.keys()]), max([int(num.real) for num in input_dict.keys()]) + 1)
        row = [input_dict[x + y*1j] if (x + y*1j) in input_dict else empty_char for x in x_range]
        nested_list.append(row)
    return nested_list