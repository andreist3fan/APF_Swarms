import os 
import numpy as np 
import matplotlib.pyplot as plt
import Analysis_settings_levels as asl 

#Folders results 
current_dir = os.path.dirname(os.path.abspath(__file__))
folder_path_swarm_L1 = os.path.join(current_dir, "Plots_Results\\L1_Plots_swarm_size")
folder_path_scattering_L1 = os.path.join(current_dir, "Plots_Results\\L1_Plots_scattering")
folder_path_single_L2 = os.path.join(current_dir, "Plots_Results\\L2_Plots_single_agent")
folder_path_swarm_low_L2 = os.path.join(current_dir, "Plots_Results\\L2_Plots_swarm_low_scattering")
folder_path_swarm_high_L2 = os.path.join(current_dir, "Plots_Results\\L2_Plots_swarm_high_scattering")

#Folder to array storage 
folder_storage = os.path.join(current_dir, "Arrays_Storage")

#Graphs for Level 1 (Swarm size)

def plot_L1(swarm, scattering): 

    swarm_values = np.load(os.path.join(folder_storage, "Storage_swarm_size_L1.npy"))
    scattering_values = np.load(os.path.join(folder_storage, "Storage_scattering_L1.npy"))

    values = []
    x_ticks = []
    name = []
    folder = []

    if swarm: 
        values.append(swarm_values)
        x_ticks.append(asl.L1_swarm_sizes)
        name.append("Swarm Size")
        folder.append(folder_path_swarm_L1)

    if scattering: 
        values.append(scattering_values)
        x_ticks.append(asl.L1_scattering)
        name.append("Scattering")
        folder.append(folder_path_scattering_L1)

    for j in range(len(values)): 

        # Path length

        y1, y2, y3 = [], [], []

        for i in range(len(x_ticks[j])): 
            y1.append(sum(x for x in values[j][0][0][i] if x != -1 and x != 0) / sum(1 for x in values[j][0][0][i] if x != -1 and x != 0))
            y2.append(sum(x for x in values[j][0][1][i] if x != -1 and x != 0) / sum(1 for x in values[j][0][1][i] if x != -1 and x != 0))
            y3.append(sum(x for x in values[j][0][2][i] if x != -1 and x != 0) / sum(1 for x in values[j][0][2][i] if x != -1 and x != 0))

        plt.figure()
        plt.plot(x_ticks[j], y1, color="green", label = "obs_dens = 0.04")
        plt.plot(x_ticks[j], y2, color="blue", label = "obs_dens = 0.07")
        plt.plot(x_ticks[j], y3, color="red", label = "obs_dens = 0.1")
        plt.xlabel(name[j])
        plt.ylim(0)
        plt.xticks(x_ticks[j])
        plt.ylabel('Path length')
        plt.title('Path length vs. '+str(name[j]))
        plt.grid(True)
        plt.legend()
        plot_path = os.path.join(folder[j], ("PathLength"))
        plt.savefig(plot_path)

        # Path length (with error bars)

        y1 = []
        y1_err = []

        for i in range(len(x_ticks[j])): 
            y1.append(sum(x for x in values[j][0][0][i] if x != -1 and x != 0) / sum(1 for x in values[j][0][0][i] if x != -1 and x != 0))
            y1_err.append(np.std([x for x in values[j][0][0][i] if x != 0]))

        plt.figure()
        plt.plot(x_ticks[j], y1, color="green")
        plt.errorbar(x_ticks[j], y1, yerr = y1_err)
        plt.xlabel(name[j])
        plt.ylim(0)
        plt.xticks(x_ticks[j])
        plt.ylabel('Path length')
        plt.title('Path length vs. '+str(name[j]))
        plt.grid(True)
        plot_path = os.path.join(folder[j], ("PathLength (Error Bars)"))
        plt.savefig(plot_path)

        # Effective path length 

        y1, y2, y3 = [], [], []

        for i in range(len(x_ticks[j])): 
            y1.append(sum(x for x in values[j][1][0][i] if x != -1 and x != 0) / sum(1 for x in values[j][1][0][i] if x != -1 and x != 0))
            y2.append(sum(x for x in values[j][1][1][i] if x != -1 and x != 0) / sum(1 for x in values[j][1][1][i] if x != -1 and x != 0))
            y3.append(sum(x for x in values[j][1][2][i] if x != -1 and x != 0) / sum(1 for x in values[j][1][2][i] if x != -1 and x != 0))

        plt.figure()
        plt.plot(x_ticks[j], y1, color="green", label = "obs_dens = 0.04")
        plt.plot(x_ticks[j], y2, color="blue", label = "obs_dens = 0.07")
        plt.plot(x_ticks[j], y3, color="red", label = "obs_dens = 0.1")
        plt.xlabel(name[j])
        plt.xticks(x_ticks[j])
        plt.ylim(1)
        plt.ylabel('Effective Path length')
        plt.title('Effective Path length vs. '+str(name[j]))
        plt.grid(True)
        plt.legend()
        plot_path = os.path.join(folder[j], ("EffectivePathLength"))
        plt.savefig(plot_path)

        # Effective path length (Error bars)

        y1 = []
        y1_err = []

        for i in range(len(x_ticks[j])): 
            y1.append(sum(x for x in values[j][1][0][i] if x != -1 and x != 0) / sum(1 for x in values[j][0][0][i] if x != -1 and x != 0))
            y1_err.append(np.std([x for x in values[j][1][0][i] if x != 0]))

        plt.figure()
        plt.plot(x_ticks[j], y1, color="green")
        plt.errorbar(x_ticks[j], y1, yerr = y1_err)
        plt.xlabel(name[j])
        plt.xticks(x_ticks[j])
        plt.ylim(1)
        plt.ylabel('Effective Path length')
        plt.title('Effective Path length vs. '+str(name[j]))
        plt.grid(True)
        plot_path = os.path.join(folder[j], ("EffectivePathLength (Error Bars)"))
        plt.savefig(plot_path)

        # Computational complexity 

        y1, y2, y3 = [], [], []

        for i in range(len(x_ticks[j])): 
            y1.append(sum(x for x in values[j][2][0][i] if x != -1 and x != 0) / sum(1 for x in values[j][2][0][i] if x != -1 and x != 0))
            y2.append(sum(x for x in values[j][2][1][i] if x != -1 and x != 0) / sum(1 for x in values[j][2][1][i] if x != -1 and x != 0))
            y3.append(sum(x for x in values[j][2][2][i] if x != -1 and x != 0) / sum(1 for x in values[j][2][2][i] if x != -1 and x != 0))

        plt.figure()
        plt.plot(x_ticks[j], y1, color="green", label = "obs_dens = 0.04")
        plt.plot(x_ticks[j], y2, color="blue", label = "obs_dens = 0.07")
        plt.plot(x_ticks[j], y3, color="red", label = "obs_dens = 0.1")
        plt.xlabel(name[j])
        plt.xticks(x_ticks[j])
        plt.ylim(0)
        plt.ylabel('Computational Complexity')
        plt.title('Computational Complexity vs. '+str(name[j]))
        plt.grid(True)
        plt.legend()
        plot_path = os.path.join(folder[j], ("ComputationalComplexity"))
        plt.savefig(plot_path)

        # Computational complexity (Error Bars)

        y1 = []
        y1_err = []

        for i in range(len(x_ticks[j])): 
            y1.append(sum(x for x in values[j][2][0][i] if x != -1 and x != 0) / sum(1 for x in values[j][0][0][i] if x != -1 and x != 0))
            y1_err.append(np.std([x for x in values[j][2][0][i] if x != 0]))

        plt.figure()
        plt.plot(x_ticks[j], y1, color="green")
        plt.errorbar(x_ticks[j], y1, yerr = y1_err)
        plt.xlabel(name[j])
        plt.xticks(x_ticks[j])
        plt.ylim(0)
        plt.ylabel('Computational Complexity')
        plt.title('Computational Complexity vs. '+str(name[j]))
        plt.grid(True)
        plot_path = os.path.join(folder[j], ("ComputationalComplexity (Error Bars)"))
        plt.savefig(plot_path)

        # Reachability 

        y1, y2, y3 = [], [], []

        for i in range(len(x_ticks[j])): 
            y1.append(sum(x for x in values[j][3][0][i] if x != -1) / sum(1 for x in values[j][3][0][i] if x != -1))
            y2.append(sum(x for x in values[j][3][1][i] if x != -1) / sum(1 for x in values[j][3][1][i] if x != -1))
            y3.append(sum(x for x in values[j][3][2][i] if x != -1) / sum(1 for x in values[j][3][2][i] if x != -1))

        plt.figure()
        plt.plot(x_ticks[j], y1, color="green", label = "obs_dens = 0.04")
        plt.plot(x_ticks[j], y2, color="blue", label = "obs_dens = 0.07")
        plt.plot(x_ticks[j], y3, color="red", label = "obs_dens = 0.1")
        plt.xlabel(name[j])
        plt.xticks(x_ticks[j])
        plt.ylim(0, 1.05)
        plt.ylabel('Reachability')
        plt.title('Reachability vs. '+str(name[j]))
        plt.grid(True)
        plt.legend()
        plot_path = os.path.join(folder[j], ("Reachability"))
        plt.savefig(plot_path)

