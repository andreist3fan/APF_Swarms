from agent_algorithms.a_star import euclidean_distance
from Agent import Agent

def min_communication_distance(agents: [Agent] ):
    """
    Computes the minimum communication distance between agents;
    In graph theory, this is also knows as the Minimum Spanning Tree (MST) Problem;
    This solution makes use of Kruskal's Algorithm to generate the MST and
    returns the length of the longest edge of the MST.
    :param agents: list of agents
    :return: minimum communication distance
    """
    graph,edges = graph_mapping(agents)

    mst_graph = {}
    for i in range(len(agents)):
        mst_graph[agents[i]] = []
    mst_edges = []

    edges = sorted(edges, key=lambda edge: edge[2])

    for edge in edges:
        mst_graph[edge[0]].append([edge[1],edge[2]])
        if check_loop(agents,mst_graph):
            mst_graph[edge[0]].remove([edge[1],edge[2]])
        else:
            mst_edges.append(edge)

    return mst_edges[-1][2]

def check_loop(agents,graph):
    res = True
    visited:set = set([])
    for agent in agents:
        if not(visited.__contains__(agent)):
            res = res and dfs(agent,visited,graph)

    return not res
def dfs(agent, visited, graph):
    res = True
    visited.add(agent)
    for [n_agent, dist] in graph[agent]:
        if agent!=n_agent and visited.__contains__(n_agent):
            return False
        else: res = res and dfs(n_agent, visited, graph)
    return res

def graph_mapping(agents: [Agent]):
    """
    Generates the adjacency map of the agents:
     - The graph of the agents is a complete graph where each agent is connected with each other
        with a cost equal to the Euclidean distance between them
    :param agents: list of all agents (that didn't crash in a obstacle)
    :return: Adjacency map of the graph
    """
    graph = {}
    edges = []
    for i in range(len(agents)):
        graph[agents[i]] = []
    for i in range(len(agents) - 1):
        for j in range(i + 1, len(agents)):
            dist = euclidean_distance(agents[i].x, agents[i].y, agents[j].x,agents[j].y)
            graph[agents[i]].append([agents[j], dist])
            graph[agents[j]].append([agents[i],dist])
            edges.append([agents[i],agents[j],dist])
            edges.append([agents[ j], agents[i], dist])

    return graph,edges
