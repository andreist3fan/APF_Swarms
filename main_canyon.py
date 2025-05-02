from Setup import Setup
import Environment as e 
import Agent as a 
import Evaluation as ev
import pygame as pg 
import time 
import math
import random
import numpy as np
from Communication.communication import pool_communication_data
from Communication.communication_distance import min_communication_distance

# seed for reproducibility for placement of agents and obstacles.

# Seeds to test improvements: 74967
# 878804799
# 963476
seed =  random.randint(0, int(1e9))
np.random.seed(seed=seed)
random.seed(a=seed)

#---------Change setup settings if not standard settings----------
# 0: CAPF
# 1: BAPF
# 2: CR-BAPF*
# 3: RAPF
# 4: A*

# 100: CAPF with Canyon approach and tweaks
algorithm = 100
setup = Setup(algorithm)
setup.obstacle_number = 110

setup.nr_agents = 5
setup.start_radius = 3

setup.visual = True     #Pygame to show run
setup.name = "Main"     #Name of the image of the simulation screenshot that is stored at the end

#--------------Pygame settings------------------------------------

setup.scale = 15        #pixel/m 
wait_time = 0.1         #Determines speed of simulation

# Agents in local minimum:  Yellow 
# Agents that hit obstacle: Orange 

#-----------------------------------------------------------------

#Create pygame 
if setup.visual: 
    pg.init()
    screen = pg.display.set_mode(((setup.scale*setup.area_size), (setup.scale*setup.area_size)))
    screen.fill("white")
    running = True

#Create environment and obstacles according to setup
env = e.Environment(setup)
print("Environment created")

#Create agent according to setup
agents = [] 
pos_agents = []
agents_stuck = []

#Create rest of the swarm 
for i in range((setup.nr_agents)): 
        agents.append(a.Agent(setup, pos_agents, env.obstacles, False))
        pos_agents.append((agents[-1].x, agents[-1].y))
print("Agents created")

agents_all = agents.copy()

#Start simulation 
start_time = time.time()
steps = 0 
running = True
agent_visual_colors = []

