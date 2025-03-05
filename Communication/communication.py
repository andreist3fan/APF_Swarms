from Agent import Agent
from Communication.communication_distance import mst_limited_cost
from Setup import Setup


def pool_communication_data(agents:[Agent], setup:Setup):
    """
    Pool data from agents to be used in the communication model
    """

    # store current agent positions
    agent_positions = {}
    for agent in agents:
        agent_positions[agent] = (agent.x, agent.y)

    # get the edges of the minimum spanning tree within the communication distance
    # i.e the clusters of agents that can communicate with each other
    mst_edges = mst_limited_cost(agents, setup.communication_distance)

    # store a dictionary for each agent, of the positions of the agents it can communicate with
    agent_specific_data = {}
    for agent in agents:
        agent_specific_data[agent] =[]

    for edge in mst_edges:
        agent_specific_data[edge[0]].append(agent_positions[edge[1]])
        agent_specific_data[edge[1]].append(agent_positions[edge[0]])

    for agent in agent_specific_data:
        agent.communicated_data = []

    for agent in agent_specific_data:
        if agent.target:
            for other_agent in agent_specific_data[agent]:
                other_agent.communicated_data.append(agent.pos_lst)


