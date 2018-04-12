from small_warehouse import warehouse as wh
from create_graphs import create_Astar_graph
from heapq import *
from Nodes import *

# The heuristic used in A* to estimate the h-value
def manhattan_distance(start, end):
    dist_x = abs(start.coordinates[1] - end.coordinates[1])
    dist_y = abs(start.coordinates[0] - end.coordinates[0])
    return dist_x + dist_y

def AStar(graph, agent):
    start = agent.pos
    target = agent.pickup.get_target()

    print("A star for agent %d from %d to %d" % (agent.id, start.id, target.id))

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

        if current == target:
            # target is found, extract the path
            path = [target]
            next_node = target.came_from
            while next_node:
                path.insert(0, next_node)
                next_node = next_node.came_from
            return path



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


#
# g = create_Astar_graph(wh)
# start = g[1][0]
# target = g[3][3]
#
# path = AStar(g, start, target)
# print([x.id for x in path])
