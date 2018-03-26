from small_warehouse import warehouse as wh
from small_warehouse import straight_line as sl
from create_graphs import create_Astar_graph
from heapq import *
from Nodes import *
from random import shuffle
import math

# The heuristic used in A* to estimate the h-value
def manhattan_distance(start, end):
    dist_x = abs(start.coordinates[1] - end.coordinates[1])
    dist_y = abs(start.coordinates[0] - end.coordinates[0])
    return dist_x + dist_y

def hash(a, b):
    return int((a+b)*(a+b+1)/2 + b)

def hash_inverse(value):
    a = value * 8
    b = a + 1
    c = math.sqrt(b)
    d = c - 1
    e = d/2
    w = int(e)

    f = w + 1
    g = w * f
    h = g/2
    y = value - h
    x = w - y
    return (x, y)

def findPathAStar(graph, start, target, rTable, W):
    start.g = 0
    start.h = manhattan_distance(start, target)
    start.f = start.h

    neighbours = [(0,1),(1,0),(-1,0),(0,-1), (0,0)]

    open_list = []
    #closed_list = set()

    heappush(open_list, start) # add start to open list

    while open_list:
        current = heappop(open_list)
        #closed_list.add(current)

        if current == target:
            print(target.id)
            print("found")
            # target is found, extract the path
            # path = [target]
            # next_node = target.came_from
            # print(next_node.id)
            # while next_node:
            #     path.insert(0, next_node)
            #     last_id = next_node.id
            #     next_node = next_node.came_from
            #     if next_node:
            #         print(next_node.id)
            # print([x.id for x in path])
            # return path
            path = [target]
            next_node = target.came_from
            path.insert(0, next_node)
            print(next_node.id)
            next_node = next_node.came_from
            path.insert(0, next_node)
            print(next_node.id)
            next_node = next_node.came_from
            path.insert(0, next_node)
            print(next_node.id)
            next_node = next_node.came_from
            path.insert(0, next_node)
            print(next_node.id)
            next_node = next_node.came_from
            path.insert(0, next_node)
            print(next_node.id)
            next_node = next_node.came_from
            path.insert(0, next_node)
            print(next_node.id)
            next_node = next_node.came_from
            path.insert(0, next_node)
            print(next_node.id)
            print([x.id for x in path])
            return path



        for (i,j) in neighbours:
            x, y = (current.coordinates[0] + i, current.coordinates[1] + j)
            if x < 0 or x >= graph.shape[0] or y < 0 or y >= graph.shape[1]:
                # neighbour coordinates are out of the graph
                continue
            neighbour = graph[x][y]
            if neighbour.type == NodeType.OBSTACLE: #or neighbour in closed_list:
                continue

            key = hash(current.g + 1, neighbour.id)
            if key in rTable:
                continue

            if neighbour not in open_list or current.g + 1 < neighbour.g:
                neighbour.g = current.g + 1
                neighbour.h = manhattan_distance(neighbour, target)
                neighbour.f = neighbour.g + neighbour.h
                if neighbour == current:
                    neighbour.wait_count += 1
                else:
                    neighbour.came_from = current
                if neighbour not in open_list:
                    heappush(open_list, neighbour)

def WHCA(graph, agents, W, K):
    rTable = dict()
    while True:
        done = True
        for a in agents:
            if not a.reachedGoal:
                done = False
                break
        if done:
            break

        #shuffle(agents)
        for a in agents:
            for i in range(0, graph.shape[0]):
                for j in range(0, graph.shape[1]):
                    graph[i][j].g = None
                    graph[i][j].h = None
                    graph[i][j].f = None
                    graph[i][j].came_from = None
            path = findPathAStar(graph, a.pos, a.goal,rTable, W)
            for t, value in enumerate(path):
                if t < W:
                    rTable[hash(t, value.id)] = True
            a.path = path

        for a in agents:
            a.move(K)

        rTable = dict()



class Agent(object):
    def __init__(self, pos, goal, id):
        self.id = id
        self.reachedGoal = pos == goal
        self.pos = pos
        self.goal = goal
        self.path = None

    def move(self, steps):
        self.pos = self.path[steps]
        if self.pos == self.goal:
            self.reachedGoal = True



#g = create_Astar_graph(wh)
#agent_list = [Agent(g[1][0], g[4][3], 1337), Agent(g[0][0], g[3][3], 69)]
g = create_Astar_graph(sl)
agent_list = [Agent(g[0][0], g[0][7], 69),Agent(g[0][1], g[0][8], 1337)]


WHCA(g, agent_list, 5, 3)
