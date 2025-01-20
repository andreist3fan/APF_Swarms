from Setup import Setup 
import Environment as e 
import Agent as a 
import Evaluation as ev
import pygame as pg 
import matplotlib.pyplot as plt
import time 
import os 

#---------------Monte Carlo settings---------------------------------

mc_runs = 5 #Runs per setting
mc_nr_agents = [1, 2, 3, 5, 10, 20] #Different settings 

mc_name = "Number_of_agents_new"

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

for na in mc_nr_agents:

    setups_lst = []

    #---------------Monte Carlo runs-----------------------------------

    for m in range(mc_runs): 

        setup = Setup() 

        #---------Adjust Setup according to MC Settings----------------

        setup.nr_agents = na 

        #--------------------------------------------------------------

        #Create agents
        agents = [] 
        for i in range(setup.nr_agents): 
            agents.append(a.Agent(setup))

        #Create environment according to setup
        env = e.Environment(setup)

        running = True 

        start_time = time.time()

        #The while loop has to be updated according to the normal main function 

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

                # Check whether agent has reached a local minimum
                if i.local_minimum:
                    print("Agent is stuck in a local minimum")
                    #delete stuck agent
                    if setup.delete_stuck:
                        del agents[ind]
                    setup.nr_stuck_agents += 1 

                ind += 1

            #If time limit is reached, run failed 
            if (time.time()-start_time) >= setup.time_limit: 
                running = False
                print("Run took to long and was stopped.")

            #If all agents are stuck, run failed 
            if ind == 0: 
                running = False 

        setups_lst.append(setup)
        print("Run " + str(m) + " completed")

    #---------------Final evaluation for one setting------------------------

    pl, cc, r = ev.evaluate_multiple(setups_lst)

    res_path_length.append(pl)
    res_computational_complexity.append(cc)
    res_reachability.append(r)

    stuck = []
    for s in setups_lst: 
        stuck.append(s.nr_stuck_agents)

    print("Setting "+str(na)+" completed.")

#---------------Comparison of different settings----------------------------


#Reachability graph 
plt.figure()
plt.plot(mc_nr_agents, res_reachability, color="red")
plt.xlabel('Swarm size')
plt.xticks(mc_nr_agents)
plt.ylabel('Reachability')
plt.ylim(0, 1.1)
plt.title('Reachability vs. Swarm size')
plt.grid(True)
plot_path = os.path.join(folder_path, "ReachabilitySwarmSize")
plt.savefig(plot_path)

#Computational Complexity graph 
plt.figure()
plt.plot(mc_nr_agents, res_computational_complexity, color="blue")
plt.xlabel('Swarm size')
plt.xticks(mc_nr_agents)
plt.ylabel('Computational Complexity [s]')
plt.ylim(0, (max(res_computational_complexity)+0.001))
plt.title('Computational Complexity vs. Swarm size')
plt.grid(True)
plot_path = os.path.join(folder_path, "ComplexitySwarmSize")
plt.savefig(plot_path)

#Path length graph 
plt.figure()
plt.plot(mc_nr_agents, res_path_length, color="green")
plt.xlabel('Swarm size')
plt.xticks(mc_nr_agents)
plt.ylabel('Path length [steps]')
plt.ylim(0, (max(res_path_length)+5))
plt.title('Path length vs. Swarm size')
plt.grid(True)
plot_path = os.path.join(folder_path, "PathLengthSwarmSize")
plt.savefig(plot_path)

#Save nr. stuck agents and other results in a text file 



