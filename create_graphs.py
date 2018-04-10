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
    item_counter = 0
    workers = []
    items = []
    for (i,j), value in np.ndenumerate(warehouse):
            graph[i][j] = AStarNode(index, NodeType(value), (i,j))
            if value == 2:
                graph[i][j].booked = False
                items.append(graph[i][j])
            if value == 3:
                workers.append(graph[i][j])
            index += 1
    return graph, items, workers
