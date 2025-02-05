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

#----------------Level 1: Adjust settings--------------

obs_num = 1                      #Index of density of list in asl (!not the actual value) -> 0, 1, 2
mc_runs = 100 

save_problematic_runs = False 
create_visuals = False            #Create folder for analysis 

mc_name = "Scattering (" + str(asl.L1_obstacle_number[obs_num]) + str(" obstacles)")        #Folder name to store analysis 

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

for sc in range(len(asl.L1_scattering)):

    setups_lst = []

    #---------------Monte Carlo runs-----------------------------------

    for m in range(mc_runs): 

        setup = Setup(asl.L1_algorithm) 

        #---------Adjust Setup according to MC Settings----------------

        setup.nr_agents = asl.L1_fixed_swarm_size
        setup.start_radius = asl.L1_scattering[sc]
        setup.obstacle_number = asl.L1_obstacle_number[obs_num]

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
                    setup.path_length = len(i.pos_lst)
                    setup.eff_path_length = setup.path_length / i.initial_distance_target_steps 
                    setup.min_distance_target = ev.safety(i, env)

                    print(setup.computational_complexity)

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
                        file_name = "Run took too long (Scattering "+str(sc)+")("+str(m)+").png"
                        ev.draw_run(setup, env, agents_all, folder_path, file_name)


            #If all agents are stuck, run failed 
            if ind == 0: 
                running = False 
                
                if create_visuals:
                    #Draw problematic run 
                    if save_problematic_runs:
                        file_name = "All agents stuck (Scattering "+str(sc)+")("+str(m)+").png"
                        ev.draw_run(setup, env, (agents+agents_stuck), folder_path, file_name)

        setups_lst.append(setup)

        #Store first run of each setting
        if create_visuals:
            if m == 0: 
                file_name = "Scattering (Example for "+str(sc)+").png"
                ev.draw_run(setup, env, (agents+agents_stuck), folder_path, file_name) 


    #---------------Final evaluation for one setting------------------------

    #Store data in storage files

    #path_length, eff_path_length, computational_complexity, reachability

    pl_l, ef_pl_l, cc_l, r_l = ev.evaluate_multiple_detail(setups_lst)

    #add_data(file_name, obstacle_density, swarm_setting, algorithm, data): 

    storage.add_data_L1("Storage_scattering_L1.npy", 0, obs_num, sc, pl_l)
    storage.add_data_L1("Storage_scattering_L1.npy", 1, obs_num, sc, ef_pl_l)
    storage.add_data_L1("Storage_scattering_L1.npy", 2, obs_num, sc, cc_l)
    storage.add_data_L1("Storage_scattering_L1.npy", 3, obs_num, sc, r_l)

    # Analyse setting for immediate diagram creation 
    if create_visuals: 
        pl, ef_pl, cc, r, min_dist = ev.evaluate_multiple(setups_lst)

        stuck = []
        for s in setups_lst: 
            stuck.append(s.nr_stuck_agents)

        res_path_length.append(pl)
        res_eff_path_length.append(ef_pl)
        res_computational_complexity.append(cc)
        res_reachability.append(r)
        res_min_dist.append(min_dist)
        res_stuck_agents.append(stuck)

    print("Setting "+str(sc+1)+" completed.")

#---------------Comparison of different settings----------------------------

if create_visuals:
    #Reachability graph 
    plt.figure()
    plt.plot(asl.L1_scattering, res_reachability, color="red")
    plt.xlabel('Scattering')
    plt.xticks(asl.L1_scattering)
    plt.ylabel('Reachability')
    plt.ylim(0, 1.1)
    plt.title('Reachability vs. Scattering')
    plt.grid(True)
    plot_path = os.path.join(folder_path, "ReachabilityScattering")
    plt.savefig(plot_path)

    #Computational Complexity graph 
    plt.figure()
    plt.plot(asl.L1_scattering, res_computational_complexity, color="blue")
    plt.xlabel('Scattering')
    plt.xticks(asl.L1_scattering)
    plt.ylabel('Computational Complexity [s]')
    plt.ylim(0, (max(res_computational_complexity)+0.001))
    plt.title('Computational Complexity vs. Scattering')
    plt.grid(True)
    plot_path = os.path.join(folder_path, "ComplexityScattering")
    plt.savefig(plot_path)

    #Path length graph 
    plt.figure()
    plt.plot(asl.L1_scattering, res_path_length, color="green")
    plt.xlabel('Scattering')
    plt.xticks(asl.L1_scattering)
    plt.ylabel('Path length [steps]')
    plt.ylim(0, (max(res_path_length)+5))
    plt.title('Path length vs. Scattering')
    plt.grid(True)
    plot_path = os.path.join(folder_path, "PathLengthScattering")
    plt.savefig(plot_path)

    #Save nr. stuck agents and other results in a text file 

    file_name = "Analysis.txt"
    file_path = os.path.join(folder_path, file_name)

    try:
        # Check if directory exists
        os.makedirs(folder_path, exist_ok=True)
        
        # Create the file and fill it with most important information
        with open(file_path, "w") as file:
            file.write("Testing different initial scattering for swarm")
            file.write("\n\n Runs per setting: "+str(mc_runs))
            file.write("\n\n Settings (Scattering): "+str(asl.L1_scattering))
            file.write("\n\n Number of agents: "+str(asl.L1_fixed_swarm_size))
            file.write("\n\n Algorithm used: "+str(asl.L1_algorithm))
            if asl.L1_algorithm == 0: 
                file.write(" (CAPF)")
            if asl.L1_algorithm == 1: 
                file.write(" (BAPF)")
            if asl.L1_algorithm == 2: 
                file.write(" (CR-BAPF)")
            if asl.L1_algorithm == 3: 
                file.write(" (RAPF)")
            if asl.L1_algorithm == 4: 
                file.write(" (A*)")
            file.write("\n\n Number of stuck agents: "+str(res_stuck_agents))
            file.write("\n\n Path length: "+str(res_path_length))
            file.write("\n\n Computational complexity: "+str(res_computational_complexity))
            file.write("\n\n Reachability: "+str(res_reachability))
            file.write("\n\n Safety distance (Closest distance to obstacle)"+str(res_min_dist))
        print("File has been created.")

    except Exception as e:
        print(f"An error occurred during creating the file: {e}")

storage.overview_scat_L1()

    





