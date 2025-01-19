import random
import math 

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
        
        print("Environment created")
