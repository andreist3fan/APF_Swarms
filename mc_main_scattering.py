from Setup import Setup 
import Environment as e 
import Agent as a 
import Evaluation as ev
import pygame as pg 
import matplotlib.pyplot as plt
import time 
import os 

#---------------Monte Carlo settings---------------------------------

mc_runs = 1 #Runs per setting
mc_scattering = [1, 1.5, 2, 2.5, 3] 
nr_agents = 15 #Different settings 
smart = True

mc_name = "New Scattering test"

algorithm = 0

#Store results of each run for final analysis 
res_reachability = []               #stores value per setting 
res_path_length = []                #stores value per setting 
res_computational_complexity = []   #stores value per setting  
res_stuck_agents = []               #stores tupel per setting 

#---------------Folder logistics-------------------------------------- 

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

for sc in mc_scattering:

    setups_lst = []

    #---------------Monte Carlo runs-----------------------------------

    for m in range(mc_runs): 

        setup = Setup(algorithm) 

        #---------Adjust Setup according to MC Settings----------------

        setup.nr_agents = nr_agents
        setup.smart_swarm = smart 
        setup.start_radius = sc

        #--------------------------------------------------------------

        #Create environment according to setup
        env = e.Environment(setup)

        #Create agent according to setup
        agents = [] 
        pos_agents = []
        agents_stuck = []
        for i in range(setup.nr_agents): 
            agents.append(a.Agent(setup, env, pos_agents))
            pos_agents.append((agents[-1].x, agents[-1].y))

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

                #Check whether agent has reached target
                i.target_check(env)
                if i.target: 
                    setup.target = True 
                    end_time = time.time()
                    print("Target is reached.")
                    setup.computational_complexity = round((end_time - start_time), 5)
                    #print(setup.computational_complexity)
                    setup.path_length = len(i.pos_lst)
                    #print(setup.path_length)
                    setup.min_distance_target = ev.safety(i, env)

                # Check whether agent has reached a local minimum
                if i.local_minimum:
                    print("Agent is stuck in a local minimum")
                    #delete stuck agent
                    if setup.delete_stuck:
                        agents_stuck.append(agents[ind])
                        del agents[ind]
                    setup.nr_stuck_agents += 1 

                ind += 1

            steps += 1 

            #If too many steps required, run ends 
            if steps > 500: 
                running = False
                print("Run took to long and was stopped.")

            #If all agents are stuck, run failed 
            if ind == 0: 
                running = False 

        setups_lst.append(setup)
        print("Run " + str(m) + " completed")

        #Draw run if all agents got stuck 

        if setup.nr_stuck_agents == setup.nr_agents: 
            file_name = "All agents stuck ("+str(setup.nr_stuck_agents)+")("+str(m)+").png"
            ev.draw_run(setup, env, (agents+agents_stuck), folder_path, file_name)
        elif m == 0: 
            file_name = "Scattering ("+str(sc)+").png"
            ev.draw_run(setup, env, (agents+agents_stuck), folder_path, file_name)


    #---------------Final evaluation for one setting------------------------

    pl, cc, r, min_dist = ev.evaluate_multiple(setups_lst)

    stuck = []
    for s in setups_lst: 
        stuck.append(s.nr_stuck_agents)

    res_path_length.append(pl)
    res_computational_complexity.append(cc)
    res_reachability.append(r)
    res_stuck_agents.append(stuck)

    print("Setting "+str(sc)+" completed.")

#---------------Comparison of different settings----------------------------


#Reachability graph 
plt.figure()
plt.plot(mc_scattering, res_reachability, color="red")
plt.xlabel('Scattering')
plt.xticks(mc_scattering)
plt.ylabel('Reachability')
plt.ylim(0, 1.1)
plt.title('Reachability vs. Scattering')
plt.grid(True)
plot_path = os.path.join(folder_path, "ReachabilityScattering")
plt.savefig(plot_path)

#Computational Complexity graph 
plt.figure()
plt.plot(mc_scattering, res_computational_complexity, color="blue")
plt.xlabel('Scattering')
plt.xticks(mc_scattering)
plt.ylabel('Computational Complexity [s]')
plt.ylim(0, (max(res_computational_complexity)+0.001))
plt.title('Computational Complexity vs. Scattering')
plt.grid(True)
plot_path = os.path.join(folder_path, "ComplexityScattering")
plt.savefig(plot_path)

#Path length graph 
plt.figure()
plt.plot(mc_scattering, res_path_length, color="green")
plt.xlabel('Scattering')
plt.xticks(mc_scattering)
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
        file.write("\n\n Settings (Scattering): "+str(mc_scattering))
        file.write("\n\n Number of agents: "+str(nr_agents))
        file.write("\n\n Algorithm used: "+str(algorithm))
        if algorithm == 0: 
            file.write(" (CAPF)")
        if algorithm == 1: 
            file.write(" (BAPF)")
        if algorithm == 2: 
            file.write(" (CR-BAPF)")
        if algorithm == 3: 
            file.write(" (RAPF)")
        if algorithm == 4: 
            file.write(" (A*)")
        file.write("\n\n Number of stuck agents: "+str(res_stuck_agents))
        file.write("\n\n Path length: "+str(res_path_length))
        file.write("\n\n Computational complexity: "+str(res_computational_complexity))
        file.write("\n\n Reachability: "+str(res_reachability))
    print("File has been created.")

except Exception as e:
    print(f"An error occurred during creating the file: {e}")



