from agent_algorithms import capf 
from agent_algorithms import bapf
from agent_algorithms import cr_bapf
from agent_algorithms import rapf 
from agent_algorithms import a_star 
import random 
import math 

class Agent: 
    def __init__(self, setup):
        
        self.algorithm = setup.algorithm  

        #Current position
        self.x = 0
        self.y = 0 

        if setup.nr_agents == 1: 
            self.x = setup.agents_start_x 
            self.y = setup.agents_start_y
        else: 
            angle = random.uniform(0, 2 * math.pi) #for random distribution 
            self.x = setup.agents_start_x + setup.start_radius * math.cos(angle)
            self.y = setup.agents_start_y + setup.start_radius * math.sin(angle)

        #List representing path of agent 
        self.pos_lst = [(self.x, self.y)]

        #True if target is reached 
        self.target = False 


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
        # Returns true if target is reached
        distance_to_target = ((environment.target_x - self.x)**2 + (environment.target_y - self.y)**2)**0.5
        self.target = distance_to_target < environment.target_radius 
