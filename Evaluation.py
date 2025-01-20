import math 

def evaluate_multiple(setups): 
    path_length = 0
    computational_complexity = 0 
    target = 0 
    not_target = 0 
    for s in setups: 
        if s.target: 
            target += 1     
            path_length += s.path_length 
            computational_complexity += s.computational_complexity 
        else: 
            not_target += 1 
    path_length = path_length/target 
    computational_complexity = computational_complexity/target 
    reachability = target/(target+not_target)
    return round(path_length, 3), round(computational_complexity, 5), reachability

#Function that draws a run if wanted 

#def draw_run(setup, environment, agents): 

