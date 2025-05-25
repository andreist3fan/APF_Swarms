"""
This file implements a rudimentary A* pathfinding algorithm for an agent in a grid-based environment.
It includes functions to update the agent's position, compute distances, validate positions, and find neighbors.

The A* algorithm is used to compute a path from the agent's current position to a target position, avoiding obstacles in the grid.
The heuristic used is the Euclidean distance in this case.

Furthermore, while the actual grid is continuous, this code assumes a discretized grid where each cell is represented by an integer coordinate.
This parameter can be tuned by adjusting the `grid_fineness` in the setup.
"""

import heapq
import copy
import numpy as np
from agent_algorithms.grid_node import Node



def pos_update(agent, environment, setup):
    if agent.step_no is None:
        return(0,0)
    
    # Take a number of steps according to the step size and grid fineness
    no_steps = int(setup.step_size*setup.grid_fineness)
    
    # Update the agent's step number
    agent.step_no+=no_steps
    
    # Check if the agent has reached the end of the path
    if agent.step_no >= len(agent.path):
        # If so, set the agent's position to the target
        agent.step_no = len(agent.path)-1
    
    return agent.path[agent.step_no][0]/setup.grid_fineness, agent.path[agent.step_no][1]/setup.grid_fineness

def euclidean_distance(x1, y1, x2, y2):
    """ 
        Compute Euclidean distance as the heuristic.
        Args:
            x1: x-coordinate of first point
            y1: y-coordinate of first point
            x2: x-coordinate of second point
            y2: y-coordinate of second point
        Returns: Euclidean distance between the two points 
    """
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def is_valid(x, y, grid):
    """
        Checks if (x, y) is within bounds and is not an obstacle.
        Args:
            x: x-coordinate
            y: y-coordinate
            grid: 2D grid representing the environment
        Returns: True if valid, False otherwise
    """
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[int(x)][int(y)] == 0:
        return True
    return False

def get_neighbors(node, grid):
    """ 
    Returns valid neighbors for the given node.
    Args:
        node: Node object
        grid: 2D grid representing the environment
    Returns: List of valid neighboring nodes
    """
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
    Args:
        agent: Agent object
        environment: Environment object
        setup: Setup object containing simulation parameters
    """
    # Create a deep copy of the grid to avoid modifying the original
    # Important for parallelization
    grid = copy.deepcopy(environment.grid)
    current = (int(agent.x * setup.grid_fineness), int(agent.y * setup.grid_fineness))

    grid[current[0]][current[1]] = 1

    goal = (int(environment.target_x * setup.grid_fineness), int(environment.target_y * setup.grid_fineness))


    open_list = []
    closed_list = set()
    heapq.heappush(open_list, Node(current[0], current[1], 0, euclidean_distance(*current, *goal)))
    came_from = {}

    # While there are nodes to explore
    while open_list:
        # Get the node with the lowest f value
        current_node = heapq.heappop(open_list)
        

        closed_list.add((current_node.x, current_node.y))

        # If we reached the goal, reconstruct the path and return
        if (current_node.x, current_node.y) == goal:
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            agent.set_path(path[::-1])

            return

        # Explore neighbors
        # Check if the neighbor is already in the closed list
        # If not, calculate the g and f values and add it to the open list
        for neighbor in get_neighbors(current_node, grid):
            if (neighbor.x, neighbor.y) in closed_list:
                continue

            if (neighbor.x, neighbor.y) not in came_from or neighbor.g < came_from[(neighbor.x, neighbor.y)].g:
                came_from[(neighbor.x, neighbor.y)] = neighbor
                heapq.heappush(open_list, Node(neighbor.x, neighbor.y, neighbor.g,
                                               euclidean_distance(neighbor.x, neighbor.y, *goal), current_node))



