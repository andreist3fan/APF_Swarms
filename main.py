from Setup import Setup 
import Environment as e 
import Agent as a 
import Evaluation as ev
import pygame as pg 
import time 

setup = Setup() 

#---------Change setup settings if not standard settings----------

setup.nr_agents = 1
setup.visual = True
setup.obst_radius_inner = 0.8
setup.grid_fineness = 5
setup.step_size = 0.2
setup.obst_N_lower = 180
setup.obst_N_upper = 200

#--------------Pygame settings------------------------------------

agent_radius = 5
scale = 600/30 #pixel/m 
running = True
wait_time = 0.1 #Determines speed of simulation
draw_influence = False #Draws outer radius of obstacles 

#Create pygame 
if setup.visual: 
    pg.init()
    screen = pg.display.set_mode((600, 600))
    running = True

#-----------------------------------------------------------------

#Create agent according to setup
agents = [] 
for i in range(setup.nr_agents): 
    agents.append(a.Agent(setup))

#Create environment according to setup
env = e.Environment(setup)

start_time = time.time()

while not setup.target and running: 

    #Draw pygame 
    if setup.visual: 

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        #screen.fill("black")
        
        #Draw agents 
        for a in agents: 
            pg.draw.circle(screen, "blue", pg.Vector2((a.x*scale), (a.y*scale)), agent_radius)
        
        #Draw target 
        pg.draw.circle(screen, "red", pg.Vector2((setup.target_x*scale), (setup.target_y*scale)), (setup.target_radius*scale))

        # draw obstacles
        for obstacle in env.obstacles:
            pos = pg.Vector2((obstacle[0]*scale), (obstacle[1]*scale))
            pg.draw.circle(screen, "white", pos, round(setup.obst_radius_inner*scale))
            if draw_influence: 
                pg.draw.circle(screen, "white", pos, round(setup.obst_radius_outer*scale), 2)

        time.sleep(wait_time)

    #Update posiiton of agents and check for target
    for i in agents: 

        #Update position 
        i.update_position(env, setup)

        #Check whether agent has reached target
        i.target_check(env)
        if i.target: 
            setup.target = True 
            end_time = time.time()
            print("Target is reached.")
            setup.computational_complexity = round((end_time - start_time), 5)
            if setup.visual: 
                print("Warning: The computational complexity is influenced by visualising the run.")
            setup.path_length = ev.evaluate_path_length(i)

    if setup.visual: 
        pg.display.flip()

if setup.visual: 
    pg.quit()

print("Path length:")
print(str(setup.path_length) + "m")
print("Computational complexity:")
print(str(setup.computational_complexity) + "s")
