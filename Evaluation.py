import math 

def evaluate_path_length(agent): 
    path_length = 0
    for i in range(len(agent.pos_lst)-1): 
        dp = math.sqrt((agent.pos_lst[i+1][0]-agent.pos_lst[i][0])**2+(agent.pos_lst[i+1][1]-agent.pos_lst[i][1])**2)
        path_length += dp 
    return round(path_length, 2)

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
    return path_length, computational_complexity, reachability
