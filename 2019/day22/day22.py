from pyhelper.pyimport import lines_to_list
from collections import deque
instructions = lines_to_list('2019/input/day22_input.txt')

def calc_shuffles(deck):
    deck_len = len(deck)
    for instruction in instructions:
        if instruction == 'deal into new stack':
            deck.reverse()
        elif instruction[:3] == 'cut':
            deck.rotate(-1 * int(instruction[4:]))
        elif instruction[:19] == 'deal with increment':
            increment = int(instruction[20:])
            new_deck = deque([None] * deck_len)
            for i in range(deck_len):
                new_deck[(i * increment) % deck_len] = deck[i]
            deck = new_deck
    return deck

deck = calc_shuffles(deque(list(range(10007))))
for i_card, card in enumerate(deck):
    if card == 2019:
        print(i_card)