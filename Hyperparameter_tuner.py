from Setup import Setup 
import Environment as e 
import Agent as a 
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import differential_evolution

step_limit = 500
safety_goal = 0.5 #Goals for smallest distance to target in a set of 100 succesful runs (meter)

# Hyperparameters
algorithm = 1
alpha_t = 10000
mu_t = 0.0017
alpha_o = 430
mu_o = 3.6

def simulate():
    setup = Setup(algorithm) 

    #Create agent
    agent = a.Agent(setup)

    #Create environment according to setup
    env = e.Environment(setup)

    # Set hyperparameters
    setup.alpha_t = alpha_t
    setup.mu_t = mu_t
    setup.alpha_o = alpha_o
    setup.mu_o = mu_o

    running = True 

    while not setup.target and running: 

        #Update position 
        agent.update_position(env, setup)

        #Check whether agent has reached target
        agent.target_check(env)
        if agent.target: 
            setup.target = True 

        # Check whether agent has reached a local minimum
        if agent.local_minimum:
            running = False 

        #If time limit is reached, run failed 
        if len(agent.pos_lst) >= step_limit: 
            running = False

    if setup.target:
        # Calculates the minimum distance to any obstacle in succesful runs
        min_distance = float('inf')
        for obst_x, obst_y in env.obstacles:
            for agent_x, agent_y in agent.pos_lst:
                distance = ((obst_x - agent_x)**2 + (obst_y - agent_y)**2)**0.5
                if distance < min_distance:
                    min_distance = distance
        return min_distance
    
    else:
        return False

num_samples = 1000 # Run the simulation multiple times to average out randomness
results = []
while len(results) < num_samples:
    try:
        min_distance = simulate()
    except:
        min_distance = False
    if min_distance: # If the run was succesful and an actual value was presented
        results.append(min_distance)
min_result = min(results)
avg_result = sum(results) / len(results)
print("Minimum clearance: " + str(round(min_result, 3)))
print("Average clearance: " + str(round(avg_result, 3)))