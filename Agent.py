from agent_algorithms import capf 
from agent_algorithms import bapf
from agent_algorithms import cr_bapf
from agent_algorithms import rapf 
from agent_algorithms import a_star 

class Agent: 
    def __init__(self, setup):
        
        self.algorithm = setup.algorithm  

        #Current position
        self.x = 0
        self.y = 0 

        #List representing path of agent 
        self.x_lst = [self.x]
        self.y_lst = [self.y]

        #True if target is reached 
        self.target = False 


    #Update position based on position 
    def update_position(self, environment): 
        if self.algorithm == 0: 
            self.x, self.y = capf.pos_update(self, environment)
        if self.algorithm == 1: 
            self.x, self.y = bapf.pos_update(self, environment)
        if self.algorithm == 2: 
            self.x, self.y = cr_bapf.pos_update(self, environment)
        if self.algorithm == 3: 
            self.x, self.y = rapf.pos_update(self, environment)
        if self.algorithm == 4: 
            self.x, self.y = a_star.pos_update(self, environment)
        
        #Append new location to the history list 
        self.x_lst.append(self.x)
        self.y_lst.append(self.y)

