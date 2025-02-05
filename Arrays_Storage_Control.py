import numpy as np
import os 

# ----------Level 1-----------------------------------------------------------

# Array_swarm_size_L1[performance parameter][obstacle_density][swarm_size][run]
# Array_scattering_L1[performance parameter][obstacle_density][scattering][run]

# Performance Parameter: 0 (path_length) | 1(eff_path_length) | 2(computational_complexity) | 3(reachability)

# Obstacle density: 0 (0.04) | 1(0.07) | 2 (0.1)

# Swarm_size:  0(1) | 1(2) | 2(3) | 3(5) | 4(10) | 5(15) | 6(20) | 7(25)

# Scattering: 0(2) | 1(3) | 2(5) | 3(7.5) | 4(10)

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

# Add data to storage files 

def add_data_L1(file_name, performance_parameter_ind, obstacle_density_ind, swarm_or_scattering_ind, data): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")
    file_path = os.path.join(folder_path, file_name)

    re = np.load(file_path)

    start = np.argmax(re[performance_parameter_ind, obstacle_density_ind, swarm_or_scattering_ind] == -1)
    print(start)

    open_spaces = 999-start

    if len(data) > open_spaces: 
        print("That setting has more than 1,000 runs. Only "+str(open_spaces)+" more data points added.")
        data = data[0:(open_spaces-1)]

    re[performance_parameter_ind, obstacle_density_ind, swarm_or_scattering_ind, start:(start+len(data))] = data

    np.save(file_path, re)

def overview_scat_L1(): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")

    scattering = np.load(os.path.join(folder_path, "Storage_scattering_L1.npy"))

    print("Amount of runs for scattering: ")
    print("Obstacle setting 0: "+str(np.argmax(scattering[0,0,0] == -1)))
    print("Obstacle setting 1: "+str(np.argmax(scattering[0,1,0] == -1)))
    print("Obstacle setting 2: "+str(np.argmax(scattering[0,2,0] == -1)))

def overview_swarm_size_L1(): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")

    swarm = np.load(os.path.join(folder_path, "Storage_swarm_size_L1.npy"))

    print("Amount of runs for swarm size: ")
    print("Obstacle setting 0: "+str(np.argmax(swarm[0,0,0] == -1)))
    print("Obstacle setting 1: "+str(np.argmax(swarm[0,1,0] == -1)))
    print("Obstacle setting 2: "+str(np.argmax(swarm[0,2,0] == -1)))

# ----------Level 2-----------------------------------------------------------

# Array_L2[performance parameter][obstacle_density][swarm][algorithm][run]

# Performance Parameter: 0 (path_length) | 1(eff_path_length) | 2(computational_complexity) | 3(reachability)

# Obstacle density: 0() | 1() | 2() | 3() | 4()

# Swarm: 0(single agent) | 1 (swarm, low scattering) | 2 (swarm, high scattering)

# Algorithm: 0(CAPF) | 1 (BAPF) | 2(CR-BAPF*) | 3(RAPF) | 4(A*)

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

# Add data to storage files 

def add_data_L2(performance_parameter_ind, obstacle_density_ind, swarm_setting_ind, algorithm, data): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")
    file_path = os.path.join(folder_path, 'Storage_L2.npy')

    re = np.load(file_path)

    start = np.argmax(re[performance_parameter_ind, obstacle_density_ind, swarm_setting_ind, algorithm] == -1)
    print(start)

    open_spaces = 999-start

    if len(data) > open_spaces: 
        print("That setting has more than 1,000 runs. Only "+str(open_spaces)+" more data points added.")
        data = data[0:(open_spaces-1)]

    re[performance_parameter_ind, obstacle_density_ind, swarm_setting_ind, algorithm, start:(start+len(data))] = data

    np.save(file_path, re)

def overview_L2(): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")

    swarm = np.load(os.path.join(folder_path, "Storage_L2.npy"))

    print("Amount of runs for L2: ")

    for obs in range(5): 
        print("Obstacle setting "+str(obs)+ ": "+str(np.argmax(swarm[0,obs,0,0] == -1)))

def clean_L2(): 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "Arrays_Storage")
    storage_L2 = np.load(os.path.join(folder_path, "Storage_L2.npy"))

    #Clean level (delete unfinished runs)
    mask = storage_L2 != -1
    count_not_minus_one = mask.sum(axis=0)
    mixed_indices = (count_not_minus_one != 0) & (count_not_minus_one != storage_L2.shape[0])
    storage_L2[:, mixed_indices] = -1     # Reset all values to -1 where an inconsistency is found

    print("Mixed indices: ")
    print(mixed_indices)

    np.save(folder_path, storage_L2)

#------------------Level universal functions-------------------

# Create average of run 

def avg(run): 
    amount = np.argmax(run, -1)
    x = 0
    for i in range(amount): 
        x += run[i]
    x = x/(amount)
    return x
    

# Analyse two variables 

#def line_graph(x_arrays, y_arrays, legends): 

    
#-------------------Run functions---------------------------------------------
create_empty_storage_L1()
create_empty_storage_L2()

print("")

current_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(current_dir, "Arrays_Storage")
#file_path = os.path.join(folder_path, 'Storage_scattering_L1.npy')
#file_path = os.path.join(folder_path, 'Storage_swarm_size_L1.npy')
file_path = os.path.join(folder_path, 'Storage_L2.npy')

re = np.load(file_path)

# Level 1: [performance parameter][obstacle_density][scattering][run]
# Level 2: [performance parameter][obstacle_density][swarm][algorithm][run]

#---------------------------------------------------------------

overview_scat_L1()
overview_swarm_size_L1()

#overview_L2()
#clean_L2()



