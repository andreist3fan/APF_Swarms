import pygame as pg 
import os 

def evaluate_multiple(setups): 
    path_length = 0
    computational_complexity = 0 
    avg_min_distance_obs = 0
    target = 0 
    not_target = 0 
    for s in setups: 
        if s.target: 
            target += 1     
            path_length += s.path_length 
            computational_complexity += s.computational_complexity 
            avg_min_distance_obs += s.min_distance_target
        else: 
            not_target += 1 
    if target != 0: 
        path_length = path_length/target 
        computational_complexity = computational_complexity/target 
        avg_min_distance_obs = avg_min_distance_obs/target 
    else: 
        path_length = 0
        computational_complexity = 0
        avg_min_distance_obs = 0
    reachability = target/(target+not_target)
    return round(path_length, 3), round(computational_complexity, 5), reachability, round(avg_min_distance_obs, 3)

def safety(agent, env):
    min_distance = float('inf')
    for obst_x, obst_y in env.obstacles:
        for agent_x, agent_y in agent.pos_lst:
            distance = ((obst_x - agent_x)**2 + (obst_y - agent_y)**2)**0.5
            if distance < min_distance:
                min_distance = distance
    return min_distance

#Function that draws a run if wanted 

def draw_run(setup, env, agents, folder_path, file_name): 

    agent_radius = 5
    scale = 600/30 #pixel/m 

    pg.init()
    screen = pg.display.set_mode((600, 600))

    #Draw target 
    pg.draw.circle(screen, "red", pg.Vector2((setup.target_x*scale), (setup.target_y*scale)), (setup.target_radius*scale))

    # draw obstacles
    for obstacle in env.obstacles:
        pos = pg.Vector2((obstacle[0]*scale), (obstacle[1]*scale))
        pg.draw.circle(screen, "white", pos, round(setup.obst_radius_inner*scale))
    
    #Draw agents and their artificial objects 
    for a in agents: 
        for obs in a.artificial_obstacles:
            print("Trying to draw artificial obstacle")
            pos = pg.Vector2((obs[0]*scale), (obs[1]*scale))
            pg.draw.circle(screen, "yellow", pos, round(setup.obst_radius_inner*scale))
        for pos in a.pos_lst: 
            pg.draw.circle(screen, "blue", pg.Vector2((pos[0]*scale), (pos[1]*scale)), agent_radius)
    
    pg.display.flip()
    file_path = os.path.join(folder_path, file_name)
    pg.image.save(screen, file_path)
    print(f"Simulation image saved.")
    pg.quit()



