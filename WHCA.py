from small_warehouse import warehouse as wh
from small_warehouse import straight_line as sl
from create_graphs import create_Astar_graph
from heapq import *
from Nodes import *
from random import shuffle
import math
import copy

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
def collisionWillOccur(rTable, current, neighbour):
    key_next_time_neighbour_pos = hash(current.depth + 1, neighbour.id)
    key_next_time_current_pos = hash(current.depth + 1, current.id)
    key_now_time_neighbour_pos = hash(current.depth, neighbour.id)

    if key_next_time_neighbour_pos in rTable:
        # Moving to node collision
        return True
    if key_next_time_current_pos in rTable and key_now_time_neighbour_pos in rTable:
        # Swap collision
        return True
    return False


def findPathAStar(graph, start, target, rTable, W):
    print("                   NEW!!!!!!!")
    start.g = 0
    start.h = manhattan_distance(start, target)
    start.f = start.h
    start.depth = 0

    neighbours = [(0,1),(1,0),(-1,0),(0,-1), (0,0)]

    open_list = []
    closed_list = set()

    heappush(open_list, start) # add start to open list

    while open_list:
        print("OPEN LIST IS:")
        print([x.id for x in open_list])
        current = heappop(open_list)
        closed_list.add(current)

        if current.depth == W:
            # target is found, extract the path
            path = [current]
            next_node = current.came_from
            while next_node:
                path.insert(0, next_node)
                next_node = next_node.came_from
            for x in path:
                x.t = 0
            print("Path is:")
            print([x.id for x in path])
            return path

        print("Current: %d, f: %d, g: %d, h: %d, depth: %d, t: %d" % (current.id, current.f, current.g, current.h, current.depth, current.t))
        if(current.depth == 0):
            if current.came_from:
                print("      IT HAS IT")
                print(current.came_from.id)

        for (i,j) in neighbours:
            x, y = (current.coordinates[0] + i, current.coordinates[1] + j)
            if x < 0 or x >= graph.shape[0] or y < 0 or y >= graph.shape[1]:
                # neighbour coordinates are out of the graph
                continue
            neighbour = graph[x][y]
            if neighbour.coordinates == current.coordinates:
                # Add a copy of the node with a t value one higher,
                # this node represents waiting
                neighbour = copy.deepcopy(current)
                neighbour.t += 1

            if neighbour.type == NodeType.OBSTACLE or neighbour in closed_list:
                # neighbour is a obstacle or has already been processed
                print("neighbour: %d depth: %d, not considered because OBSTACLE or IN CLOSEdLIST" % (neighbour.id, neighbour.depth))
                continue


            if collisionWillOccur(rTable, current, neighbour):
                # can't move to neighbour since another agent is there
                print("neighbour: %d depth: %d, not considered because COLLISION" % (neighbour.id, neighbour.depth))
                continue

            if (neighbour not in open_list or current.g + 1 < neighbour.g or current.depth + 1 < neighbour.depth) and current.t <= neighbour.t:
                # update or initialize new node
                if neighbour.coordinates == target.coordinates:
                    neighbour.g = current.g + 0
                else:
                    neighbour.g = current.g + 1
                neighbour.h = manhattan_distance(neighbour, target)
                neighbour.f = neighbour.g + neighbour.h
                neighbour.depth = current.depth + 1

                # set parent
                neighbour.came_from = current

                if neighbour not in open_list:
                    # add newly discovered node to open list.
                    print("Added: %d, f: %d, g: %d, h: %d, depth: %d, t: %d" % (neighbour.id, neighbour.f, neighbour.g, neighbour.h, neighbour.depth, neighbour.t))
                    heappush(open_list, neighbour)

def WHCA(graph, agents, W, K):
    rTable = dict()
    while True:
        print("                     NEW MAIN LOOP")
        done = True
        for a in agents:
            if not a.reachedGoal:
                done = False
                break
        if done:
            break

        shuffle(agents)
        for a in agents:
            for i in range(0, graph.shape[0]):
                for j in range(0, graph.shape[1]):
                    graph[i][j].g = None
                    graph[i][j].h = None
                    graph[i][j].f = None
                    graph[i][j].came_from = None
                    graph[i][j].depth = 0
                    graph[i][j].t = 0
                    print(graph[i][j].id)
            print(a.id)
            path = findPathAStar(graph, a.pos, a.goal,rTable, W)
            for t, value in enumerate(path):
                if t <= W:
                    rTable[hash(value.depth, value.id)] = True
            a.path = path
            print("agentd %d is about to walk %d steps on path: " %(a.id, K))
            print([x.id for x in a.path])
            print([x.depth for x in a.path])
            for x in a.path:
                # reset
                x.came_from = None
                x.depth = 0
                x.f = None
                x.g = None
                x.h = None
                x.t = 0

        for a in agents:
            a.move(K)
            print("agent %d now stands on id %d, coord: (%d, %d)" % (a.id, a.pos.id, a.pos.coordinates[0], a.pos.coordinates[1]))
        rTable = dict()



class Agent(object):
    def __init__(self, pos, goal, id):
        self.id = id
        self.reachedGoal = pos == goal
        self.pos = pos
        self.goal = goal
        self.path = None
        self.actualWalking = []

    def move(self, steps):
        if steps > len(self.path)-1:
            self.pos = self.path[-1]
            self.actualWalking = self.actualWalking + self.path
        else:
            self.pos = self.path[steps]
            self.actualWalking = self.actualWalking + self.path[:steps]
        if self.pos.coordinates == self.goal.coordinates:
            self.reachedGoal = True
        else:
            self.reachedGoal = False



g = create_Astar_graph(wh)
agent_list = [Agent(g[1][0], g[4][3], 1337), Agent(g[0][0], g[3][3], 69)]
#g = create_Astar_graph(sl)
#agent_list = [Agent(g[0][0], g[0][7], 69),Agent(g[0][1], g[0][8], 1337)]

for a in agent_list:
    print("Agent %d starts at %d and wants to get to %d" % (a.id, a.pos.id, a.goal.id))

WHCA(g, agent_list, 10, 5)

for a in agent_list:
    print("Agent %d actually walked the path:" % (a.id))
    print([x.id for x in a.actualWalking])

for i in range(0, len(agent_list[0].actualWalking)):
    if agent_list[0].actualWalking[i] == agent_list[1].actualWalking[i]:
        print("CRASHASHOAIHWDOAIWHDOAIWH")
