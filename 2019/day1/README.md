[Link to puzzle](https://adventofcode.com/2019/day/1)
## Import

```python
from pyhelper.pyimport import lines_to_list
masses = lines_to_list('2019/input/day1_input.txt', cast = int)
```

## Solution

The answer to the first question is found by calculating the fuel mass requirement per module mass, and summing the results.

For the answer to the second question, we additionally calculate the fuel mass requirement of the mass we just added, and we keep doing this until that mass is negative. Since we only need the mass of all modules combined, we do not have to store the fuel mass requirement per module.

```python
from pyhelpers.pyimports import lines_to_ints

masses = lines_to_ints('2019/input/dec1_input.txt')

fuel_requirements = [int(mass / 3) - 2 for mass in masses]
print(sum(fuel_requirements))

total_mass = 0
for mass in masses:
    last_fuel_addition = mass
    while last_fuel_addition > 0:
        last_fuel_addition = int(last_fuel_addition / 3) - 2
        total_mass += max(last_fuel_addition, 0)
print(total_mass)
```