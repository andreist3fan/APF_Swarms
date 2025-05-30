# Setups and handels storing the results of the Monte Carlo runs 

import numpy as np
import os 
import matplotlib.pyplot as plt 
import Analysis_settings_levels as asl

# ----------Level 1-----------------------------------------------------------

# Array_swarm_size_L1[performance parameter][obstacle_density][swarm_size][run]
# Array_scattering_L1[performance parameter][obstacle_density][scattering][run]

# Performance Parameter: 0 (path_length) | 1(eff_path_length) | 2(computational_complexity) | 3(reachability)

# Obstacle density: 0 (0.04) | 1(0.07) | 2 (0.1)

# Swarm_size:  0(1) | 1(2) | 2(3) | 3(5) | 4(10) | 5(15) | 6(20) | 7(25)

# Scattering: 0(2) | 1(3) | 2(5) | 3(7.5) | 4(10)

# Create storage for Level 1 

def create_empty_storage_L1(): 

    #Create performance parameter 
    storage_swarm_size_L1 = np.full((4, 3, 8, 1000), -1.0)
    storage_scattering_L1 = np.full((4, 3, 5, 1000), -1.0)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")

    names = ['Storage_swarm_size_L1.npy', 'Storage_scattering_L1.npy'] 
    pp = [storage_swarm_size_L1, storage_scattering_L1] 
    
    for i in range(len(names)): 
        file_path = os.path.join(folder_path, names[i])
        if not os.path.exists(file_path):
            np.save(file_path, pp[i])
        else: 
            print(str(names[i])+" already exists.")

# Add data to storage file level 1 

def add_data_L1(file_name, performance_parameter_ind, obstacle_density_ind, swarm_or_scattering_ind, data): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")
    file_path = os.path.join(folder_path, file_name)

    re = np.load(file_path)

    if re[performance_parameter_ind, obstacle_density_ind, swarm_or_scattering_ind, -1]==-1:
        start = np.argmax(re[performance_parameter_ind, obstacle_density_ind, swarm_or_scattering_ind] == -1)
        print(start)

        open_spaces = 1000 - start

        if len(data) > open_spaces: 
            print("That setting has more than 1,000 runs. Only "+str(open_spaces)+" more data points added.")
            data = data[0:(open_spaces)]

        re[performance_parameter_ind, obstacle_density_ind, swarm_or_scattering_ind, start:(start+len(data))] = data

        np.save(file_path, re)
    else: 
        print("Setting is full.")

# Print overview of Level 1 results (effect of starting radius)

def overview_scat_L1(): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")

    scattering = np.load(os.path.join(folder_path, "Storage_scattering_L1.npy"))

    print("Amount of runs for scattering: ")
    print("Obstacle setting 0: "+str(sum(1 for x in scattering[0,0,0] if x != -1)))
    print("Obstacle setting 1: "+str(sum(1 for x in scattering[0,1,0] if x != -1)))
    print("Obstacle setting 2: "+str(sum(1 for x in scattering[0,2,0] if x != -1)))

# Print overview of Level 1 results (effect of swarm size)

def overview_swarm_size_L1(): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")

    swarm = np.load(os.path.join(folder_path, "Storage_swarm_size_L1.npy"))

    print("Amount of runs for swarm size: ")
    print("Obstacle setting 0: "+str(sum(1 for x in swarm[0,0,0] if x != -1)))
    print("Obstacle setting 1: "+str(sum(1 for x in swarm[0,1,0] if x != -1)))
    print("Obstacle setting 2: "+str(sum(1 for x in swarm[0,2,0] if x != -1)))

# ----------Level 2-----------------------------------------------------------

# Array_L2[performance parameter][obstacle_density][swarm][algorithm][run]

# Performance Parameter: 0 (path_length) | 1 (eff_path_length) | 2 (computational_complexity) | 3 (reachability)

# Obstacle density: 0() | 1() | 2() | 3() | 4()

# Swarm: 0(single agent) | 1 (swarm, low scattering) | 2 (swarm, high scattering)

# Algorithm: 0(CAPF) | 1 (BAPF) | 2(CR-BAPF*) | 3(RAPF) | 4(A*)

# Create storage for level 2

def create_empty_storage_L2(): 

    #Create performance parameter 
    storage_L2 = np.full((4, 5, 3, 5, 1000), -1.0)
    name = 'Storage_L2.npy'

    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")
    file_path = os.path.join(folder_path, name)
    if not os.path.exists(file_path):
        np.save(file_path, storage_L2)
    else: 
        print(str(name)+" already exists.")

# Function that investigates error with outliers in computational complexity due to background programs of computing device 

def clean_obs_dens(storage_file): 
    data = re = np.load(file_path)
    for perf_idx in range(len(data)):
        if len(data[perf_idx]) > 1:  # Ensure obstacle_density index 2 exists
            for swarm_idx in range(len(data[perf_idx][2])):
                for algo_idx in range(len(data[perf_idx][2][swarm_idx])):
                    for run_idx in range(len(data[perf_idx][2][swarm_idx][algo_idx])):
                        data[perf_idx][3][swarm_idx][algo_idx][run_idx] = -1

    np.save(storage_file, data)
    print("Updated with deleted obstacle density")

