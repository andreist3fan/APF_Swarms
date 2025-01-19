import heapq
import numpy as np
from agent_algorithms.grid_node import Node

def pos_update(agent, environment, setup):

    # define useful functions

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
        for dx, dy in moves:
            nx, ny = node.x + dx, node.y + dy
            if is_valid(nx, ny, grid):
                cost = 1 if dx == 0 or dy == 0 else np.sqrt(2)  # Diagonal cost
                neighbors.append(Node(nx, ny, node.g + cost, 0, node))
        return neighbors

    def iterate(current,goal,grid):
        """
            Uses the A* algorithm to find the next best step towards the goal.
            :param current: current position
            :param goal: target position
            :param grid: 2D list of obstacles
        """
        print(f"Iterating: {current[0]}, {current[1]}, {goal[0]}, {goal[1]}")
        open_list = []

        heapq.heappush(open_list, Node(current[0], current[1], 0, euclidean_distance(*current, *goal)))

        closed_set = set()
        best_step = None

        while open_list:
            current_node = heapq.heappop(open_list)

            if (current_node.x, current_node.y) == goal:
                return (current_node.x, current_node.y)  # Reached the goal

            closed_set.add((current_node.x, current_node.y))

            # Get neighbors and compute cost
            for neighbor in get_neighbors(current_node, grid):
                if (neighbor.x, neighbor.y) in closed_set:
                    continue
                neighbor.h = euclidean_distance(neighbor.x, neighbor.y, *goal)
                neighbor.f = neighbor.g + neighbor.h
                heapq.heappush(open_list, neighbor)

            return open_list[0].x, open_list[0].y

        return current  # No valid move, stay in place

    no_steps = setup.grid_fineness * setup.step_size

    crt_x = int(agent.x*setup.grid_fineness)
    crt_y = int(agent.y*setup.grid_fineness)

    goal_x = int(environment.target_x*setup.grid_fineness)
    goal_y = int(environment.target_y*setup.grid_fineness)

    grid = environment.grid
    for _ in range (int(no_steps)):
        crt_x, crt_y = iterate((crt_x, crt_y), (goal_x, goal_y), grid)


    crt_x = crt_x/setup.grid_fineness
    crt_y = crt_y/setup.grid_fineness
    print(f"Position updated: {crt_x}, {crt_y}")
    return crt_x, crt_y