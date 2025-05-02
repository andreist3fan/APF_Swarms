from agent_algorithms import capf 
from agent_algorithms import bapf
from agent_algorithms import cr_bapf
from agent_algorithms import cr_bapf_star
from agent_algorithms import rapf 
from agent_algorithms import a_star 
from agent_algorithms import multi_agent_rapf
from agent_algorithms import L4_rapf
from agent_algorithms import capf_canyon
import random 
import math 
from scipy.stats import truncnorm

class Agent: 
    def __init__(self, setup, pos_other_agents, obstacles, fixed):

    #Fixed True: location at spawning center
    #Fixed False: location random scattered
        #------------Communication--------------------------------
        self.communicated_data = []         #List of all communicated data


        #------------Characteristics------------------------------

        self.algorithm = setup.algorithm

        # For A* algorithm, since we precompute the path
        self.step_no = None
        self.path = None
        #Current position
        self.x = 0                        #Current position
        self.y = 0
        self.radius = 0.2 #Agents cant spawn closer to each other than twice the radius
        self.pos_lst = []                   #List representing path

        self.initial_distance_target = 0 

        self.target = False
        self.hit = False                    #True if hit obstacle ("dead")
        self.local_minimum = False          #True if in local minimum

        self.artificial_obstacles = []      #List of all artificial obstacles locations
        self.radius = setup.agent_radius

        # For CR-BAPF*
        self.random_walk = 0

        #--------Determine initial agent position-----------------

        if setup.nr_agents == 1 or fixed:
            self.x = setup.agents_start_x 
            self.y = setup.agents_start_y
        else:
            center_x = setup.agents_start_x
            center_y = setup.agents_start_y

            min_dist_target = math.sqrt((center_x-setup.target_x)**2+(center_y-setup.target_y)**2)

            close_to_target = True
            close_to_other_agent = True
            close_to_obstacle = True

            while close_to_other_agent or close_to_obstacle or close_to_target:

                #Create new position until one with distance to other objects is found 
                angle = random.uniform(0, 2 * math.pi) #for random distribution 

                std_dev = (setup.start_radius) / 2
                a, b = (-setup.start_radius) / std_dev, (setup.start_radius) / std_dev
                dist_center = truncnorm.rvs(a, b, loc=0, scale=std_dev)

                new_x = center_x + dist_center * math.cos(angle)
                new_y = center_y + dist_center * math.sin(angle)

                #Reset conditions to check new location
                close_to_target = False
                close_to_other_agent = False
                close_to_obstacle = False

                #Check distance to target
                #distance_to_target = math.sqrt((new_x-setup.target_x)**2+(new_y-setup.target_y)**2)
                #if distance_to_target < min_dist_target:
                #    close_to_obstacle = True

                #Check distance to other agents
                if pos_other_agents:
                    for pos in pos_other_agents:
                        distance_between_agents = math.sqrt((new_x-pos[0])**2+(new_y-pos[1])**2)
                        if distance_between_agents <= (2*self.radius):
                            close_to_other_agent = True

                #Check distance to obstacles
                if obstacles:
                    for obs in obstacles:
                        distance_to_obs = math.sqrt((new_x-obs[0])**2+(new_y-obs[1])**2)
                        if distance_to_obs <= (setup.obst_radius + self.radius):
                            close_to_obstacle = True

                #Add condition to notice when circle is full because circle too small or swarm too big

            self.x = new_x
            self.y = new_y

        self.astar_init = False # for A*, if the grid was initialized or not
        #True if target is reached
        self.target = False 
        self.pos_lst.append((self.x, self.y))
        self.initial_distance_target = math.sqrt((self.x-setup.target_x)**2+(self.y-setup.target_y)**2)

    #------------------Functions-------------------------------------------

    # Update position based on position and algorithm

    def update_position(self, environment, setup, agent_positions = None): 
        if self.algorithm == 0: 
            self.x, self.y = capf.pos_update(self, environment, setup)
        elif self.algorithm == 1: 
            self.x, self.y = bapf.pos_update(self, environment, setup)
        elif self.algorithm == 2: 
            self.x, self.y = cr_bapf_star.pos_update(self, environment, setup)
        elif self.algorithm == 3: 
            self.x, self.y = rapf.pos_update(self, environment, setup)
        elif self.algorithm == 4:
            if not self.astar_init:
                a_star.initialize_path(self, environment, setup)
                self.astar_init = True
            self.x, self.y = a_star.pos_update(self, environment, setup)
        elif self.algorithm == 5:
            self.x, self.y = multi_agent_rapf.pos_update(self, environment, setup, agent_positions, 1)
        elif self.algorithm == 6:
            self.x, self.y = multi_agent_rapf.pos_update(self, environment, setup, agent_positions, 2)
        elif self.algorithm == 7:
            self.x, self.y = multi_agent_rapf.pos_update(self, environment, setup, agent_positions, 3)
        elif self.algorithm == 8:
            self.x, self.y = L4_rapf.pos_update(self, environment, setup, agent_positions, 3)
        elif self.algorithm == 100:
            self.x, self.y = capf_canyon.pos_update(self, environment, setup)

        #Append new location to the history list 
        self.pos_lst.append((self.x, self.y))

    # Check if target is reached

    def target_check(self, environment):
        # Set to True if target is reached
        distance_to_target = ((environment.target_x - self.x)**2 + (environment.target_y - self.y)**2)**0.5
        self.target = distance_to_target < environment.target_radius 

    #Check if obstacle is hit

    def obs_check(self, environment):
        for obs in environment.obstacles:
            distance_to_obstacle = math.sqrt((obs[0]-self.x)**2+(obs[1]-self.y)**2)
            if distance_to_obstacle < (self.radius + environment.obs_radius):
                self.hit = True

    # sets path for the A* algorithm, once computed
    def set_path(self, path):
        self.path = path
        self.step_no = 0