from pyhelper.pyimport import file_to_str
datastream = file_to_str("2022\input\day6_input.txt")

def calc(num):
    pos = num
    while len(set(datastream[pos - num:pos])) < num:
        pos += 1
    print(pos)

calc(4)

calc(14)