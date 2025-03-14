import numpy as np

with open('2024/input/day9_input.txt', 'r') as file:
    txt = np.array([int(num) for num in file.read()])

# part 1
txt_extended = []
for i in range(len(txt[0::2])):
    for j in range(txt[0::2][i]):
        txt_extended.append(i)

correct_order = []
i_txt = 0
i_extended_front = 0
i_extended_back = len(txt_extended) - 1
while len(correct_order) < len(txt_extended):
    for j in range(txt[i_txt]):
        correct_order.append(txt_extended[i_extended_front])
        i_extended_front += 1
    i_txt += 1
    for j in range(txt[i_txt]):
        correct_order.append(txt_extended[i_extended_back])
        i_extended_back -= 1
    i_txt += 1
correct_order = correct_order[:len(txt_extended)]

sum = 0
for i, num in enumerate(correct_order):
    sum += i * num
print('ans1: ' + str(sum))

# part 2
txt_extended = []
for i in range(len(txt[0::2])):
    for j in range(txt[0::2][i]):
        txt_extended.append(i)
    if i < len(txt[1::2]):
        for j in range(txt[1::2][i]):
            txt_extended.append('.')

i_backwards = len(txt_extended) - 1
while i_backwards > 0:
    if txt_extended[i_backwards] != '.':
        current_num = txt_extended[i_backwards]
        chunk_size = 1
        while txt_extended[i_backwards - chunk_size] == current_num:
            chunk_size += 1
        found_suitable_location = False
        i_empty = 0
        empty_size = 0
        while found_suitable_location == False and i_empty < len(txt_extended):
            if txt_extended[i_empty] == '.':
                empty_size += 1
            else:
                empty_size = 0
            if empty_size == chunk_size:
                found_suitable_location = True
            else:
                i_empty += 1
        if found_suitable_location == True and i_empty < i_backwards:
            for i_rel_chunk in range(chunk_size):
                txt_extended[i_backwards - i_rel_chunk] = '.'
            for i_rel_empty in range(chunk_size):
                txt_extended[i_empty - i_rel_empty] = current_num
        # correct i
        i_backwards -= chunk_size
    else:
        i_backwards -= 1

sum = 0
for i in range(len(txt_extended)):
    if txt_extended[i] != '.':
        sum += i * txt_extended[i]
print('ans2: ' + str(sum))