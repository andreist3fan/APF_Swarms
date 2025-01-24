
#!!!
#Please dont change the values of the parameters in this file since multiple main functions assume these default values 
#To run a setup with a different setting, change the values in an object, not the class itself 
#!!!

class Setup: 

    def __init__(self, algorithm):

        self.name = "Run_1"

        #Visualise run in pygame (! Influences speed of simulation)
        self.visual = False 


        #------Fill in----------------------------- 

        #Point around which agents are initially scattered 
        self.agents_start_x = 5
        self.agents_start_y = 5
        self.start_radius = 3 #Radius of circle that represents area where agents start

        self.smart_swarm = False #If one agent reaches a local minimum, that point is added to the obstacle list of the environment

        #Agents 
        self.nr_agents = 1
        self.algorithm = algorithm

        #0: CAPF 
        #1: BAPF
        self.N_bacteria = 60
        #2: CR-BAPF
        #3: RAPF
        self.N_bacteria_RAPF = 8
        #4: A*

        #Reachability/Stuck agents 
        self.time_limit = 10 #If simulation takes longer, reachability is set to 0
        self.delete_stuck = True #If an agent gets stuck, ignore it in the further process (assumes that there is no way to unstuck it)
        self.nr_stuck_agents = 0 
        #------------Environment--------------------------

        #Sqaured total size in m 
        self.area_size = 30

        #Target
        self.target_x = 25
        self.target_y = 25
        self.target_radius = 0.5

        #lower and upper bound for number of obstacles 
        self.obst_N_lower = 60 #influenced by values in paper 
        self.obst_N_upper = 80 

        #-------------Agents-----------------------------------

        # Movement
        self.step_size = 0.4
        self.step_variance = 0.01

        #--------------Hyperparameter from paper----------------

        # Simulation Hyperparameter values (from https://ieeexplore-ieee-org.tudelft.idm.oclc.org/document/10115857)
        self.range = 8
        self.obst_radius_inner = 0.6
        self.obst_radius_outer = 4.5
        self.alpha_t = 100
        self.mu_t = 0.002
        self.alpha_o = 8
        self.mu_o = 1.5
        

        #--------------Performance matrix----------------------------- 

        self.target = False #True as soon as one agent reaches target 
        # Note by Rens: I feel like this variable belongs in main.py, since it is constantly switched between False and True between runs (and setup should contain constants right?)
        #Response by Firine: Since we assume that the reachibility will be 100% (we stop the simulation only if an agent has reached the target), it could be in main. But I think we will 
        #store the evaluation parameters (path length and computational complexity) also in Setup, so it might be nice to also have it here. Doesnt really matter I guess 

        self.path_length = 0 
        self.computational_complexity = 0 
        self.min_distance_target = 0 

