class Setup: 

    def __init__(self):

        self.name = "Run_1"

        #------Fill in----------------------------- 

        #Agents 
        self.nr_agents = 1
        self.algorithm = 0 

        #0: CAPF 
        #1: BAPF
        #2: CR-BAPF
        #3: RAPF 
        #4: A*

        #Environment 
        self.target_x = 20
        self.target_y = 20
        self.target_radius = 0.5

        # Movement
        self.step_size = 0.4
        self.step_variance = 0.01

        # Simulation Hyperparameter values (from https://ieeexplore-ieee-org.tudelft.idm.oclc.org/document/10115857)
        self.range = 8
        self.alpha_t = 10000
        self.mu_t = 1 * 0.001
        self.alpha_o = 1
        self.mu_o = 1000 * 0.001
        self.obst_radius_inner = 0.4
        self.obst_radius_outer = 4.5

        #Other 
        self.target = False #True as soon as one agent reaches target 
        # Note by Rens: I feel like this variable belongs in main.py, since it is constantly switched between False and True between runs (and setup should contain constants right?)




