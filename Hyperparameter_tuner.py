from Setup import Setup 
import Environment as e 
import Agent as a 
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import differential_evolution

step_limit = 500
safety_goal = 0.5 #Goals for smallest distance to target in a set of 100 succesful runs (meter)

# Hyperparameters
alpha_t = 10000  # This one is kept constant, because it is all relative

def simulate(params):
    setup = Setup() 
    setup.algorithm = 0

    #Create agent
    agent = a.Agent(setup)

    #Create environment according to setup
    env = e.Environment(setup)

    # Set hyperparameters
    setup.alpha_t = alpha_t # This one is kept constant, because it is all relative
    setup.mu_t = params[0]
    setup.alpha_o = params[1]
    setup.mu_o = params[2]

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

def objective_function(params):
    num_samples = 100 # Run the simulation multiple times to average out randomness
    results = []
    while len(results) < num_samples:
        try:
            min_distance = simulate(params)
        except:
            min_distance = False
        if min_distance: # If the run was succesful and an actual value was presented
            results.append(min_distance)
    min_result = min(results)
    difference = abs(min_result - safety_goal)
    print("Tested some parameters with " + str(round(min_result, 2)) + " meter minimum clearance")
    if min_result > 0.1:
        print(params)
        print(oiujhgfdfghjkloiuygfghjklkjhgfdgielgiel)
    return difference

bounds = [(0.001, 1), (1, 1000), (1, 1000)]
bounds = [(0.0001, 0.01), (100, 500), (0.1, 10)]

# Perform optimization
result = differential_evolution(objective_function, bounds, tol=0.05)

print("Optimized parameters:", result.x)
print("Achieved average:", np.mean([simulate(result.x) for _ in range(100)]))