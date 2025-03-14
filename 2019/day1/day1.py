from pyhelper.pyimport import lines_to_list
masses = lines_to_list('2019/input/day1_input.txt', cast = int)

fuel_requirements = [int(mass / 3) - 2 for mass in masses]
print(sum(fuel_requirements))

total_mass = 0
for mass in masses:
    last_fuel_addition = mass
    while last_fuel_addition > 0:
        last_fuel_addition = int(last_fuel_addition / 3) - 2
        total_mass += max(last_fuel_addition, 0)
print(total_mass)