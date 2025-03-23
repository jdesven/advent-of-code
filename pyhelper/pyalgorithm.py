def breadth_first_search(map: set, pos_from: complex, pos_to: complex):
    paths = [[pos_from]]
    pos_seen = set([pos_from])
    while len(paths) > 0:
        paths_next = []
        for path in paths:
            for dir in (-1j, 1j, -1, 1):
                next_pos = path[-1] + dir
                if next_pos in map and next_pos not in pos_seen:
                    if next_pos == pos_to:
                        return path + [next_pos]
                    paths_next.append(path + [next_pos])
                    pos_seen.add(next_pos)
        paths = paths_next
    return []