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

    # Step 3: Set bacteria points, sorted by distance to target
    target_vector_angle = np.arctan((setup.target_y - agent.y)/(setup.target_x - agent.x))
    bacteria_points = [(agent.x + setup.step_size * np.cos(2* np.pi * k / setup.N_bacteria_RAPF + target_vector_angle), agent.y + setup.step_size * np.sin(2* np.pi * k / setup.N_bacteria_RAPF + target_vector_angle)) for k in range(setup.N_bacteria_RAPF)]
    def distance_to_target(point):
        return ((point[0] - setup.target_x)**2 + (point[1] - setup.target_y)**2) **0.5
    sorted_bacteria_points = sorted(bacteria_points, key=distance_to_target)

    # Step 4: Find the first bacteria point that has a lower potential and make a step (including random position errors)
    J_agent = potential_field(agent.x, agent.y)
    for (x, y) in sorted_bacteria_points:
        if potential_field(x, y) <= J_agent:
            new_x = np.random.normal(x, setup.step_variance)
            new_y = np.random.normal(y, setup.step_variance)
            return new_x, new_y
        
    # Step 5: If no better point was found, the agent is stuck in a local minimum, so an artifical obstacle is placed
    agent.artificial_obstacles.append((agent.x, agent.y))
    print("Artificial obstacle placed")
    print(agent.artificial_obstacles)
    agent.local_minimum = True
    return agent.x, agent.y # Return current location to avoid errors

    