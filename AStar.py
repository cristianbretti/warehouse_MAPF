from heapq import *
from Nodes import *
from functions import *
import copy

def AStar(graph, agent, p=False):
    #reset_graph(graph)
    start = agent.pos
    start.depth = 0
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
            return extract_path(current, graph)

        for (i,j) in neighbours:
            x, y = (current.coordinates[0] + i, current.coordinates[1] + j)
            if x < 0 or x >= graph.shape[0] or y < 0 or y >= graph.shape[1]:
                # neighbour coordinates are out of the graph
                continue
            neighbour = graph[x][y]
            neighbour.depth = 0
            if neighbour.type == NodeType.OBSTACLE and agent.is_carrying_shelf:
                continue
            if neighbour in closed_list:
                continue

            if neighbour not in open_list or current.g + 1 < neighbour.g:
                neighbour.g = current.g + 1
                neighbour.h = manhattan_distance(neighbour, target)
                neighbour.f = neighbour.g + neighbour.h
                neighbour.came_from = current
                if neighbour not in open_list:
                    heappush(open_list, neighbour)

def collisionWillOccur(reservation_table, current, neighbour):
    if (neighbour.id, current.depth + 1) in reservation_table:
        # Moving to node collision
        return True
    if (current.id, current.depth + 1) in reservation_table and (neighbour.id, current.depth) in reservation_table:
        # Swap collision
        return True
    return False

def AStarReserved(graph, agent, reservation_table, p=False):
    #reset_graph(graph)
    start = agent.pos
    start.came_from = None
    start.depth = 0
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
        closed_list.add((current.id, current.depth))

        if p:
            print("now looking at %d depth: %d" % (current.id, current.depth))

        if current.coordinates == target.coordinates:
            # target is found, extract the path
            path = extract_path(current, graph)
            if p:
                print("found path is")
                print([x.id for x in path])
            return path

        for (i,j) in neighbours:
            x, y = (current.coordinates[0] + i, current.coordinates[1] + j)
            if x < 0 or x >= graph.shape[0] or y < 0 or y >= graph.shape[1]:
                # neighbour coordinates are out of the graph
                continue
            neighbour = graph[x][y]
            #if not current.depth > 7:
            neighbour = copy.deepcopy(neighbour)
            neighbour.depth = current.depth + 1
            if neighbour.type == NodeType.OBSTACLE and agent.is_carrying_shelf:
                continue

            if (neighbour.id, current.depth + 1) in closed_list:
                if p:
                    print("skipped neighbour %d depth: %d becuase in CLOSED" % (neighbour.id, neighbour.depth))
                continue

            if collisionWillOccur(reservation_table, current, neighbour):
                if p:
                    print("skipped neighbour %d depth %d becuase of collision" % (neighbour.id, neighbour.depth))
                continue

            if neighbour in open_list:
                # make neighbour refer to correct node object
                for x in open_list:
                    if x == neighbour:
                        neighbour = x
                        break

            if neighbour not in open_list or current.g + 1 < neighbour.g:
                neighbour.g = current.g + 1
                neighbour.h = manhattan_distance(neighbour, target)
                neighbour.f = neighbour.g + neighbour.h
                neighbour.came_from = current
                if neighbour not in open_list:
                    if p:
                        print("added %d depth %d to open list" % (neighbour.id, neighbour.depth))
                    heappush(open_list, neighbour)
    return []
