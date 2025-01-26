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
        self.artificial_obstacles = []          # found by agents
        self.obs_radius = setup.obst_radius

        #Determine number of obstacles 
        obst_nr = random.randint(setup.obst_N_lower, setup.obst_N_upper)

        #Create obstacles
        for i in range(obst_nr):
            close_to_target = True
            close_to_other_obstacle = True

            while close_to_target or close_to_other_obstacle: 
                
                #Create new position until one with distance to other objects is found 
                new_x = random.randint(0, setup.area_size)
                new_y = random.randint(0, setup.area_size)

                #Reset conditions to check new location
                close_to_target = False
                close_to_other_obstacle = False

                #Check distance to target 
                distance_to_target = math.sqrt((new_x-setup.target_x)**2+(new_y-setup.target_y)**2)
                if distance_to_target <= (setup.target_radius + setup.obst_radius):
                    close_to_target = True

                #Check if it is close to preset closest agent
                distance = math.sqrt((new_x-setup.agents_start_x)**2+(new_y-setup.agents_start_y)**2)
                if distance < (setup.obst_radius + setup.agent_radius):
                    close_to_other_obstacle = True

                #Check distance to other objects 
                if self.artificial_obstacles:
                    for obs in self.obstacles:
                        distance = math.sqrt((new_x-obs[0])**2+(new_y-obs[1])**2)
                        if distance <= (2*setup.obst_radius):
                            close_to_other_obstacle = True

            self.obstacles.append((new_x, new_y))


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
