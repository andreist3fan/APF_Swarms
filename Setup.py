
#!!!
#Please dont change the values of the parameters in this file since multiple main functions assume these default values 
#To run a setup with a different setting, change the values in an object, not the class itself 
#!!!

class Setup: 

    def __init__(self, algorithm):

        self.name = "Run_1"

        #-------------Agents-----------------------------------

        #Agent characteristics
        self.agent_radius = 0.2
        self.step_size = 0.4
        self.step_variance = 0.01
        self.algorithm = algorithm

        #0: CAPF 
        #1: BAPF
        self.N_bacteria = 60
        #2: CR-BAPF*
        self.random_walk_length = 3
        #3: RAPF
        self.N_bacteria_RAPF = 16
        #4: A*
        self.grid_fineness = 10

        #Swarm characteristics
        self.smart_swarm = False #If one agent reaches a local minimum, that point is added to the obstacle list of the environment
        self.nr_agents = 5

        #Reachability/Stuck agents
        self.time_limit = 10 #If simulation takes longer, reachability is set to 0
        self.delete_stuck = True #If an agent gets stuck, ignore it in the further process (assumes that there is no way to unstuck it)
        self.nr_stuck_agents = 0
        self.nr_hit_agents = 0

        #------------Environment--------------------------

        #Length of square (m)
        self.area_size = 35

        #Point around which agents are initially scattered
        self.agents_start_x = 10
        self.agents_start_y = 10
        self.start_radius = 5      #Radius of circle that represents area where agents start (scattering)

        #Target
        self.target_x = 30
        self.target_y = 30
        self.target_radius = 0.5

        #Obstacles
        self.obst_radius = 0.6
        self.obstacle_number = 70  

        #--------------Hyperparameter-------------------------

        # Simulation Hyperparameter values
        self.range = 8
        self.obst_radius_inner = 0.6
        self.obst_radius_outer = 4.5
        self.alpha_t = 100
        self.mu_t = 0.002
        self.alpha_o = 8
        self.mu_o = 1.5
        self.alpha_a = 5  
        self.mu_a = 0.2
        self.agent_influence_radius = 4.5

        #------------Simulation--------------------------------

        self.visual = False         #Visualise run in pygame (! Influences speed of simulation)
        self.scale = 15
        self.step_limit = 250       #If exceeded, run fails


        #--------------Performance metrics-----------------------------

        self.target = False                 #True as soon as one agent reaches target 
        self.path_length = 0                #Lenth of path of agent that first reached the target (steps)
        self.eff_path_length = 0            #Lenth of path of agent that first reached the target divided by initial distance (steps)
        self.computational_complexity = 0   #Time of simulation (s)
        self.min_distance_target = 0        #Minimum clearance of agent that reached the target first


