import numpy as np

def pos_update(agent, environment, setup): 
    # Step 1: Isolate all obstacles that are within the view range
    total_obstacles = environment.obstacles.copy() 
    obstacles_in_range = []
    
    #Smart swarm 
    if setup.smart_swarm: 
        if environment.artificial_obstacles: 
            total_obstacles.extend(environment.artificial_obstacles)
            print("I have added an artifical obstacle")

    for obstacle in total_obstacles: 
        distance = ((agent.x - obstacle[0]) ** 2 + (agent.y - obstacle[1]) ** 2) ** 0.5
        if distance < setup.range:
            obstacles_in_range.append(obstacle)

    # Step 2: Define potential field equation
    def potential_field(x, y):
        target_potential = - setup.alpha_t * np.exp(-setup.mu_t * ((setup.target_x - x)**2 + (setup.target_y - y)**2))
        obstacle_potentials = [setup.alpha_o * np.exp(-setup.mu_o *((obstacle[0] - x)**2 + (obstacle[1] - y)**2)) for obstacle in obstacles_in_range]
        return target_potential + sum(obstacle_potentials)

    # Step 3: Set bacteria points, sorted by distance to target
    bacteria_points = [(agent.x + setup.step_size * np.cos(2* np.pi * k / setup.N_bacteria), agent.y + setup.step_size * np.sin(2* np.pi * k / setup.N_bacteria)) for k in range(setup.N_bacteria)]
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
        
    # Step 5: If no better point was found, the agent is stuck in a local minimum
    agent.local_minimum = True
    return agent.x, agent.y # Return current location to avoid errors

    