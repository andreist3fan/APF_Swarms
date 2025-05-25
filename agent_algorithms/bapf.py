"""
This file implements the Bacterial Artificial Potential Field (BAPF) algorithm for an agent to navigate towards a target while avoiding obstacles.

The potential field is calculated from the target and obstacle positions. Bacteria points are generated and evaluated to find the best point. The new agent position is then returned.

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
        obstacle_potentials = [setup.alpha_o * np.exp(-setup.mu_o *((obstacle[0] - x)**2 + (obstacle[1] - y)**2)) for obstacle in obstacles_in_range]
        return target_potential + sum(obstacle_potentials)

    # Step 3: Set bacteria points, find the minimum potential
    bacteria_points = [(agent.x + setup.step_size * np.cos(2* np.pi * k / setup.N_bacteria), agent.y + setup.step_size * np.sin(2* np.pi * k / setup.N_bacteria)) for k in range(setup.N_bacteria)]
    bacteria_potentials = [potential_field(x, y) for (x, y) in bacteria_points]
    min_potential = min(bacteria_potentials)

    # Step 4: Step to the best bacteria point (with random error), or stuck in local minimum
    if min_potential < potential_field(agent.x, agent.y):
        selected_point = bacteria_points[bacteria_potentials.index(min_potential)]
        new_x = np.random.normal(selected_point[0], setup.step_variance)
        new_y = np.random.normal(selected_point[1], setup.step_variance)
        return new_x, new_y
    else: # Local minimum
        agent.local_minimum = True
        return agent.x, agent.y