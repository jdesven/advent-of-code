import re

with open('2024/input/day13_input.txt', 'r') as file:
    txt = file.read().splitlines()
button_a = [[int(row.split(',')[0]), int(row.split(',')[1])] for row in [re.sub(r'[^0-9,]','',row) for row in txt[0::4]]]
button_b = [[int(row.split(',')[0]), int(row.split(',')[1])] for row in [re.sub(r'[^0-9,]','',row) for row in txt[1::4]]]
prizes = [[int(row.split(',')[0]), int(row.split(',')[1])] for row in [re.sub(r'[^0-9,]','',row) for row in txt[2::4]]]

def calc_tokens(button_a, button_b, prizes):
    tokens = 0
    for i in range(len(prizes)):
        det_A = button_a[i][0] * button_b[i][1] - button_b[i][0] * button_a[i][1]
        det_A1 = prizes[i][0] * button_b[i][1] - button_b[i][0] * prizes[i][1]
        det_A2 = button_a[i][0] * prizes[i][1] - prizes[i][0] * button_a[i][1]
        if det_A1 % det_A == 0 and det_A2 % det_A == 0:
            tokens += 3 * int(det_A1 / det_A) + int(det_A2 / det_A)
    return tokens
print(calc_tokens(button_a, button_b, prizes))

prizes_translated = [[num + 1e13 for num in prize] for prize in prizes]
print(calc_tokens(button_a, button_b, prizes_translated))