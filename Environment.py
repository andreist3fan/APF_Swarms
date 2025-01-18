
class Environment: 
    def __init__(self, setup):
        
        #Target
        self.target_x = setup.target_x
        self.target_y = setup.target_y
        self.target_radius = setup.target_radius
        
        #Obstacles 
        self.obstacles = [(2, 4), (5, 1), (8, 8), (7, 10)] # (x, y) for each obstacle
        print("Environment created")
