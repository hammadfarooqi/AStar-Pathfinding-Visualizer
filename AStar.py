import math


def heuristic(a, b, diagonals):
    if diagonals:
        d = math.dist([a.x, a.y], [b.x, b.y])
    else:
        d = abs(a.x - b.x) + abs(a.y - b.y)
    return d


class Node:
    def __init__(self, x, y, wall = False):
        self.x = x
        self.y = y

        self.g = 0
        self.h = 0
        self.f = 0

        self.neighbors = []
        self.parent = 0
        self.wall = wall

    def add_neighbors(self, grid, diagonals = False):
        if self.y > 0:
            self.neighbors.append(grid[self.y - 1][self.x])
        if self.y < len(grid) - 1:
            self.neighbors.append(grid[self.y + 1][self.x])
        if self.x > 0:
            self.neighbors.append(grid[self.y][self.x - 1])
        if self.x < len(grid[self.y]) - 1:
            self.neighbors.append(grid[self.y][self.x + 1])
        if diagonals:
            if self.x > 0 and self.y > 0:
                self.neighbors.append(grid[self.y - 1][self.x-1])
            if self.x > 0 and self.y < len(grid) - 1:
                self.neighbors.append(grid[self.y + 1][self.x - 1])
            if self.x < len(grid[self.y]) - 1 and self.y > 0:
                self.neighbors.append(grid[self.y - 1][self.x + 1])
            if self.x < len(grid[self.y]) - 1 and self.y < len(grid) - 1:
                self.neighbors.append(grid[self.y + 1][self.x + 1])

    def __str__(self):
        return "(" + str(self.x) + " " + str(self.y) + ")" # + str(self.wall)

def find_shortest_path(grid_size, start, end, walls, diagonals=False):
    grid = []

    for i in range(grid_size[1]):
        grid.append([])
        for j in range(grid_size[0]):
            grid[i].append(Node(j, i))

    for row in grid:
        for item in row:
            item.add_neighbors(grid, diagonals)
            for wall in walls:
                if wall[0] == item.x and wall[1] == item.y:
                    item.wall = True

    start = grid[start[1]][start[0]]
    end = grid[end[1]][end[0]]

    open_set = []
    closed_set = []

    open_set.append(start)

    while len(open_set) > 0:
        winner_index = 0
        for i in range(len(open_set)):
            if open_set[i].f < open_set[winner_index].f:
                winner_index = i

        current = open_set[winner_index]

        if current == end:
            path = []
            temp = current
            path.append(temp)
            while temp.parent:
                path.insert(0, temp.parent)
                temp = temp.parent
            path_coordinates = []
            for item in path:
                path_coordinates.append((item.x, item.y))
            return path_coordinates

        closed_set.append(current)
        open_set.remove(current)

        for neighbor in current.neighbors:
            if neighbor not in closed_set and not neighbor.wall:
                temp_g = current.g + 1

                new_path = False
                if neighbor in open_set:
                    if temp_g < neighbor.g:
                        new_path = True
                else:
                    new_path = True
                    open_set.append(neighbor)

                if new_path:
                    neighbor.h = heuristic(neighbor, end, diagonals)
                    neighbor.g = temp_g
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current

    path = []
    temp = current
    path.append(temp)
    while temp.parent:
        path.insert(0, temp.parent)
        temp = temp.parent
    path_coordinates = []
    for item in path:
        path_coordinates.append((item.x, item.y))
    return path_coordinates
    # return None