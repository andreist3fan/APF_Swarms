from Setup import Setup 
import Environment as e 
import Agent as a 
import Evaluation as ev
import pygame as pg 
import time 
import os 


#---------Change setup settings if not standard settings----------

algorithm = 0

setup = Setup(algorithm) 

setup.nr_agents = 3
setup.visual = True 
name = "main" #Name of the image of the simulation screenchot that is stored at the end 

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
agents_stuck = []
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

        #Draw target 
        pg.draw.circle(screen, "red", pg.Vector2((setup.target_x*scale), (setup.target_y*scale)), (setup.target_radius*scale))

        # draw obstacles
        for obstacle in env.obstacles:
            pos = pg.Vector2((obstacle[0]*scale), (obstacle[1]*scale))
            pg.draw.circle(screen, "white", pos, round(setup.obst_radius_inner*scale))
            if draw_influence: 
                pg.draw.circle(screen, "white", pos, round(setup.obst_radius_outer*scale), 2)
        
        #Draw agents and their artificial objects 
        for a in agents: 
            for obs in a.artificial_obstacles:
                print("Trying to draw artificial obstacle")
                pos = pg.Vector2((obs[0]*scale), (obs[1]*scale))
                pg.draw.circle(screen, "yellow", pos, round(setup.obst_radius_inner*scale))
                if draw_influence: 
                    pg.draw.circle(screen, "yellow", pos, round(setup.obst_radius_outer*scale), 2)
            pg.draw.circle(screen, "blue", pg.Vector2((a.x*scale), (a.y*scale)), agent_radius)

        for a in agents_stuck: 
            for obs in a.artificial_obstacles:
                print("Trying to draw artificial obstacle")
                pos = pg.Vector2((obs[0]*scale), (obs[1]*scale))
                pg.draw.circle(screen, "yellow", pos, round(setup.obst_radius_inner*scale))
                if draw_influence: 
                    pg.draw.circle(screen, "yellow", pos, round(setup.obst_radius_outer*scale), 2)

        time.sleep(wait_time)

    ind = 0

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
            setup.path_length = len(i.pos_lst)
            print("Minimum clearance: "+ str(ev.safety(i, env)))

        # Check whether agent has reached a local minimum
        if i.local_minimum:
            print("Agent is stuck in a local minimum")
            if setup.smart_swarm: 
                env.artificial_obstacles.append((i.x, i.y))
            #delete stuck agent
            if setup.delete_stuck:
                agents_stuck.append(agents[ind])
                del agents[ind]
            setup.nr_stuck_agents += 1 

        ind += 1 

    #If time limit is reached, run failed 
    if (time.time()-start_time) >= setup.time_limit: 
        running = False
        print("Run took to long and was stopped.")
        # Note by Rens: I would prefer using a maximum allowed number of steps instead of time limit, because a time limit is hard to determine for
        # running the Monte Carlo simulations (it wil be less then a second). The time limit will also have to be way higher when visualizing a run.

    #If all agents are stuck, run failed 
    if ind == 0: 
        running = False 

    if setup.visual: 
        pg.display.flip()

if setup.visual: 
    simulation_path = "simulation_main(algorithm "+str(algorithm)+").png"
    #current_dir = os.path.dirname(os.path.abspath(__file__))
    pg.image.save(screen, simulation_path)
    print(f"Simulation image saved.")
    pg.quit()

print("Path length:")
print(str(setup.path_length) + " steps")
print("Computational complexity:")
print(str(setup.computational_complexity) + "s")
print("Number of stuck agents:")
print(str(setup.nr_stuck_agents)+" out of "+str(setup.nr_agents))
