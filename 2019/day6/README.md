[Link to puzzle](https://adventofcode.com/2019/day/6)
## Import

```python
from pyhelper.pyimport import lines_to_list_of_list
input = lines_to_list_of_list('2019/input/day6_input.txt', seperator = ')')
```

## Solution

We create a dictionary `orbitting` that connects every orbiting planet (key) to the planet that it is orbitting (value). Then, for every planet in `orbitting`, we check if it is orbitting `COM` and if it is not, we add 1 to `count`. We then set the current orbit `cur_orbit` to the planet that is is _actually_ orbitting, and repeat this process until we reach `COM`. We have now added 1 to `count` as many times as the level of indentation of the original planet. If we repeat this process for every planet in `orbitting`, we find the answer to the first question.

```python
orbitting = {orbit[1]: orbit[0] for orbit in input}
count = 0
for orbit in orbitting:
    cur_orbit = orbit
    while cur_orbit != 'COM':
        cur_orbit = orbitting[cur_orbit]
        count += 1
print(count)
```

We create the dictionary `orbitted` that, for every planet (key), saves a dictionary (value) that contains orbitting planets (key) and how many indented orbits this planet is away (value). As an example, suppose we have some planet A, which is being orbitted by some planet B, which itself is being orbitted by some planet C. In this case, `orbitted = {A: {B : 1, C: 2}, B: {C: 1}}`. We construct this dictionary by looping over all planets that do not have an orbitting planet of their own. We then find the planet that it orbits and add the original planet to the `orbitted` entry of the orbitted planet with distance 1. Then we move upwards along the indentation of orbits, until we reach `COM`. At every step, we add 1 to all previous distances.

```python
orbitted = {orbit[1]:{} for orbit in input}
for orbit_start in [orbit for orbit in orbitted.keys() if orbit not in orbitting.values()]:
    dict = {}
    cur_orbit = orbit_start
    while cur_orbit != 'COM':
        for key, value in dict.items():
            if key not in orbitted[cur_orbit].keys():
                orbitted[cur_orbit][key] = value
            dict[key] += 1
        dict[cur_orbit] = 0
        cur_orbit = orbitting[cur_orbit]
```

We make a list of how many orbital transfers it takes to move from `YOU` to `SAN`, for every planet that contains those two value in their `orbitted` dictionary. The answer to the second question is the minimum of this list.

```python
orbital_transfers = [orbit[1]['YOU'] + orbit[1]['SAN'] for orbit in orbitted.items() if 'YOU' in orbit[1] and 'SAN' in orbit[1]]
print(min(orbital_transfers))
```