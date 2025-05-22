def breadth_first_search(map: set[complex], pos_from: complex, pos_to: complex):
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

def dijkstra(pos_start: any, pos_end: any, connected_nodes: dict[any, set[tuple[any, int]]]) -> tuple[complex, int, list[list]]:
    nodes_to_check = {pos_start: [0, [[]]]}
    nodes_checked = set()
    while len(nodes_to_check) > 0:
        pos, (total_cost, routes) = min(nodes_to_check.items(), key = lambda x: x[1][0])
        if (type(pos_end) in (list, tuple, set) and pos in pos_end) or pos == pos_end:
            return pos, total_cost, [route + [pos] for route in routes]
        for node, cost in connected_nodes[pos]:
            if node not in nodes_checked:
                if node not in nodes_to_check or nodes_to_check[node][0] > total_cost + cost:
                    nodes_to_check[node] = [total_cost + cost, [route + [pos] for route in routes]]
                elif nodes_to_check[node][0] == total_cost + cost:
                    nodes_to_check[node][1].extend(route + [pos] for route in routes)
        nodes_checked.add(pos)
        nodes_to_check.pop(pos)
    return tuple()