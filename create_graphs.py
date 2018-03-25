import numpy as np
from Nodes import *

def create_basic_graph(warehouse):
    graph = np.ndarray((warehouse.shape), dtype=BasicNode)

    index = 0
    for (i,j), value in np.ndenumerate(warehouse):
            graph[i][j] = BasicNode(index, NodeType(value))
            index += 1
    return graph

def create_Astar_graph(warehouse):
    graph = np.ndarray((warehouse.shape), dtype=BasicNode)

    index = 0
    for (i,j), value in np.ndenumerate(warehouse):
            graph[i][j] = AStarNode(index, NodeType(value), (i,j))
            index += 1
    return graph
