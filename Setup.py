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


        #Other 
        self.target = False #True as soon as one agent reaches target 




