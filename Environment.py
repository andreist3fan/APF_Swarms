import random
import math 

class Environment: 
    def __init__(self, setup):
        
        #Target
        self.target_x = setup.target_x
        self.target_y = setup.target_y
        self.target_radius = setup.target_radius
        self.obstacles = [] # (x, y) for each obstacle
        self.artificial_obstacles = []

        #Create obstacles 

        #Determine number of obstacles 
        obst_nr = random.randint(setup.obst_N_lower, setup.obst_N_upper)

        for i in range(obst_nr): 
            close_to_target = True 
            close_to_other_obstacle = True 
            while close_to_target or close_to_other_obstacle: 
                
                #Create new position until one with distance to other objects is found 
                new_x = random.randint(0, setup.area_size)
                new_y = random.randint(0, setup.area_size)
                close_to_target = True 
                close_to_other_obstacle = True 

                #Check distance to target 
                distance_to_target = math.sqrt((new_x-setup.target_x)**2+(new_y-setup.target_y)**2)
                if distance_to_target >= (setup.target_radius + setup.obst_radius_inner): 
                    close_to_target = False 
                
                no_obstacle = True 

                #Check distance to other objects 
                for obs in self.obstacles: 
                    no_obstacle = False 
                    distance = math.sqrt((new_x-obs[0])**2+(new_y-obs[1])**2)
                    if distance >= (2*setup.obst_radius_inner):
                        close_to_other_obstacle = False 
                    else: 
                        print("Was too close")
                if no_obstacle: #There is no other obstacle yet 
                    close_to_other_obstacle = False 

            self.obstacles.append((new_x, new_y))
        
        print("Environment created")

    def adjust_initial_swarm_position(self, setup, agents): 
        #Move swarm such that closest agent at predetermined point 

        #Find closest agent 
        min_dist = math.sqrt((agents[0].x-setup.agents_start_x)**2+(agents[1].y-setup.agents_start_y)**2)
        closest_agent = agents[0]
        for ag in agents: 
            distance = math.sqrt((ag.x-setup.agents_start_x)**2+(ag.y-setup.agents_start_y)**2)
            if distance < min_dist: 
                min_dist = distance 
                closest_agent = ag 

        #Determine shift 
        shift_x = setup.agents_start_x - closest_agent.x
        shift_y = setup.agents_start_y - closest_agent.y

        #Shift agents 
        for ag in agents: 
            ag.x = ag.x + shift_x 
            ag.y = ag.y + shift_y 
            ag.pos_lst.append((ag.x, ag.y))
            print(str(ag.x)+", "+str(ag.y))
