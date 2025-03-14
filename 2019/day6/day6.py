from pyhelper.pyimport import lines_to_list_of_list
input = lines_to_list_of_list('2019/input/day6_input.txt', seperator = ')')

orbitting = {orbit[1]: orbit[0] for orbit in input}
count = 0
for orbit in orbitting:
    cur_orbit = orbit
    while cur_orbit != 'COM':
        cur_orbit = orbitting[cur_orbit]
        count += 1
print(count)

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
orbital_transfers = [orbit[1]['YOU'] + orbit[1]['SAN'] for orbit in orbitted.items() if 'YOU' in orbit[1] and 'SAN' in orbit[1]]
print(min(orbital_transfers))