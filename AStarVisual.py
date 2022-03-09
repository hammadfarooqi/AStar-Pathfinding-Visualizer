import pygame
from pygame.locals import *
from AStar import heuristic, Node
import sys

GRID_SIZE = (48, 24)
NODE_SIZE = 20
NODE_EDGE = 1

"""
Node Type Guide:
0: Nothing, Light Grey
1: Start, Blue
2: End, Green
3: Wall, Red

Pathing nodes
4: Current, Yellow
5: Path, Orange
6: Closed Set, Pink
"""
COLORS = {0: (2,48,85), 1: (29, 215, 251), 2: (177, 242, 177), 3: (69,217,192), 4: (255, 255, 150), 5: (2,159,218), 6: (5,82,140)}

def find_shortest_path(screen, visual_grid, is_selected, real_mouse, clock, diagonals=False):
    grid = []

    for y, row in enumerate(visual_grid):
        grid.append([])
        for x, element in enumerate(row):
            grid[y].append(Node(x, y, element == 3))
            if element == 1:
                start = grid[y][x]
            elif element == 2:
                end = grid[y][x]
            elif element != 3:
                visual_grid[y][x] = 0

    for row in grid:
        for element in row:
            element.add_neighbors(grid, diagonals)

    open_set = []
    closed_set = []

    open_set.append(start)
    # for row in grid:
    #     print("")
    #     for element in row:
    #         print(element, end = "")
    while len(open_set) > 0:
        winner_index = 0
        for i in range(len(open_set)):
            if open_set[i].f < open_set[winner_index].f:
                winner_index = i

        current = open_set[winner_index]
        if visual_grid[current.y][current.x] != 1 and visual_grid[current.y][current.x] != 2:
            visual_grid[current.y][current.x] = 4
        
        #drawing progress right here
        clock.tick(40)


        #THIS SHIT SOMEHOW CAUSES THE ALORITHM TO RUN NONSTOP, WHY?!?!?!
        # for event in pygame.event.get(): #ONLY RUNS IF AN EVENT HAS OCCURRED
        # #     #Making X button work
        #     if event.type == QUIT:
        #         pygame.quit()
        #         sys.exit()

        draw(screen, visual_grid, is_selected, real_mouse)

        if current == end:

            path = []
            temp = current
            path.append(temp)
            if visual_grid[current.y][current.x] != 1 and visual_grid[current.y][current.x] != 2:
                visual_grid[temp.y][temp.x] = 5
            while temp.parent:
                draw(screen, visual_grid, is_selected, real_mouse)
                path.insert(0, temp.parent)
                if visual_grid[temp.parent.y][temp.parent.x] != 1 and visual_grid[temp.parent.y][temp.parent.x] != 2:
                    visual_grid[temp.parent.y][temp.parent.x] = 5
                temp = temp.parent
            # path_coordinates = []
            # for item in path:
            #     path_coordinates.append((item.x, item.y))
            # for element in path:
            #     print(element)
            return visual_grid

        closed_set.append(current)
        if visual_grid[current.y][current.x] != 1 and visual_grid[current.y][current.x] != 2:
            visual_grid[current.y][current.x] = 6
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

    return visual_grid

def draw(screen, grid, is_selected, real_mouse):
    screen.fill((80, 80, 80))
    for x,row in enumerate(grid):
        for y,element in enumerate(row):
            if element in COLORS:
                color = COLORS[element]
                # if element in is_selected and is_selected[element]:
                #     color = (0, 0, 0)
            else:
                color = (0, 0, 0)
            pygame.draw.rect(screen, color, (x*NODE_SIZE+NODE_EDGE, y*NODE_SIZE+NODE_EDGE, NODE_SIZE - 2 * NODE_EDGE, NODE_SIZE - 2 * NODE_EDGE))
        for key in is_selected:
            if is_selected[key]:
                color = COLORS[key]
                pygame.draw.rect(screen, color, (real_mouse[0] - NODE_SIZE//2, real_mouse[1] - NODE_SIZE//2, NODE_SIZE - 2 * NODE_EDGE, NODE_SIZE - 2 * NODE_EDGE))
    pygame.display.update()

if __name__ == '__main__':
    #Essential pygame initializations
    pygame.init()
    clock = pygame.time.Clock()
    node_screen = pygame.display.set_mode(size = (GRID_SIZE[0]*NODE_SIZE, GRID_SIZE[1]*NODE_SIZE))
    pygame.display.set_caption("A* Pathfinding Visualizer")
    pygame.display.set_icon(pygame.image.load('PathFindingIcon.png').convert_alpha())

    #Creating the initial grid
    grid = []
    for x in range(GRID_SIZE[0]):
        grid.append([])
        for y in range(GRID_SIZE[1]):
            grid[x].append(0)

    grid[0][0] = 1 #Initially adds the start node in the top left
    grid[GRID_SIZE[0]-1][GRID_SIZE[1]-1] = 2 #Initially adds end node in the bottom right

    keys = {K_SPACE:False, K_BACKSPACE:False, K_DELETE:False, K_RETURN:False}
    is_selected = {1: False, 2: False}

    mouse_pressed = False
    mouse_released = False
        

    while True:

        #Getting mouse status
        real_mouse = pygame.mouse.get_pos()
        mouse = (real_mouse[0]//NODE_SIZE, real_mouse[1]//NODE_SIZE)

        #Getting events
        for event in pygame.event.get(): #ONLY RUNS IF AN EVENT HAS OCCURRED
            
            #Making X button work
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            #Checking if they just clicked the mouse
            if event.type == MOUSEBUTTONDOWN:
                mouse_pressed = True
            if event.type == MOUSEBUTTONUP:
                mouse_released = True

            #Check the states of all the important keys
            if event.type == KEYDOWN:
                for key in keys:
                    if event.key == key:
                        keys[key] = True
            if event.type == KEYUP:
                for key in keys:
                    if event.key == key:
                        keys[key] = False
        
        
        #Checks if the player selected or released any of the selectable nodes
        if mouse_pressed and mouse_released:
            mouse_pressed = False
            mouse_released = False
            if True in is_selected.values():    
                for key in is_selected:
                    if is_selected[key]:
                        grid[mouse[0]][mouse[1]] = key
                        is_selected[key] = False
            else:
                for key in is_selected:
                    if grid[mouse[0]][mouse[1]] == key:
                        grid[mouse[0]][mouse[1]] = 0
                        is_selected[key] = True
        
        #Check if the player is drawing wall nodes
        if keys[K_SPACE] and grid[mouse[0]][mouse[1]] != 1 and grid[mouse[0]][mouse[1]] != 2:
            grid[mouse[0]][mouse[1]] = 3
        #Checks if the player is removing wall nodes
        if (keys[K_BACKSPACE] or keys[K_DELETE]) and grid[mouse[0]][mouse[1]] == 3:
            grid[mouse[0]][mouse[1]] = 0

        #Check if the player is requesting a path
        if keys[K_RETURN] and not True in is_selected.values():
            grid = find_shortest_path(node_screen, grid, is_selected, real_mouse, clock)

        draw(node_screen, grid, is_selected, real_mouse)