import numpy as np

map = np.array([list(map(int,(line))) for line in np.loadtxt('2024/input/day10_input.txt', dtype = str, comments = None)])

# part 1
score = 0
for y in range(len(map)):
    for x in range(len(map)):
        if map[y][x] == 0:
            trailheads = []
            neighbors = [[0, x, y]]
            while len(neighbors) > 0:
                dirs = []
                if neighbors[0][1] > 0:
                    dirs.append([-1, 0])
                if neighbors[0][1] < len(map[0]) - 1:
                    dirs.append([1, 0])
                if neighbors[0][2] > 0:
                    dirs.append([0, -1])
                if neighbors[0][2] < len(map) - 1:
                    dirs.append([0, 1])
                new_neighbors = []
                for dir in dirs:
                    if map[neighbors[0][2] + dir[1]][neighbors[0][1] + dir[0]] == neighbors[0][0] + 1:
                        new_neighbors.append([neighbors[0][0] + 1, neighbors[0][1] + dir[0], neighbors[0][2] + dir[1]])
                for new_neighbor in new_neighbors:
                    if new_neighbor[0] == 9:
                        trailheads.append(new_neighbor)
                    else:
                        neighbors.append(new_neighbor)
                neighbors.pop(0)
            score += len(np.unique(np.array(trailheads), axis = 0))
print('answ1: ' + str(score))

# part 2
score = 0
for y in range(len(map)):
    for x in range(len(map)):
        if map[y][x] == 0:
            trailheads = []
            neighbors = [[0, x, y]]
            while len(neighbors) > 0:
                dirs = []
                if neighbors[0][1] > 0:
                    dirs.append([-1, 0])
                if neighbors[0][1] < len(map[0]) - 1:
                    dirs.append([1, 0])
                if neighbors[0][2] > 0:
                    dirs.append([0, -1])
                if neighbors[0][2] < len(map) - 1:
                    dirs.append([0, 1])
                new_neighbors = []
                for dir in dirs:
                    if map[neighbors[0][2] + dir[1]][neighbors[0][1] + dir[0]] == neighbors[0][0] + 1:
                        new_neighbors.append([neighbors[0][0] + 1, neighbors[0][1] + dir[0], neighbors[0][2] + dir[1]])
                for new_neighbor in new_neighbors:
                    if new_neighbor[0] == 9:
                        score += 1
                    else:
                        neighbors.append(new_neighbor)
                neighbors.pop(0)
print('answ2: ' + str(score))