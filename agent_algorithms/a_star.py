import heapq
import copy
import numpy as np
from agent_algorithms.grid_node import Node



def pos_update(agent, environment, setup):
    if agent.step_no is None:
        return(0,0)
    no_steps = int(setup.step_size*setup.grid_fineness)
    #print(no_steps)
    agent.step_no+=no_steps
    #print(agent.step_no)
    if agent.step_no >= len(agent.path):
        agent.step_no = len(agent.path)-1
    #print("Index updated: "+str(agent.step_no))
    #print(agent.path[agent.step_no][0],", ",+agent.path[agent.step_no][1])
    #print("" + str((agent.path[agent.step_no][0]/setup.grid_fineness, agent.path[agent.step_no][0]/setup.grid_fineness))+ "")
    return agent.path[agent.step_no][0]/setup.grid_fineness, agent.path[agent.step_no][1]/setup.grid_fineness

def euclidean_distance(x1, y1, x2, y2):
    """ Compute Euclidean distance as the heuristic. """
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def is_valid(x, y, grid):
    """
        Checks if (x, y) is within bounds and is not an obstacle.
        :param x: x-coordinate
        :param y: y-coordinate
        :param grid: 2D list of obstacles
    """
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[int(x)][int(y)] == 0:
        return True
    return False

def get_neighbors(node, grid):
    """ Returns valid neighbors for the given node. """
    # Possible moves: up, down, left, right, diagonal
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1),
             (-1, -1), (-1, 1), (1, -1), (1, 1)]

    neighbors = []
    if node is None:
        return neighbors
    for dx, dy in moves:
        nx, ny = node.x + dx, node.y + dy
        if is_valid(nx, ny, grid):
            cost = 1 if dx == 0 or dy == 0 else np.sqrt(2)  # Diagonal cost
            neighbors.append(Node(nx, ny, node.g + cost, 0, node))
    return neighbors


def initialize_path(agent, environment, setup):
    """
    Computes the A* algorithm for the given agent and environment.
    :param agent:
    :param environment:
    :param setup:
    :return:
    """
    pos_list = []
    grid = copy.deepcopy(environment.grid)
    pos_list.append((agent.x, agent.y))
    grid[int(agent.x * setup.grid_fineness)][int(agent.y * setup.grid_fineness)] = 1

    goal = (int(environment.target_x * setup.grid_fineness), int(environment.target_y * setup.grid_fineness))
    current = (int(agent.x * setup.grid_fineness),int(agent.y * setup.grid_fineness))

    open_list = []
    closed_list = []
    heapq.heappush(open_list, Node(current[0], current[1], 0, euclidean_distance(*current, *goal)))
    came_from = {}

    while open_list:
        current_node = heapq.heappop(open_list)
        #print(current_node.x, current_node.y)
        closed_list.append((current_node.x, current_node.y))

        if (current_node.x, current_node.y) == goal:
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            agent.set_path(path[::-1])
            #print("Path computed: "+str(path[::-1]))
            return

        for neighbor in get_neighbors(current_node, grid):
            if (neighbor.x, neighbor.y) in closed_list:
                continue

            if (neighbor.x, neighbor.y) not in came_from or neighbor.g < came_from[(neighbor.x, neighbor.y)].g:
                came_from[(neighbor.x, neighbor.y)] = neighbor
                heapq.heappush(open_list, Node(neighbor.x, neighbor.y, neighbor.g,
                                               euclidean_distance(neighbor.x, neighbor.y, *goal), current_node))



