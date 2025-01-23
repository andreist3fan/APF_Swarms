import random
import math 
import numpy as np
class Environment: 
    def __init__(self, setup):
        
        #Target
        self.target_x = setup.target_x
        self.target_y = setup.target_y
        self.target_radius = setup.target_radius
        self.obstacles = [] # (x, y) for each obstacle

        #Create obstacles 

        #Determine number of obstacles 
        obst_nr = random.randint(setup.obst_N_lower, setup.obst_N_upper)

        for i in range(obst_nr): 
            close_to_target = True 
            while close_to_target: 
                obst_x = random.randint(0, setup.area_size)
                obst_y = random.randint(0, setup.area_size)
                distance_to_target = math.sqrt((obst_x-setup.target_x)**2+(obst_y-setup.target_y)**2)
                if distance_to_target >= (setup.target_radius + setup.obst_radius_inner): 
                    close_to_target = False 
            self.obstacles.append((obst_x, obst_y))


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

        print("Environment created")
