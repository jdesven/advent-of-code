from math import gcd, atan2, pi
from pyhelper.pyimport import grid_to_complex_set
asteroids = grid_to_complex_set('2019/input/day10_input.txt', {'#'})

detectable = {}
for station in asteroids:
    vectors_gcd = set()
    for asteroid in [pos for pos in asteroids if pos != station]:
        vector = asteroid - station
        vectors_gcd.add(vector / gcd(int(vector.real), int(vector.imag)))
    detectable[station] = len(vectors_gcd)
print(max(detectable.values()))

station = max(detectable, key=detectable.get)
asteroids_per_gcd = {}
for asteroid in [pos for pos in asteroids if pos != station]:
    vector = asteroid - station
    vector_gcd = vector / gcd(int(vector.real), int(vector.imag))
    if vector_gcd in asteroids_per_gcd:
        asteroids_per_gcd[vector_gcd].add(vector)
    else:
        asteroids_per_gcd[vector_gcd] = set([vector])
for vector_gcd in asteroids_per_gcd:
    asteroids_per_gcd[vector_gcd] = sorted(asteroids_per_gcd[vector_gcd], key=lambda x: x.real)
sorted_gcd = sorted(asteroids_per_gcd.keys(), key=lambda point: -atan2(int(point.real), int(point.imag)))
vaporized = []
times_rotated = 0
i_rotation = 0
while len(vaporized) < 200:
    if len(asteroids_per_gcd[sorted_gcd[i_rotation]]) > times_rotated:
        vaporized.append(asteroids_per_gcd[sorted_gcd[i_rotation]][times_rotated])
    if i_rotation < len(sorted_gcd) - 1:
        i_rotation += 1
    else:
        i_rotation = 0
        times_rotated += 1
print(int((vaporized[199] + station).real) * 100 + int((vaporized[199] + station).imag))