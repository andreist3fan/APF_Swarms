from Setup import Setup 
import Environment as e 
import Agent as a 
import Evaluation as ev

setup = Setup() 

#---------Change setup settings if not standard settings----------

setup.nr_agents = 1

#-----------------------------------------------------------------

#Create agent according to setup
agents = [] 
for i in range(setup.nr_agents): 
    agents.append(a.Agent(setup))

#Create environment according to setup
env = e.Environment(setup)

while not setup.target: 

    #Update posiiton of agents and check for target
    for i in agents: 

        #Update position 
        i.update_position(env, setup)

        #Check whether agent has reached target
        i.target_check(env)
        if i.target: 
            setup.target = True 


    # For now only one loop for testing purposes 
    #setup.target = True 
