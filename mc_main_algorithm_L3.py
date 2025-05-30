# Monte Carlo run for Level 3 

from Setup import Setup 
import Environment as e 
import Agent as a 
import Evaluation as ev
import pygame as pg 
import matplotlib.pyplot as plt
import time 
import os 
import Analysis_settings_levels as asl 
import Arrays_Storage_Control as storage 
import time 

#----------------Level 3: Adjust settings--------------

mc_runs = 1000                      # Number of Monte Carlo runs 

file = 'Storage_L3_2.npy'           # Storage of simulation results 
swarm_set = asl.L3_2_swarm_size
scat_set = asl.L3_2_scattering


save_problematic_runs = False 
create_visuals = False              # Create folder for analysis 

mc_name = "Collision avoidance"     #Folder name to store analysis 

#Store results of each run for final analysis 
res_reachability = []               #stores value per setting 
res_path_length = []                #stores value per setting 
res_eff_path_length = []            #stores value per setting 
res_computational_complexity = []   #stores value per setting 
res_min_dist = []                   #stores value per setting  
res_stuck_agents = []               #stores tupel per setting 

#---------------Folder logistics-------------------------------------- 
if create_visuals:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, mc_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        con = False 
        while not con: 
            print(f"Folder '{mc_name}' already exists in {current_dir}. Do you want to keep the name?")
            print("0: no")
            print("1: yes (Files are getting deleted and replaced by new ones)")
            user_input = input("Enter 0 or 1: ")
            if user_input == "0":
                mc_name = input("Enter a new name for the folder: ")
                folder_path = os.path.join(current_dir, mc_name)
                print(f"New folder name '{mc_name}' will be used.")
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    con = True 
            else: 
                con = True 
                print("The name is kept and data overwritten.")

#--------------Runs for different settings----------------------------
setups_store = []

set_lst = []
data_lst = []

for alg in range(len(asl.L3_algorithm)):

    for swarm in range(len(swarm_set)):

        setups_lst = []

        for m in range(mc_runs): 

            #---------------Monte Carlo runs-----------------------------------

            setup = Setup(asl.L3_algorithm[alg]) 

            #---------Adjust Setup according to MC Settings----------------

            setup.nr_agents = swarm_set[swarm]
            setup.start_radius = scat_set[swarm]
            setup.obstacle_number = asl.L3_obs_number
            setup.algorithm = asl.L3_algorithm[alg]

            #--------------------------------------------------------------

            #Create environment according to setup
            env = e.Environment(setup)

            #Create agent according to setup
            agents = [] 
            pos_agents = []
            agents_stuck = []

            #Create rest of the swarm 
            for i in range((setup.nr_agents)): 
                    agents.append(a.Agent(setup, pos_agents, env.obstacles, False))
                    pos_agents.append((agents[-1].x, agents[-1].y))

            agents_all = agents.copy()

            running = True 
            start_time = time.time()

            #The while loop has to be updated according to the normal main function 

            steps = 0 

            while not setup.target and running: 

                ind = 0 

                #Update posiiton of agents and check for target
                for i in agents: 

                    #Update position 
                    if i.algorithm == 5 or i.algorithm == 6 or i.algorithm == 7: 
                        agent_positions = [(j.x, j.y) for j in agents if not j == i] # Used for Level 3: agent-agent collision avoidance
                        i.update_position(env, setup, agent_positions)
                    else:
                        i.update_position(env, setup)

                    #Check whether agent hit an obstacle 
                    i.obs_check(env)

                    #Check whether agent has reached target
                    i.target_check(env)

                    if i.target: 
                        end_time = time.time()

                        #Performance matrix
                        setup.target = True 
                        setup.computational_complexity = round((end_time - start_time), 5)
                        setup.path_length = (len(i.pos_lst)-1)*setup.step_size 
                        setup.eff_path_length = setup.path_length / i.initial_distance_target
                        setup.min_distance_target = ev.safety(i, env)

                    # Consequences if agent in trouble (hit obstacle, local minimum)
                    if i.hit: 
                        del agents[ind]
                        setup.nr_hit_agents += 1 
                    elif i.local_minimum:# Check whether agent has reached a local minimum
                        #delete stuck agent
                        if setup.delete_stuck:
                            agents_stuck.append(agents[ind])
                            del agents[ind]
                        setup.nr_stuck_agents += 1

                    ind += 1

                steps += 1 

                #If too many steps required, run ends 
                if steps > setup.step_limit: 
                    running = False

                    if create_visuals:
                        #Draw problematic run 
                        if save_problematic_runs:
                            file_name = "Run took too long (Algorithm "+str(alg)+")("+str(m)+").png"
                            ev.draw_run(setup, env, agents_all, folder_path, file_name)


                #If all agents are stuck, run failed 
                if ind == 0: 
                    running = False 
                    
                    if create_visuals:
                        #Draw problematic run 
                        if save_problematic_runs:
                            file_name = "All agents stuck (Algorithm "+str(alg)+")("+str(m)+").png"
                            ev.draw_run(setup, env, (agents+agents_stuck), folder_path, file_name)

            setups_lst.append(setup)

        print("Done setting: alg("+str(alg+1)+ "/4) swarm("+str(swarm+1)+"/"+str((len(swarm_set)))+")")
        

        # Intermediate storage 
        set_lst_new = [swarm, alg]
        set_lst.append(set_lst_new)

        pl_l, ef_pl_l, cc_l, r_l = ev.evaluate_multiple_detail(setups_lst)
        data_lst_new = [pl_l, ef_pl_l, cc_l, r_l]
        data_lst.append(data_lst_new)

# Store all data (they are all stored at the end to make sure that in 
# case the program stops in the middle, no intermediate results are stored that mess the storing structure up)
print("Start storing")

for i in range(len(set_lst)): 
    # performance_parameter_ind, swarm_setting_ind, collision, data
    storage.add_data_L3(0, set_lst[i][0], set_lst[i][1], data_lst[i][0], file)
    storage.add_data_L3(1, set_lst[i][0], set_lst[i][1], data_lst[i][1], file)
    storage.add_data_L3(2, set_lst[i][0], set_lst[i][1], data_lst[i][2], file)
    storage.add_data_L3(3, set_lst[i][0], set_lst[i][1], data_lst[i][3], file)

print("End storing")




    
