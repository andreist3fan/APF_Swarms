from Agent import Agent
from Communication.communication_distance import mst_limited_cost
from Setup import Setup


def pool_communication_data(agents:[Agent], setup:Setup):
    """
    Pool data from agents to be used in the communication model
    """
    agent_positions = {}
    for agent in agents:
        agent_positions[agent] = (agent.x, agent.y)

    agent_data = []
    mst_edges = mst_limited_cost(agents, setup.communication_distance)


    agent_specific_data = {}
    for agent in agents:
        agent_specific_data[agent] =[]

    for edge in mst_edges:
        agent_specific_data[edge[0]].append(agent_positions[edge[1]])
        agent_specific_data[edge[1]].append(agent_positions[edge[0]])



    return agent_specific_data


def canyon(agents:[Agent], setup:Setup):
