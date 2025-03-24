from pyhelper.pyimport import seperator_to_list
txt = seperator_to_list('2024/input/day9_input.txt', cast = int)

def calc_txt_full(txt):
    txt_full = []
    for i, num in enumerate(txt):
        if i % 2 == 0:
            txt_full.extend([int(i / 2)] * num)
        else:
            txt_full.extend(['.'] * num)
    return txt_full

txt_full = calc_txt_full(txt)
ptr_empty = 0
ptr_move = len(txt_full) - 1
while ptr_move > ptr_empty:
    if txt_full[ptr_move] != '.':
        while txt_full[ptr_empty] != '.':
            ptr_empty += 1
        if ptr_move > ptr_empty:
            txt_full[ptr_empty] = txt_full[ptr_move]
            txt_full[ptr_move] = '.'
    ptr_move -= 1
print(sum(i * num for i, num in enumerate(txt_full) if num != '.'))

txt_full = calc_txt_full(txt)
for ptr_move in range(len(txt_full) - 1, 0, -1):
    if txt_full[ptr_move] != '.' and txt_full[ptr_move] != txt_full[ptr_move - 1]:
        size_move = txt_full.count(txt_full[ptr_move])
        for ptr_empty in range(ptr_move):
            if txt_full[ptr_empty] == '.' and txt_full[ptr_empty - 1] != '.':
                size_empty = next((i for i in range(ptr_empty, len(txt_full)) if isinstance(txt_full[i + 1], int)), -1) - ptr_empty + 1
                if size_empty >= size_move:
                    txt_full[ptr_empty:ptr_empty + size_move] = txt_full[ptr_move:ptr_move + size_move]
                    txt_full[ptr_move:ptr_move + size_move] = ['.'] * size_move
                    break
print(sum(i * num for i, num in enumerate(txt_full) if num != '.'))