from pyhelper.pyimport import lines_to_list
inputs = [(line[0], int(line[2:])) for line in lines_to_list("2022\input\day9_input.txt")]

def calc(num):
    seen, pos = {0j}, [0j]*num
    for letter, amt in inputs:
        for _ in range(amt):
            pos[0] += {'L': -1 + 0j, 'U': -1j, 'R': 1 + 0j, 'D': 1j}[letter]
            for i in range(num - 1):
                diff = pos[i] - pos[i + 1]
                if abs(diff) > 2**0.5:
                    pos[i+1] += complex((diff.real > 0) - (diff.real < 0), (diff.imag > 0) - (diff.imag < 0))
            seen.add(pos[-1])
    print(len(seen))

calc(2)
calc(10)