while not setup.target and running: 

    agents_targets = [x.target for x in agents]
    non_target = [x for x in agents if not x.target]
    if all(agents_targets):
        running = False
        print("All agents reached the target.")
        break

    ind = 0
    

    #Update posiiton of agents
    for index,i in enumerate(agents):
        
        agent_positions = [(j.x, j.y) for j in agents if not j == i] # Used for Level 3: agent-agent collision avoidance
        
        #Update position
        if not i.target:

            i.update_position(env, setup, agent_positions)

            #Check whether agent has reached target
            i.target_check(env)

            #Check whether agent hit an obstacle
            i.obs_check(env)

            # if(len(non_target)<=2):
            #     print(f"agent is at {i.x}, {i.y}")

        # Consequences if agent reached target
        if i.target: 
            end_time = time.time()

            #Performance matrix
            #setup.target = True
            #setup.computational_complexity = round((end_time - start_time), 5)
            #setup.path_length = len(i.pos_lst)
            #setup.eff_path_length = setup.path_length / i.initial_distance_target_steps
            #setup.min_distance_target = ev.safety(i, env)

            #Compute minimum communication distance such that all agents know that
            # this one has reached the target
            min_d = min_communication_distance(agents + agents_stuck)
            setup.min_communication_distance = min_d
            # print(f"Target is reached. Minimum communication distance:{min_d}")
 

            # Gather path data and communicate it among agents
            pool_communication_data(agents, setup)

            # insert into Setup
            
            
        # Consequences if agent in trouble (hit obstacle, local minimum)
        if i.hit: 
            print("Agent hit an obstacle :(")
            del agents[ind]
            setup.nr_hit_agents += 1 
        elif i.local_minimum:# Check whether agent has reached a local minimum
            print("Agent is stuck in a local minimum")
            #delete stuck agent
            if setup.delete_stuck:
                agents_stuck.append(agents[ind])
                del agents[ind]
            setup.nr_stuck_agents += 1

        ind += 1 

    # Assign colors to agents for better visualization in clutered areas
    if setup.visual and len(agent_visual_colors) == 0:
        for a in agents:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            agent_visual_colors.append(pg.Color(r,g,b,1))
    # Draw pygame 
    if setup.visual: 

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        #Draw spawning area agents 
        min_dist = math.sqrt((setup.target_x-setup.agents_start_x)**2+(setup.target_y-setup.agents_start_y)**2)
        pg.draw.circle(screen, "green", ((setup.agents_start_x*setup.scale), (setup.agents_start_y*setup.scale)), (setup.start_radius*setup.scale), 2)

        #Draw target 
        pg.draw.circle(screen, "red", pg.Vector2((setup.target_x*setup.scale), (setup.target_y*setup.scale)), (setup.target_radius*setup.scale))

        # draw obstacles
        for obstacle in env.obstacles:
            pos = pg.Vector2((obstacle[0]*setup.scale), (obstacle[1]*setup.scale))
            pg.draw.circle(screen, "gray", pos, round(setup.obst_radius*setup.scale))

        #Draw agents and their artificial objects 
        for ix,a in enumerate(agents):
            #Artificial position of agents 
            for obs in a.artificial_obstacles:
                #print("Trying to draw artificial obstacle")
                pos = pg.Vector2((obs[0]*setup.scale), (obs[1]*setup.scale))
                pg.draw.circle(screen, "yellow", pos, round(setup.agent_radius*setup.scale))

            #Agent in trouble
            if a.hit: 
                pg.draw.circle(screen, "orange", pg.Vector2((a.x*setup.scale), (a.y*setup.scale)), (a.radius*setup.scale))
            elif a.local_minimum: 
                pg.draw.circle(screen, "yellow", pg.Vector2((a.x*setup.scale), (a.y*setup.scale)), (a.radius*setup.scale))
            #Normal agent
            else: 
                pg.draw.circle(screen, agent_visual_colors[ix], pg.Vector2((a.x*setup.scale), (a.y*setup.scale)), (a.radius*setup.scale))


        #Draw initial position of agents 
        for pos in pos_agents: 
            pg.draw.circle(screen, "green", pg.Vector2((pos[0]*setup.scale), (pos[1]*setup.scale)), 2)

        #Draw artificial obstacles of stuck agents 
        for a in agents_stuck: 
            for obs in a.artificial_obstacles:
                print("Trying to draw artificial obstacle")
                pos = pg.Vector2((obs[0]*setup.scale), (obs[1]*setup.scale))
                pg.draw.circle(screen, "yellow", pos, round(setup.obst_radius_inner*setup.scale))

        time.sleep(wait_time)

    steps += 1

    #If too many steps required, run ends 
    if steps > setup.step_limit: 
        running = False
        print("Run took to long and was stopped.")
        for agent in agents:
            if not agent.target:
                agent.local_minimum = True
                agents_stuck.append(agent)
                setup.nr_stuck_agents += 1

    #If all agents are stuck, run failed 
    if ind == 0: 
        running = False 

    if setup.visual: 
        pg.display.flip()

#Save image of run 
if setup.visual: 
    simulation_path = "simulation "+str(setup.name)+" (algorithm "+str(algorithm)+").png"
    pg.image.save(screen, simulation_path)
    print(f"Simulation image saved.")
    pg.quit()

#User output 
print(f"Seed used for simulation: {seed}")
print("Path length:")
print(str(setup.path_length) + " steps")
print("Computational complexity:")
print(str(setup.computational_complexity) + "s")
if setup.visual: 
    print("Warning: The computational complexity is influenced by visualising the run.")
print("Minimum clearance: "+ str(ev.safety(i, env)))
print("Number of stuck agents:")
print(str(setup.nr_stuck_agents)+" out of "+str(setup.nr_agents))
print("Number of agents that hit an obstacle: ")
print(str(setup.nr_hit_agents)+" out of "+str(setup.nr_agents))
print("Number of left agents: ")
print(len(agents))