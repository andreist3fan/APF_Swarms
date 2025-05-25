"""
This file implements the Changing Radii Artificial Potential Field with random walk (CR-BAPF*) algorithm for an agent to navigate towards a target while avoiding obstacles.

The potential field is calculated from the target and obstacle positions. Bacteria points are generated and evaluated to find the best point. 
The new agent position is then returned. When the agent is stuck, a random walk is applied.

"""

import numpy as np

def pos_update(agent, environment, setup): 
    # Step 1: Isolate all obstacles that are within the view range
    obstacles_in_range = []
    for obstacle in environment.obstacles:
        distance = ((agent.x - obstacle[0]) ** 2 + (agent.y - obstacle[1]) ** 2) ** 0.5
        if distance < setup.range:
            obstacles_in_range.append(obstacle)

    # Step 2: Define potential field equation
    def potential_field(x, y):
        target_potential = - setup.alpha_t * np.exp(-setup.mu_t * ((setup.target_x - x)**2 + (setup.target_y - y)**2))
        obstacle_potential = 0
        for obstacle in obstacles_in_range:
            distance_squared = (obstacle[0] - x)**2 + (obstacle[1] - y)**2
            if distance_squared**0.5 < setup.obst_radius_inner:
                obstacle_potential = float('inf')
            elif distance_squared**0.5 < setup.obst_radius_outer:
                obstacle_potential += setup.alpha_o * np.exp(-setup.mu_o * distance_squared)
        return target_potential + obstacle_potential

    # Step 3: Set bacteria points, find the minimum potential
    bacteria_points = [(agent.x + setup.step_size * np.cos(2* np.pi * k / setup.N_bacteria), agent.y + setup.step_size * np.sin(2* np.pi * k / setup.N_bacteria)) for k in range(setup.N_bacteria)]
    bacteria_potentials = [potential_field(x, y) for (x, y) in bacteria_points]
    min_potential = min(bacteria_potentials)

    # Step 4: Step to the best bacteria point (with random error), or stuck in local minimum in which case a random step is taken
    if min_potential < potential_field(agent.x, agent.y) and agent.random_walk == 0:
        selected_point = bacteria_points[bacteria_potentials.index(min_potential)]
        new_x = np.random.normal(selected_point[0], setup.step_variance)
        new_y = np.random.normal(selected_point[1], setup.step_variance)
        return new_x, new_y
    else: # Local minimum, searching for a random step that does not collide with an obstacle
        random_steps = np.random.permutation(bacteria_points)
        for random_step in random_steps: # Going 1-by-1 through possible random steps
            searching = False
            for obstacle in obstacles_in_range: # Checking the distance to every obstacle
                distance = ((random_step[0] - obstacle[0]) ** 2 + (random_step[1] - obstacle[1]) ** 2) ** 0.5
                if distance < (setup.obst_radius_inner + setup.agent_radius):
                    searching = True # If the random step is close to an obstacle, continue searching
            if not searching: # If the random step does not collide with an obstacle
                new_x = np.random.normal(random_step[0], setup.step_variance)
                new_y = np.random.normal(random_step[1], setup.step_variance)
                agent.random_walk += 1
                if agent.random_walk == setup.random_walk_length:  # When enough random steps have been taken, return to normal
                    agent.random_walk = 0
                return new_x, new_y
        # If none of the steps work, because they all collide with an obstacle (incredibly rare)
        agent.local_minimum = True
        return agent.x, agent.y

    