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

    # Step 3: Determine the gradient of the potential field
    def calculate_gradient(J, x, y, dx=1e-3, dy=1e-3):
        # Using central difference numerical differentiation
        dJ_dx = (J(x + dx, y) - J(x - dx, y)) / (2 * dx)
        dJ_dy = (J(x, y + dy) - J(x, y - dy)) / (2 * dy)
        return np.array([dJ_dx, dJ_dy])
    
    gradient = calculate_gradient(potential_field, agent.x, agent.y)

    # Step 4: Determine the best direction and make a step (including random position errors)
    if np.linalg.norm(gradient) == 0:
        raise ValueError('The gradient is 0. Choose better hyperparameters mafkees')

    direction = - gradient / np.linalg.norm(gradient)  # A unit vector in the direction of movement
    delta_x = setup.step_size * direction[0]
    delta_y = setup.step_size * direction[1]
    
    new_x = agent.x + np.random.normal(delta_x, setup.step_variance)
    new_y = agent.y + np.random.normal(delta_y, setup.step_variance)

    return new_x, new_y