import numpy as np
import os 

# ----------Level 1-----------------------------------------------------------

# Array_swarm_size_L1[obstacle_density][swarm_size][run]
# Array_scattering_L1[obstacle_density][scattering][run]

# Obstacle density: 0 (0.04) | 1(0.07) | 2 (0.1)

# Swarm_size:  0(1) | 1(2) | 2(3) | 3(5) | 4(10) | 5(15) | 6(20) | 7(25)

# Scattering: 0(2) | 1(3) | 2(5) | 3(7.5) | 4(10)

def create_empty_storage_L1(): 

    #Create performance parameter 
    reachability_swarm_size_L1 = np.full((3, 8, 1000), -1)
    computational_complexity_swarm_size_L1 = np.full((3, 8, 1000), -1)
    path_length_swarm_size_L1 = np.full((3, 8, 1000), -1)
    eff_path_length_swarm_size_L1 = np.full((3, 8, 1000), -1)

    reachability_scattering_L1 = np.full((3, 5, 1000), -1)
    computational_scattering_L1 = np.full((3, 5, 1000), -1)
    path_length_swarm_scattering_L1 = np.full((3, 5, 1000), -1)
    eff_path_length_scattering_L1 = np.full((3, 5, 1000), -1)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")

    names = ['reachability_swarm_size_L1.npy', 'computational_complexity_swarm_size_L1.npy', 'path_length_swarm_size_L1.npy', 'eff_path_length_swarm_size_L1.npy', 'reachability_scattering_L1.npy', 'computational_scattering_L1.npy', 'path_length_swarm_scattering_L1.npy', 'eff_path_length_scattering_L1.npy']
    pp = [reachability_swarm_size_L1, computational_complexity_swarm_size_L1, path_length_swarm_size_L1, eff_path_length_swarm_size_L1, reachability_scattering_L1, computational_scattering_L1, path_length_swarm_scattering_L1, eff_path_length_scattering_L1]
    
    for i in range(len(names)): 
        file_path = os.path.join(folder_path, names[i])
        if not os.path.exists(file_path):
            np.save(file_path, pp[i])
        else: 
            print(str(names[i])+" already exists.")

# ----------Level 2-----------------------------------------------------------

# Array_L2[obstacle_density][swarm][algorithm][run]

# Obstacle density: 0() | 1() | 2() | 3() | 4()

# Swarm: 0(single agent) | 1 (swarm, low scattering) | 2 (swarm, high scattering)

# Algorithm: 0(CAPF) | 1 (BAPF) | 2(CR-BAPF*) | 3(RAPF) | 4(A*)

def create_empty_storage_L2(): 

    #Create performance parameter 
    reachability_L2 = np.full((5, 3, 5, 1000), -1)
    computational_complexity_L2 = np.full((5, 3, 5, 1000), -1)
    path_length_L2 = np.full((5, 3, 5, 1000), -1)
    eff_path_length_L2 = np.full((5, 3, 5, 1000), -1)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")

    names = ['reachability_L2.npy', 'computational_complexity_L2.npy', 'path_length_L2.npy', 'eff_path_length_L2.npy']
    pp = [reachability_L2, computational_complexity_L2, path_length_L2, eff_path_length_L2]
    
    for i in range(4): 
        file_path = os.path.join(folder_path, names[i])
        if not os.path.exists(file_path):
            np.save(file_path, pp[i])
        else: 
            print(str(names[i])+" already exists.")

#Add data to overall file 

def add_data(file_name, obstacle_density, swarm_setting, algorithm, data): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")
    file_path = os.path.join(folder_path, file_name)

    re = np.load(file_path)

    start = np.argmax(re[obstacle_density, swarm_setting, algorithm] == -1)
    print(start)

    if start+len(data) > 999: 
        print("That setting has more than 1,000 runs (not more data stored)")

    re[obstacle_density, swarm_setting, algorithm, start:(start+len(data))] = data
    print(re)

    np.save(file_path, re)


#-------------------Run functions----------------------------------------------

create_empty_storage_L1()
create_empty_storage_L2()