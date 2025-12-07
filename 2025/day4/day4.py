from pyhelper.pyimport import grid_to_complex_set
coords = grid_to_complex_set("2025\input\day4_input.txt", {'@'})

print(sum(sum(pos + x + y in coords for x in (-1,0,1) for y in (-1j,0,1j)) <= 4 for pos in coords))

removed = set()
changed = True
while changed:
    changed = False
    for pos in coords - removed:
        if sum((pos + x + y) in coords and (pos + x + y) not in removed for x in (-1,0,1) for y in (-1j,0,1j)) <= 4:
            removed.add(pos)
            changed = True
print(len(removed))