def plot_L2(nr_alg): 

    #data = np.load(os.path.join(folder_storage, "Storage_L2.npy"))
    data = np.load(os.path.join(folder_storage, "Storage_L2_missing _A_star.npy"))

    #values = []
    x_ticks = asl.L2_obstacle_numbers 
    name = ["Single agent", "Swarm low scattering", "Swarm high scattering"]
    folder = [folder_path_single_L2, folder_path_swarm_low_L2, folder_path_swarm_high_L2]

    color = ["pink", "blue", "red", "orange", "green"]
    alg_name = ["CAPF", "BAPF", "CR-BAPF*", "RAPF", "A*"]

    for j in range(3): 
    
        # Array_L2[performance parameter][obstacle_density][swarm][algorithm][run]

        # Path length

        y = [] 

        for i in range(nr_alg):
            y.append([])

        for i in range(len(x_ticks)): 
            for k in range(nr_alg): 
                y[k].append(sum(x for x in data[0][i][j][k] if x != -1 and x != 0) / sum(1 for x in data[0][i][j][k] if x != -1 and x != 0))
            
        plt.figure()
        
        for i in range(len(y)): 
            plt.plot(x_ticks, y[i], color[i], label = alg_name[i]) 
        plt.xlabel("Obstacle number")
        plt.ylim(0)
        plt.xticks(x_ticks)
        plt.ylabel('Path length')
        plt.title('Path length vs. Obstacle density ('+str(name[j])+")")
        plt.grid(True)
        plt.legend()
        plot_path = os.path.join(folder[j], ("PathLength"))
        plt.savefig(plot_path)

        # Effective path length 

        y = [] 

        for i in range(nr_alg):
            y.append([])

        for i in range(len(x_ticks)): 
            for k in range(nr_alg): 
                y[k].append(sum(x for x in data[1][i][j][k] if x != -1 and x != 0) / sum(1 for x in data[1][i][j][k] if x != -1 and x != 0))
                
        plt.figure()
        for i in range(len(y)): 
            plt.plot(x_ticks, y[i], color[i], label = alg_name[i]) 
        plt.xlabel("Obstacle number")
        plt.ylim(0)
        plt.xticks(x_ticks)
        plt.ylim(1)
        plt.ylabel('Effective Path length')
        plt.title('Effective Path length vs. Obstacle density ('+str(name[j])+")")
        plt.grid(True)
        plt.legend()
        plot_path = os.path.join(folder[j], ("EffectivePathLength"))
        plt.savefig(plot_path)

        # Computational complexity 

        y = [] 

        for i in range(nr_alg):
            y.append([])

        for i in range(len(x_ticks)): 
            for k in range(nr_alg): 
                y[k].append(sum(x for x in data[2][i][j][k] if x != -1 and x != 0) / sum(1 for x in data[2][i][j][k] if x != -1 and x != 0))
            
        plt.figure()
        for i in range(len(y)): 
            plt.plot(x_ticks, y[i], color[i], label = alg_name[i]) 
        plt.xlabel("Obstacle number")
        plt.ylim(0)
        plt.xticks(x_ticks)
        plt.ylim(0)
        plt.ylabel('Computational Complexity')
        plt.title('Computational Complexity vs. Obstacle density ('+str(name[j])+")")
        plt.grid(True)
        plt.legend()
        plot_path = os.path.join(folder[j], ("ComputationalComplexity"))
        plt.savefig(plot_path)

        # Reachability 

        y = [] 

        for i in range(nr_alg):
            y.append([])

        for i in range(len(x_ticks)): 
            for k in range(nr_alg): 
                y[k].append(sum(x for x in data[3][i][j][k] if x != -1) / sum(1 for x in data[3][i][j][k] if x != -1))

        plt.figure()
        for i in range(len(y)): 
            plt.plot(x_ticks, y[i], color[i], label = alg_name[i]) 
        plt.xlabel("Obstacle number")
        plt.ylim(0)
        plt.xticks(x_ticks)
        plt.ylim(0, 1.05)
        plt.ylabel('Reachability')
        plt.title('Reachability vs. Obstacle density ('+str(name[j])+")")
        plt.grid(True)
        plt.legend()
        plot_path = os.path.join(folder[j], ("Reachability"))
        plt.savefig(plot_path)
    


#---------------Run functions---------------------


#plot_L1(True, True)
plot_L2(4)

