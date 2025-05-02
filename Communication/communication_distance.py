from agent_algorithms.a_star import euclidean_distance
from Agent import Agent


def min_communication_distance(agents: [Agent]):
    """
    Computes the minimum communication distance between agents;
    In graph theory, this is also knows as the Minimum Spanning Tree (MST) Problem;
    This solution makes use of Kruskal's Algorithm to generate the MST and
    returns the length of the longest edge of the MST.
    :param agents: list of agents
    :return: minimum communication distance
    """

    # If there is only one agent, then there's noone to communicate with
    if len(agents) <= 1:
        return 0

    # Otherwise, take the graph representation of the agents
    graph, edges = graph_mapping(agents)

    # Initialize the graph and the edges
    mst_graph = {}
    for i in range(len(agents)):
        mst_graph[agents[i]] = []
    mst_edges = []

    # And generate the MST using Kruskal:
    # Sort the edges ascending by weight
    edges = sorted(edges, key=lambda edge: edge[2])

    # For each edge, add it to the MST if it doesn't create a loop
    for edge in edges:
        mst_graph[edge[0]].append([edge[1], edge[2]])
        if check_loop(agents, mst_graph):
            mst_graph[edge[0]].remove([edge[1], edge[2]])
        else:
            mst_edges.append(edge)

    # The longest edge of the MST is the minimum communication distance
    return mst_edges[-1][2]


def check_loop(agents, graph):
    """
    Check if there is a loop in the graph
    :param agents: list of agents
    :param graph: adjacency map of the graph
    :return: True if there is a loop, False otherwise
    """
    res = True
    visited: set = set([])

    for agent in agents:
        if not (visited.__contains__(agent)):
            res = res and dfs(agent, visited, graph)

    return not res


def dfs(agent, visited, graph):
    """
    The classic DFS (depth-first search) algorithm to check if there is a 
    loop in the graph
    :param agent: current agent
    :param visited: set of visited agents
    :param graph: adjacency map of the graph
    :return: True if there is a loop, False otherwise
    """
    res = True
    visited.add(agent)
    for [n_agent, dist] in graph[agent]:
        if agent != n_agent and visited.__contains__(n_agent):
            return False
        else:
            res = res and dfs(n_agent, visited, graph)
    return res


def graph_mapping(agents: [Agent]):
    """
    Generates the adjacency map and edge list of the agents:
     - The graph of the agents is a complete graph where each agent is connected with each other
        with a cost equal to the Euclidean distance between them
    :param agents: list of all agents (that didn't crash in a obstacle)
    :return: Adjacency map and edge list of the graph
    """
    graph = {}
    edges = []
    for i in range(len(agents)):
        graph[agents[i]] = []
    for i in range(len(agents) - 1):
        for j in range(i + 1, len(agents)):
            dist = euclidean_distance(
                agents[i].x, agents[i].y, agents[j].x, agents[j].y
            )

            graph[agents[i]].append([agents[j], dist])
            graph[agents[j]].append([agents[i], dist])

            edges.append([agents[i], agents[j], dist])
            edges.append([agents[j], agents[i], dist])

    return graph, edges


def mst_limited_cost(agents: [Agent], limit: float):
    """
    Computes the agents who can communicate with each other given a cost limit;
    Uses Kruskal's Algorithm to generate the MST and returns the edges used to generate the MST
    :param agents: list of agents
    :param limit: maximum cost allowed
    :return: edges used to generate the MST and the clusters of agents
    """
    if len(agents) <= 1:
        return 0
    _, edges = graph_mapping(agents)

    mst_graph = {}
    assigned_clusters = {}
    # Assign each agent to a cluster at the beginning
    for index, agent in enumerate(agents):
        mst_graph[agent] = []
        assigned_clusters[agent] = index
    mst_edges = []

    # Sort the edges ascending by weight
    edges = sorted(edges, key=lambda edge: edge[2])

    for edge in edges:
        mst_graph[edge[0]].append([edge[1], edge[2]])
        if check_loop(agents, mst_graph):
            mst_graph[edge[0]].remove([edge[1], edge[2]])
        else:
            mst_edges.append([edge[0], edge[1], edge[2]])
            k = assigned_clusters[edge[1]]
            for agent in agents:
                if assigned_clusters[agent] == k:
                    assigned_clusters[agent] = assigned_clusters[edge[0]]
        # If the last edge added to the MST is greater than the limit, remove it
        # and break the loop -> This means that the MST is complete
        if mst_edges[-1][2] > limit:
            mst_edges.pop()
            break

    return mst_edges, assigned_clusters


# def mst_path(agents: [Agent], mst_edges):
#     """
#     Computes, given an MST, which agents can communicate with each other through the edges
#     :param agents:
#     :param mst_edges:
#     :return:
#     """
#     communication_map = {}
#     for agent in agents:
#         communication_map[agent] = []
#     for agent in agents:
#         for other_agent in agents:
#             if agent != other_agent and [agent, other_agent] in mst_edges:
#                 communication_map[agent].append(other_agent)
#                 communication_map[other_agent].append()
#     return communication_map
