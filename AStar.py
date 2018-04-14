from heapq import *
from Nodes import *
from functions import *

def AStar(graph, agent, p=False):
    #reset_graph(graph)
    start = agent.pos
    start.came_from = None
    target = agent.pickup.get_target()

    if p:
        print("new astar from %d to %d" % (start.id, target.id))

    start.g = 0
    start.h = manhattan_distance(start, target)
    start.f = start.h

    neighbours = [(0,1),(1,0),(-1,0),(0,-1)]

    open_list = []
    closed_list = set()

    heappush(open_list, start) # add start to open list

    while open_list:
        current = heappop(open_list)
        closed_list.add(current)

        if current.coordinates == target.coordinates:
            # target is found, extract the path
            return extract_path(current)

        for (i,j) in neighbours:
            x, y = (current.coordinates[0] + i, current.coordinates[1] + j)
            if x < 0 or x >= graph.shape[0] or y < 0 or y >= graph.shape[1]:
                # neighbour coordinates are out of the graph
                continue
            neighbour = graph[x][y]
            if neighbour.type == NodeType.OBSTACLE or neighbour in closed_list:
                continue

            if neighbour not in open_list or current.g + 1 < neighbour.g:
                neighbour.g = current.g + 1
                neighbour.h = manhattan_distance(neighbour, target)
                neighbour.f = neighbour.g + neighbour.h
                neighbour.came_from = current
                if neighbour not in open_list:
                    heappush(open_list, neighbour)
