import pygame as pg 
import os 
import math

# Evaluate Monte Carlo simulation (average performance matrices)
# Return: path length, effective path length, complexity, reachability, min average distance

def evaluate_multiple(setups): 

    path_length = 0
    eff_path_length = 0                         

    computational_complexity = 0 
    avg_min_distance_obs = 0
    target = 0                      # Number of runs where an agent found the target 
    not_target = 0                  # Number of runs where swarm failed 

    for s in setups: 
        if s.target: 
            target += 1     
            path_length += s.path_length
            eff_path_length += s.eff_path_length 
            computational_complexity += s.computational_complexity 
            avg_min_distance_obs += s.min_distance_target
        else: 
            not_target += 1 
    if target != 0: 
        path_length = path_length/target 
        eff_path_length = eff_path_length/target 
        computational_complexity = computational_complexity/target 
        avg_min_distance_obs = avg_min_distance_obs/target 
    else: 
        path_length = 0
        computational_complexity = 0
        eff_path_length = 0
        avg_min_distance_obs = 0
    reachability = target/(target+not_target)

    return round(path_length, 3), round(eff_path_length, 3), round(computational_complexity, 5), reachability, round(avg_min_distance_obs, 3)

# Store data of all runs organized by performance parameter in arrays (prepare for storage)

def evaluate_multiple_detail(setups): 

    path_length = []
    eff_path_length = []                        
    computational_complexity = []
    reachability = []                      #1 for reached and 0 for all agents lost

    for s in setups: 
        if s.target: 
            path_length.append(s.path_length)
            eff_path_length.append(s.eff_path_length)
            computational_complexity.append(s.computational_complexity)
            reachability.append(1)
        else: 
            path_length.append(0)
            eff_path_length.append(0)
            computational_complexity.append(0)
            reachability.append(0)

    return path_length, eff_path_length, computational_complexity, reachability

# Find minimum clearance of an agent during the run 

def safety(agent, env):
    min_distance = float('inf')
    for obst_x, obst_y in env.obstacles:
        for agent_x, agent_y in agent.pos_lst:
            distance = ((obst_x - agent_x)**2 + (obst_y - agent_y)**2)**0.5
            if distance < min_distance:
                min_distance = distance
    return min_distance

# Draw run 

def draw_run(setup, env, agents, folder_path, file_name): 

    scale = setup.scale #pixel/m 

    pg.init()
    size = scale*setup.area_size
    screen = pg.display.set_mode((size, size))

    #Draw target 
    pg.draw.circle(screen, "red", pg.Vector2((setup.target_x*scale), (setup.target_y*scale)), (setup.target_radius*scale))
    
    #Draw spawning area agents 
    pg.draw.circle(screen, "green", ((setup.agents_start_x*setup.scale), (setup.agents_start_y*setup.scale)), (setup.start_radius*setup.scale), 2)

    #Draw obstacles
    for obstacle in env.obstacles:
        pos = pg.Vector2((obstacle[0]*scale), (obstacle[1]*scale))
        pg.draw.circle(screen, "white", pos, round(setup.obst_radius*scale))
    
    #Draw paths of agents 
    for a in agents: 
        for obs in a.artificial_obstacles:
            print("Trying to draw artificial obstacle")
            pos = pg.Vector2((obs[0]*scale), (obs[1]*scale))
            pg.draw.circle(screen, "yellow", pos, round(setup.obst_radius*scale))
        for pos in a.pos_lst: 
            pg.draw.circle(screen, "blue", pg.Vector2((pos[0]*scale), (pos[1]*scale)), (setup.agent_radius*scale))

    #Draw special points of agents on top
    for a in agents: 
        #Agent in trouble 
        if a.hit: 
            pg.draw.circle(screen, "orange", pg.Vector2((a.x*setup.scale), (a.y*setup.scale)), (a.radius*setup.scale))
        elif a.local_minimum: 
            pg.draw.circle(screen, "yellow", pg.Vector2((a.x*setup.scale), (a.y*setup.scale)), (a.radius*setup.scale))

        #Draw initial position of agents 
        pg.draw.circle(screen, "green", pg.Vector2((a.pos_lst[0][0]*setup.scale), (a.pos_lst[0][1]*setup.scale)), 2)
 
    pg.display.flip()
    file_path = os.path.join(folder_path, file_name)
    pg.image.save(screen, file_path)
    pg.quit()



