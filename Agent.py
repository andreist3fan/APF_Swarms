from agent_algorithms import capf 
from agent_algorithms import bapf
from agent_algorithms import cr_bapf
from agent_algorithms import rapf 
from agent_algorithms import a_star 
import random 
import math 

class Agent: 
    def __init__(self, setup, environment, pos_other_agents):
        
        self.algorithm = setup.algorithm  

        #Current position
        self.x = 0
        self.y = 0 
        self.radius = 0.2 #Agents cant spawn closer to each other than twice the radius 

        if setup.nr_agents == 1: 
            self.x = setup.agents_start_x 
            self.y = setup.agents_start_y
        else: 
            '''
            angle = random.uniform(0, 2 * math.pi) #for random distribution 
            self.x = setup.agents_start_x + setup.start_radius * math.cos(angle)
            self.y = setup.agents_start_y + setup.start_radius * math.sin(angle)
            '''            
            close_to_obstacle = True 
            close_to_other_agent = True 

            while close_to_obstacle or close_to_other_agent: 

                #Create new position until one with distance to other objects is found 
                angle = random.uniform(0, 2 * math.pi) #for random distribution 
                new_x = setup.agents_start_x + setup.start_radius * math.cos(angle)
                new_y = setup.agents_start_y + setup.start_radius * math.sin(angle)
                close_to_obstacle = True 
                close_to_other_agent = True 

                #Check distance to other agents 
                for pos in pos_other_agents: 
                    distance_between_agents = math.sqrt((new_x-pos[0])**2+(new_y-pos[1])**2)
                    if distance_between_agents >= (2*self.radius): 
                        close_to_other_agent = False 
                if not pos_other_agents: #There is no other agent yet 
                    close_to_other_agent = False 

                for obs in environment.obstacles: 
                    distance = math.sqrt((new_x-obs[0])**2+(new_y-obs[1])**2)
                    if distance >= (2*setup.obst_radius_inner): 
                        close_to_obstacle = False 
                if not environment.obstacles: #There is no other obstacle yet 
                    close_to_other_obstacle = False 

                #Add condition to notice when circle is full because circle too small or swarm too big 
            self.x = new_x
            self.y = new_y
            #'''

        #List representing path of agent 
        self.pos_lst = [(self.x, self.y)]

        #True if target is reached 
        self.target = False 

        #True if in local minimum
        self.local_minimum = False

        #List of all artificial obstacles locations
        self.artificial_obstacles = []


    #Update position based on position 
    def update_position(self, environment, setup): 
        if self.algorithm == 0: 
            self.x, self.y = capf.pos_update(self, environment, setup)
        if self.algorithm == 1: 
            self.x, self.y = bapf.pos_update(self, environment, setup)
        if self.algorithm == 2: 
            self.x, self.y = cr_bapf.pos_update(self, environment, setup)
        if self.algorithm == 3: 
            self.x, self.y = rapf.pos_update(self, environment, setup)
        if self.algorithm == 4: 
            self.x, self.y = a_star.pos_update(self, environment, setup)
        
        #Append new location to the history list 
        self.pos_lst.append((self.x, self.y))

    def target_check(self, environment):
        # Set to True if target is reached
        distance_to_target = ((environment.target_x - self.x)**2 + (environment.target_y - self.y)**2)**0.5
        self.target = distance_to_target < environment.target_radius 
