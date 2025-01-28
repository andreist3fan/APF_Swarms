from Setup import Setup 
import Environment as e 
import Agent as a 
import Evaluation as ev
import pygame as pg 
import time 
import math

#---------Change setup settings if not standard settings----------

algorithm = 0
setup = Setup(algorithm)

setup.nr_agents = 20
setup.start_radius = 5

setup.visual = True     #Pygame to show run
setup.name = "Main"           #Name of the image of the simulation screenchot that is stored at the end 

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

while not setup.target and running: 

    ind = 0

    #Update posiiton of agents
    for i in agents: 

        #Update position 
        i.update_position(env, setup)

        #Check whether agent has reached target
        i.target_check(env)

        #Check whether agent hit an obstacle 
        i.obs_check(env)

        # Consequences if agent reached target
        if i.target: 
            end_time = time.time()

            #Performance matrix 
            setup.target = True 
            setup.computational_complexity = round((end_time - start_time), 5)
            setup.path_length = len(i.pos_lst)
            setup.eff_path_length = setup.path_length / i.initial_distance_target_steps 
            setup.min_distance_target = ev.safety(i, env)

            #User output 
            print("Target is reached.")
 
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
            pg.draw.circle(screen, "white", pos, round(setup.obst_radius*setup.scale))
        
        #Draw agents and their artificial objects 
        for a in agents: 
            #Artificial position of agents 
            for obs in a.artificial_obstacles:
                print("Trying to draw artificial obstacle")
                pos = pg.Vector2((obs[0]*setup.scale), (obs[1]*setup.scale))
                pg.draw.circle(screen, "yellow", pos, round(setup.agent_radius*setup.scale))

            #Agent in trouble
            if a.hit: 
                pg.draw.circle(screen, "orange", pg.Vector2((a.x*setup.scale), (a.y*setup.scale)), (a.radius*setup.scale))
            elif a.local_minimum: 
                pg.draw.circle(screen, "yellow", pg.Vector2((a.x*setup.scale), (a.y*setup.scale)), (a.radius*setup.scale))
            #Normal agent
            else: 
                pg.draw.circle(screen, "blue", pg.Vector2((a.x*setup.scale), (a.y*setup.scale)), (a.radius*setup.scale))


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