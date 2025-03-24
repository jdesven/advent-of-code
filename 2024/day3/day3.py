import re
from pyhelper.pyimport import file_to_str

txt = file_to_str('2024\input\day3_input.txt')

sum = 0
for mul in re.finditer('mul\(\d{1,3},\d{1,3}\)', txt):
    num = re.findall('\d{1,3}', mul.group())
    sum += int(num[0]) * int(num[1])
print(sum)

do_locations = []
for match in re.finditer('do()', txt):
    do_locations.append(match.start())
dont_locations = []
for match in re.finditer('don\'t()', txt):
    dont_locations.append(match.start())
sum = 0
for mul in re.finditer('mul\(\d{1,3},\d{1,3}\)', txt):
    previous_do = [x for x in do_locations if x < mul.start()]
    previous_dont = [x for x in dont_locations if x < mul.start()]
    if len(previous_dont) == 0 or max(previous_do) > max(previous_dont):
        num = re.findall('\d{1,3}', mul.group())
        sum += int(num[0]) * int(num[1])
print(sum)