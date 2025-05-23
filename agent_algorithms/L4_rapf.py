import numpy as np

####### !!!!!!!!!!!!!!!!!!!!! #######
## This method is an attempt at creating inter-agent attraction forces when agents are about to leave the communication distance,
## thereby assuring that the communication network remains connected.
## This method is not used in the paper.


def pos_update(agent, environment, setup, agent_positions, implementation): 
    # Step 1: Isolate all (artificial) obstacles and agents that are within the view range
    obstacles_in_range = []
    agents_in_range = []
    agents_in_comm_range = []
    communication_range = 5
    agent_attraction_strength = 0.5
    for obstacle in environment.obstacles:
        distance = ((agent.x - obstacle[0]) ** 2 + (agent.y - obstacle[1]) ** 2) ** 0.5
        if distance < setup.range:
            obstacles_in_range.append(obstacle)
    for obstacle in agent.artificial_obstacles:
        distance = ((agent.x - obstacle[0]) ** 2 + (agent.y - obstacle[1]) ** 2) ** 0.5
        if distance < setup.range:
            obstacles_in_range.append(obstacle)
    for other_agent in agent_positions:
        distance = ((agent.x - other_agent[0]) ** 2 + (agent.y - other_agent[1]) ** 2) ** 0.5
        if distance < setup.range:
            agents_in_range.append(other_agent)
        if distance < communication_range:
            agents_in_comm_range.append(other_agent)

    # Step 2: Define potential field equation
    starting_distance_to_target = ((setup.target_x - setup.agents_start_x)**2 + (setup.target_y - setup.agents_start_y)**2) ** 0.5
    def potential_field(x, y):
        target_potential = - setup.alpha_t * np.exp(-setup.mu_t * ((setup.target_x - x)**2 + (setup.target_y - y)**2))
        obstacle_potential = 0
        agent_potential = 0
        # Obstacles
        for obstacle in obstacles_in_range:
            distance_squared = (obstacle[0] - x)**2 + (obstacle[1] - y)**2
            if distance_squared**0.5 < setup.obst_radius_inner:
                obstacle_potential = float('inf')
            elif distance_squared**0.5 < setup.obst_radius_outer:
                obstacle_potential += setup.alpha_o * np.exp(-setup.mu_o * distance_squared)
        # Inter-agent repelling forces
        for other_agent in agents_in_range:
            distance = ((x - other_agent[0]) ** 2 + (y - other_agent[1]) ** 2) ** 0.5
            if implementation == 1 or implementation == 2 or implementation == 3:
                if distance < agent.radius * 2 * 1.5: # Added 50% safety margin (still needs to be decided how to handle things properly)
                    agent_potential = float('inf')
            if implementation == 2:
                if distance < setup.agent_influence_radius:
                    agent_potential += setup.alpha_a * np.exp(-setup.mu_a * distance**2)
            if implementation == 3:
                distance_to_target = ((setup.target_x - other_agent[0])**2 + (setup.target_y - other_agent[1])**2) ** 0.5
                relative_distance_to_target = distance_to_target / starting_distance_to_target
                if distance < setup.agent_influence_radius:
                    agent_potential += 2 * relative_distance_to_target * setup.alpha_a * np.exp(-setup.mu_a * distance**2)
        # Attracting forces to keep connected network
        if len(agents_in_comm_range) == 1:
            other_agent = agents_in_comm_range[0] # The only entry in that list
            distance = ((x - other_agent[0]) ** 2 + (y - other_agent[1]) ** 2) ** 0.5
            if distance < communication_range:
                agent_potential += agent_attraction_strength * communication_range**2 / (distance - communication_range)**2
            else:
                agent_potential = float('inf')


        return target_potential + obstacle_potential + agent_potential

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
        new_x = np.random.normal(selected_point[0], setup.step_variance)
        new_y = np.random.normal(selected_point[1], setup.step_variance)
        if min_potential > potential_field(agent.x, agent.y):
            agent.artificial_obstacles.append((agent.x, agent.y))

    return new_x, new_y