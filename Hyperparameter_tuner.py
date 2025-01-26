from Setup import Setup 
import Environment as e 
import Agent as a 
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

step_limit = 250
minimum_safety = 0.8 # 2 sigma safety (97.72% safe)

# Hyperparameters
algorithm = 1
alpha_t = 100
mu_t = 0.002
alpha_o = 8
mu_o = 1.5

def simulate():
    setup = Setup(algorithm)
    setup.nr_agents = 1
    setup.obst_N_lower = 150 #influenced by values in paper 
    setup.obst_N_upper = 200 

    #Create agent
    agent = a.Agent(setup, "placeholder", "placeholder")

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

        #If step limit is reached, run failed 
        if len(agent.pos_lst) >= step_limit: 
            running = False

    min_distance = float('inf')
    for obst_x, obst_y in env.obstacles:
        for agent_x, agent_y in agent.pos_lst:
            distance = ((obst_x - agent_x)**2 + (obst_y - agent_y)**2)**0.5
            if distance < min_distance:
                min_distance = distance
    return min_distance
"""
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
        """

num_samples = 1000 # Run the simulation multiple times to average out randomness
results = []
print("Simulating algorithm " + str(algorithm) + " with following hyperparameters: " + str(alpha_t) + ", " + str(mu_t) + ", " + str(alpha_o) + ", " + str(mu_o))
while len(results) < num_samples:
    print(str(len(results)) + " runs", end='\r')
    if len(results) % 100 == 0:
        print(str(len(results)) + " runs", end='\r')
    try:
        min_distance = simulate()
    except:
        min_distance = False
    if min_distance and not min_distance == 1: # If the run was succesful and an actual value was presented
        results.append(min_distance)
min_result = min(results)
avg_result = sum(results) / len(results)
sorted_results = sorted(results)
goal_result = sorted_results[int(0.0228*num_samples)]
print("Minimum clearance: " + str(round(min_result, 3)))
print("Average clearance: " + str(round(avg_result, 3)))
print("2 sigma safety clearance: " + str(round(goal_result, 3)))

# Plot the histogram of the data
plt.hist(results, bins=50, density=True, alpha=0.6, color='blue', label='Data')

# Fit a normal distribution to the data
mu, std = norm.fit(results)

# Generate the x values for the bell curve
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 1000)
p = norm.pdf(x, mu, std)

# Plot the bell curve
plt.plot(x, p, 'k', linewidth=2, label=f'Bell Curve\nμ={mu:.2f}, σ={std:.2f}')

# Add labels and legend
plt.title("Histogram with Bell Curve")
plt.xlabel("Value")
plt.ylabel("Density")
plt.legend()

# Show the plot
plt.show()