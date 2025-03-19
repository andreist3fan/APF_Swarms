from cgi import print_form

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
    mst_edges, clusters = mst_limited_cost(agents, setup.communication_distance)
    reverse_clusters = {}
    for index in clusters.values():
        reverse_clusters[index] = []

    for agent in agents:
        reverse_clusters[clusters[agent]].append(agent)

    for agent in agents:
        if agent.target:
            cluster = reverse_clusters[clusters[agent]]
            for other_agent in cluster:
                if agent != other_agent:
                    other_agent.communicated_data.append(agent.pos_lst)