# Add data to storage files for level 2 

def add_data_L2(performance_parameter_ind, obstacle_density_ind, swarm_setting_ind, algorithm, data): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")
    #file_path = os.path.join(folder_path, 'Storage_L2.npy')
    file_path = os.path.join(folder_path, 'Storage_L2.npy')
    re = np.load(file_path)
    
    if re[performance_parameter_ind, obstacle_density_ind, swarm_setting_ind, algorithm, -1]==-1:
        start = np.argmax(re[performance_parameter_ind, obstacle_density_ind, swarm_setting_ind, algorithm] == -1)
        print("Start: "+str(start))

        open_spaces = 1000 - start

        if len(data) > open_spaces: 
            print("That setting has more than 1,000 runs. Only "+str(open_spaces)+" more data points added.")
            data = data[0:(open_spaces)]

        re[performance_parameter_ind, obstacle_density_ind, swarm_setting_ind, algorithm, start:(start+len(data))] = data
        print("Saved something")

        np.save(file_path, re)
    else: 
        print("Setting is full.")

# Print overview of Level 2 results 

def overview_L2(): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")

    swarm = np.load(os.path.join(folder_path, "Storage_L2.npy"))

    print("Amount of runs for L2: ")

    for obs in range(5): 
        print("Obstacle setting "+str(obs)+ ": "+str(sum(1 for x in swarm[0,obs,0,0] if x != -1)))

# ----------Level 3-----------------------------------------------------------

# Array_L3[performance parameter][swarm][collision][run]

# Performance Parameter: 0 (path_length) | 1 (eff_path_length) | 2 (computational_complexity) | 3 (reachability)

# Swarm: 0(single agent) | 1 (swarm, low scattering) | 2 (swarm, high scattering)

# Collision: 0 (None) | 1 (Bumper method) | 2 (Obstacle method) | 3 (Teardrop method) 

# Create storage file for level 3 (Version 1)

def create_empty_storage_L3(): 

    #Create performance parameter 
    swarm_int = len(asl.L3_swarm_size)
    collision_int = len(asl.L3_algorithm)
    storage_L3 = np.full((4, swarm_int, collision_int, 1000), -1.0)
    name = 'Storage_L3.npy'

    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")
    file_path = os.path.join(folder_path, name)
    if not os.path.exists(file_path):
        np.save(file_path, storage_L3)
    else: 
        print(str(name)+" already exists.")

# Create storafe file for level 3 (Version 2)

def create_empty_storage_L3_2(): 
    #Create performance parameter 
    swarm_int = len(asl.L3_2_swarm_size)
    collision_int = len(asl.L3_algorithm)
    storage_L3 = np.full((4, swarm_int, collision_int, 1000), -1.0)
    name = 'Storage_L3_2.npy'

    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")
    file_path = os.path.join(folder_path, name)
    if not os.path.exists(file_path):
        np.save(file_path, storage_L3)
    else: 
        print(str(name)+" already exists.")


# Add data to storage file for level 3 

def add_data_L3(performance_parameter_ind, swarm_setting_ind, collision, data, file): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")
    file_path = os.path.join(folder_path, file)

    re = np.load(file_path)
    
    if re[performance_parameter_ind, swarm_setting_ind, collision, -1]==-1:
        start = np.argmax(re[performance_parameter_ind, swarm_setting_ind, collision] == -1)
        print("Start: "+str(start))

        open_spaces = 1000 - start

        if len(data) > open_spaces: 
            print("That setting has more than 1,000 runs. Only "+str(open_spaces)+" more data points added.")
            data = data[0:(open_spaces)]

        re[performance_parameter_ind, swarm_setting_ind, collision, start:(start+len(data))] = data
        print("Saved something")

        np.save(file_path, re)
    else: 
        print("Setting is full.")

# Give overview of level 3 simulation (Version 1)

def overview_L3(): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")

    data = np.load(os.path.join(folder_path, "Storage_L3.npy"))

    print("Amount of runs for L3: ")
 
    print("Number runs: "+str(sum(1 for x in data[0,0,0] if x != -1)))

# Give overview of level 3 simulation (Version 2)

def overview_L3_2(): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")

    data = np.load(os.path.join(folder_path, "Storage_L3_2.npy"))

    print("Amount of runs for L3_2: ")
 
    print("Number runs: "+str(sum(1 for x in data[0,0,0] if x != -1)))


#------------------Level universal functions-------------------

# Create average of all runs for one setting 

def avg(run): 
    amount = np.argmax(run, -1)
    x = 0
    for i in range(amount): 
        x += run[i]
    x = x/(amount)
    return x    

#-------------------Run functions---------------------------------------------

# Creates storage for levels, if they do not exist yet 

create_empty_storage_L1()
create_empty_storage_L2()
create_empty_storage_L3()
create_empty_storage_L3_2()

# Print status of every simulation level

overview_scat_L1()
overview_swarm_size_L1()
overview_L2()
overview_L3()
overview_L3_2()



