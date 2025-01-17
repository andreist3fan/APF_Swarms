
class Environment: 
    def __init__(self, setup):
        
        #Target
        self.target_x = setup.target_x
        self.target_y = setup.target_y
        
        #Obstacles 
        self.obst_x = []
        self.obst_y = []
        self.obst_radius = 2 #Could be made a list if all the obstacles have a different radius of influence
        print("Environment created")
