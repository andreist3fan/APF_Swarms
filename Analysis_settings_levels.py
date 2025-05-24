# Stores numerical values for settings of the different levels 

#---------------Level 1--------------------------

# Environment settings 
L1_obstacle_number = [50, 80, 110] 

# Analysis effect of swarm size
L1_swarm_sizes = [1, 2, 3, 5, 10, 15, 20, 25]     #Number of agents  
L1_sws_scattering = 5

# Analysis of effect of starting radius 
L1_scattering = [2, 3, 5, 7.5, 10]                # Scattering radius around center (not smaller than 2)
L1_fixed_swarm_size = 5

# Algorithm: CAPF 
L1_algorithm = 0 

#----------------Level 2-------------------------

# Environment settings 
L2_obstacle_numbers = [75, 125, 175, 225, 275]

# Swarm settings 
L2_swarm_size = [1, 5, 5]
L2_scattering = [3, 3, 10]

# Different algorithms 
L2_algorithm = [0, 1, 2, 3, 4]

#---------------Level 3--------------------------

#Environment settings 
L3_obs_number = 200

# Swarm settings (original Level 3)
L3_swarm_size = [5, 5, 10]
L3_scattering = [3, 10, 10]
L3_swarm_options = ["size: 5, scattering: 3", "size: 5, scattering: 10", "size: 10, scattering: 10"]

#Swarm settings (updated Level 3)
L3_2_swarm_size = [2, 5, 10, 15, 20, 5, 5, 5, 5, 5]
L3_2_swarm_analysis = [2, 5, 10, 15, 20]
L3_2_scattering = [5, 5, 5, 5, 5, 2, 3, 5, 7.5, 10]
L3_2_scat_analysis = [2, 3, 5, 7.5, 10]

# Algorithms: RAPF with no/different collision methods 
L3_algorithm = [3, 5, 6, 7]




