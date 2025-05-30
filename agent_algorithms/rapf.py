"""
This file implements the Robust Artificial Potential Field (RAPF) algorithm for an agent to navigate towards a target while avoiding obstacles.

The potential field is calculated from the target and (artificial) obstacle positions. Bacteria points are generated and evaluated to find the best point. 
The new agent position is then returned. When the agent is stuck, an artificial obstacle is placed.

"""

import numpy as np

def pos_update(agent, environment, setup): 
    # Step 1: Isolate all (artificial) obstacles that are within the view range
    obstacles_in_range = []
    for obstacle in environment.obstacles:
        distance = ((agent.x - obstacle[0]) ** 2 + (agent.y - obstacle[1]) ** 2) ** 0.5
        if distance < setup.range:
            obstacles_in_range.append(obstacle)
    for obstacle in agent.artificial_obstacles:
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
    N_bacteria_RAPF = setup.N_bacteria_RAPF
    target_vector_angle = np.arctan((setup.target_y - agent.y)/(setup.target_x - agent.x))
    bacteria_points = [(agent.x + setup.step_size * np.cos(2* np.pi * k / N_bacteria_RAPF + target_vector_angle), agent.y + setup.step_size * np.sin(2* np.pi * k / N_bacteria_RAPF + target_vector_angle)) for k in range(N_bacteria_RAPF)]
    bacteria_potentials = [potential_field(x, y) for (x, y) in bacteria_points]
    min_potential = min(bacteria_potentials)

    # Step 4: Step to the best bacteria point (with random error), or stuck in local minimum
    if min_potential < potential_field(agent.x, agent.y):
        selected_point = bacteria_points[bacteria_potentials.index(min_potential)]
        new_x = np.random.normal(selected_point[0], setup.step_variance)
        new_y = np.random.normal(selected_point[1], setup.step_variance)
    else: # Step 5: If no better point was found, the agent is stuck in a local minimum, first try a larger amount of bacteria points, otherwise an artifical obstacle is placed
        bacteria_points = [(agent.x + setup.step_size * np.cos(2* np.pi * k / setup.N_bacteria), agent.y + setup.step_size * np.sin(2* np.pi * k / setup.N_bacteria)) for k in range(setup.N_bacteria)]
        bacteria_potentials = [potential_field(x, y) for (x, y) in bacteria_points]
        min_potential = min(bacteria_potentials)
        selected_point = bacteria_points[bacteria_potentials.index(min_potential)] # Select the point with lowest potential, even if it is not an improvement (to dodge the artificial obstacle)
        new_x = np.random.normal(selected_point[0], setup.step_variance) # Move to the best position (with error)
        new_y = np.random.normal(selected_point[1], setup.step_variance)# Move to the best position (with error)
        if min_potential > potential_field(agent.x, agent.y):
            agent.artificial_obstacles.append((agent.x, agent.y)) # place artificial obstacle

    return new_x, new_y