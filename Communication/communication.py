from cgi import print_form

from Agent import Agent
from Communication.communication_distance import mst_limited_cost
from Setup import Setup
import numpy as np

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

    for agent in agents:
        if len(agent.communicated_data)>0:
            all_comm = np.vstack(agent.communicated_data)

            all_comm = all_comm[np.lexsort((all_comm[:, 1], all_comm[:, 0]))]

            # Reduce points based on min_neighbourhood_distance
            reduced_points = []
            for point in all_comm:
                if not reduced_points or np.linalg.norm(point - reduced_points[-1]) >= setup.min_neighbourhood_distance:
                    reduced_points.append(point)

            # Update the agent's communicated data with the reduced points
            agent.communicated_data = reduced_points