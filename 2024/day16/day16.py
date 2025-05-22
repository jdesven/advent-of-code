from pyhelper.pyimport import grid_to_dict
from pyhelper.pyalgorithm import dijkstra

input = grid_to_dict('2024/input/day16_input.txt', relevant_chars = ('.', 'S', 'E'))
pos_start = next(pos for pos, val in input.items() if val == 'S')
pos_end = next(pos for pos, val in input.items() if val == 'E')
grid = set(input.keys())
nodes = set([pos for pos in grid if [pos + dir in grid for dir in (-1, 1, -1j, 1j)] not in ([True, True, False, False], [False, False, True, True])] + [pos_start, pos_end])
connected_nodes = {}
unchecked_nodes = [(pos_start, 1)]
while len(unchecked_nodes) > 0:
    pos, dir = unchecked_nodes.pop(0)
    connected_nodes[(pos, dir)] = set()
    if pos + dir in grid:
        steps = next(step for step in range(1, 1000) if pos + step * dir in nodes)
        unchecked_node = (pos + steps * dir, dir)
        connected_nodes[(pos, dir)].add((unchecked_node, steps))
        if unchecked_node not in connected_nodes.keys() and unchecked_node not in connected_nodes.keys():
            unchecked_nodes.append(unchecked_node)
            connected_nodes[unchecked_node] = set()
    for dir_new in [dir * -1j, dir * 1j]:
        if pos + dir_new in grid:
            unchecked_node = (pos, dir_new)
            connected_nodes[(pos, dir)].add((unchecked_node, 1000))
            if unchecked_node not in connected_nodes.keys() and unchecked_node not in connected_nodes.keys():
                unchecked_nodes.append(unchecked_node)
                connected_nodes[unchecked_node] = set()
pos, cost, routes = dijkstra((pos_start, 1), [(pos_end, dir) for dir in (-1, 1, -1j, 1j)], connected_nodes)
print(cost)

tiles_on_best_paths = set()
for route in routes:
    for node_from, node_to in zip(route, route[1:]):
        dist = int(abs(node_from[0].real - node_to[0].real)) + int(abs(node_from[0].imag - node_to[0].imag))
        if dist > 0:
            dir = int(node_to[0].real - node_from[0].real) // dist + int(node_to[0].imag - node_from[0].imag) // dist * 1j
            tiles_on_best_paths.update(node_from[0] + step * dir for step in range(dist + 1))
print(len(tiles_on_best_paths))