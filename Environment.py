import random
import math 
import numpy as np
class Environment: 
    def __init__(self, setup):
        
        #------------------Target-------------------------------------

        self.target_x = setup.target_x
        self.target_y = setup.target_y
        self.target_radius = setup.target_radius

        #-----------------Obstacles-----------------------------------

        self.obstacles = []                     # (x, y) for each obstacle
        self.obs_radius = setup.obst_radius

        #Determine number of obstacles 
        obst_nr = random.randint(setup.obst_N_lower, setup.obst_N_upper)

        # Create obstacles
        possible_locations = [(x, y) for x in range(setup.area_size) for y in range(setup.area_size)]
        # Integer locations neighbouring the spawn and target points are removed
        unavailable_locations = [(x, y) for x in range(self.target_x - 1, self.target_x + 2) for y in range(self.target_y - 1, self.target_y + 2)] + [(x, y) for x in range(setup.agents_start_x - 1, setup.agents_start_x + 2) for y in range(setup.agents_start_y - 1, setup.agents_start_y + 2)]
        available_locations = [(x, y) for x, y in possible_locations if (x, y) not in unavailable_locations]
        self.obstacles = random.sample(available_locations, obst_nr)

        #Create grid for A* algorithm
        if setup.algorithm == 4:
            """
            #Create grid for A* algorithm
            self.grid =  np.zeros((setup.area_size * setup.grid_fineness, setup.area_size * setup.grid_fineness))

            # Mark all cells in the range of the obstacles as occupied
            for i in range (setup.area_size * setup.grid_fineness):
                for j in range (setup.area_size * setup.grid_fineness):
                    for obstacle in self.obstacles:
                        distance = ((i/setup.grid_fineness - obstacle[0])
                                    ** 2 + (j/setup.grid_fineness - obstacle[1]) ** 2) ** 0.5
                        # Mark the cell as occupied if it is within the inner radius of an obstacle
                        if distance < setup.obst_radius_inner:
                            self.grid[i][j] = -1
                            break
            """
            # Create grid for A* algorithm
            grid_size = setup.area_size * setup.grid_fineness
            grid = np.zeros((grid_size, grid_size))
            obstacle_avoidance_radius = setup.obst_radius_inner + setup.agent_radius
            obst_radius_cells = int(obstacle_avoidance_radius * setup.grid_fineness)
            for obstacle in self.obstacles:
                # Convert obstacle center to grid coordinates
                ox, oy = int(obstacle[0] * setup.grid_fineness), int(obstacle[1] * setup.grid_fineness)
                
                # Calculate bounds for the circle in grid coordinates
                x_min = max(0, ox - obst_radius_cells)
                x_max = min(grid.shape[0], ox + obst_radius_cells + 1)
                y_min = max(0, oy - obst_radius_cells)
                y_max = min(grid.shape[1], oy + obst_radius_cells + 1)
                
                # Mark the cells within the circle
                for x in range(x_min, x_max):
                    for y in range(y_min, y_max):
                        if (x - ox)**2 + (y - oy)**2 <= obst_radius_cells**2:
                            grid[x, y] = -1

            self.grid = grid
            
