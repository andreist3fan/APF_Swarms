class Setup: 

    def __init__(self):

        self.name = "Run_1"

        #Visualise run in pygame (! Influences speed of simulation)
        self.visual = False 

        #------Fill in----------------------------- 

        #Agents 
        self.nr_agents = 1
        self.algorithm = 3

        #Point around which agents are initially scattered 
        self.agents_start_x = 3
        self.agents_start_y = 3
        self.start_radius = 3 #Radius of circle that represents area where agents start

        #0: CAPF 
        #1: BAPF
        self.N_bacteria = 60
        #2: CR-BAPF
        #3: RAPF
        self.N_bacteria_RAPF = 8
        #4: A*

        #------------Environment--------------------------

        #Sqaured total size in m 
        self.area_size = 30

        #Target
        self.target_x = 22
        self.target_y = 22
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
        self.obst_radius_inner = 0.4
        self.obst_radius_outer = 4.5

        # Unfortunately, these parameters are highly dependent on the APF algorithm to work.
       
        if self.algorithm == 0:
            self.alpha_t = 10000 * 1
            self.mu_t = 1 * 0.001
            self.alpha_o = 1 * 300 #was 1, changed it (no specific reason why this value) to see the influence of obstacles in the simulation
            self.mu_o = 1000 * 0.001
        elif self.algorithm == 1:
            self.alpha_t = 10000
            self.mu_t = 1
            self.alpha_o = 1 * 40   # Still trying to find the optimum
            self.mu_o = 1000 * 0.2  # Still trying to find the optimum
        else:
            self.alpha_t = 10000
            self.mu_t = 1
            self.alpha_o = 1
            self.mu_o = 1000
        

        #--------------Performance matrix----------------------------- 

        self.target = False #True as soon as one agent reaches target 
        # Note by Rens: I feel like this variable belongs in main.py, since it is constantly switched between False and True between runs (and setup should contain constants right?)
        #Response by Firine: Since we assume that the reachibility will be 100% (we stop the simulation only if an agent has reached the target), it could be in main. But I think we will 
        #store the evaluation parameters (path length and computational complexity) also in Setup, so it might be nice to also have it here. Doesnt really matter I guess 

        self.path_length = 0 
        self.computational_complexity = 0 

