from small_warehouse import warehouse as wh
from small_warehouse import straight_line as sl
from small_warehouse import backing
from small_warehouse import big_warehouse as big
from create_graphs import create_Astar_graph
from draw_simulation import draw
from heapq import *
from Nodes import *
from Agent import *
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

def collisionWillOccur(reservation_table, current, neighbour):
    key_next_time_neighbour_pos = hash(current.depth + 1, neighbour.id)
    key_next_time_current_pos = hash(current.depth + 1, current.id)
    key_now_time_neighbour_pos = hash(current.depth, neighbour.id)

    if key_next_time_neighbour_pos in reservation_table:
        # Moving to node collision
        return True
    if key_next_time_current_pos in reservation_table and key_now_time_neighbour_pos in reservation_table:
        # Swap collision
        return True
    return False

def reset_graph(graph):
    for i in range(0, graph.shape[0]):
        for j in range(0, graph.shape[1]):
            graph[i][j].g = None
            graph[i][j].h = None
            graph[i][j].f = None
            graph[i][j].came_from = None
            graph[i][j].depth = 0

def all_agents_at_target(agents):
    for a in agents:
        if not a.reachedGoal:
            return False
    return True

def round_robin_shuffle(agents):
    agents.append(agents.pop(0))
    

def findPathAStar(graph, start, target, reservation_table, W):
    # initialize starting node
    start.g = 0
    start.h = manhattan_distance(start, target)
    start.f = start.h
    start.depth = 0

    neighbours = [(0,1),(1,0),(-1,0),(0,-1), (0,0)]

    open_list = []
    closed_list = set()

    # add start to open list
    heappush(open_list, start)

    while open_list:
        current = heappop(open_list)
        closed_list.add(current)

        if current.depth == W:
            # target is found, extract the path
            path = [current]
            next_node = current.came_from
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
            neighbour = copy.deepcopy(neighbour)
            neighbour.depth = current.depth + 1

            if neighbour.type == NodeType.OBSTACLE:
                # neighbour is not traversable, an obstacle
                continue

            if neighbour in closed_list:
                # neighbour case has already been considered
                continue

            if collisionWillOccur(reservation_table, current, neighbour):
                # can't move to neighbour since another agent is there
                continue

            if neighbour in open_list:
                # make neighbour refer to correct node object
                for x in open_list:
                    if x == neighbour:
                        neighbour = x
                        break

            if neighbour not in open_list or current.g + 1 < neighbour.g:
                if neighbour.coordinates == target.coordinates:
                    # waiting at target is preferred
                    neighbour.g = current.g + 0
                else:
                    neighbour.g = current.g + 1
                neighbour.h = manhattan_distance(neighbour, target)
                neighbour.f = neighbour.g + neighbour.h

                # set parent
                neighbour.came_from = current

                if neighbour not in open_list:
                    # add newly discovered node to open list.
                    heappush(open_list, neighbour)


def WHCA(graph, agents, W, K):
    reservation_table = dict()
    while not all_agents_at_target(agents):

        round_robin_shuffle(agents)

        # Find collision free paths for each agent
        for a in agents:
            reset_graph(graph)

            path = findPathAStar(graph, a.pos, a.goal, reservation_table, W)

            # Reserve path
            for time, value in enumerate(path):
                if time <= W:
                    reservation_table[hash(value.depth, value.id)] = True

            # Save path
            a.path = path

        for a in agents:
            a.move_on_path(K)

        reservation_table = dict()



def main():
    #g = create_Astar_graph(wh)
    #agent_list = [Agent(g[1][0], g[4][3], 1337), Agent(g[0][0], g[3][3], 69)]
    #g = create_Astar_graph(sl)
    #agent_list = [Agent(g[0][0], g[0][7], 69),Agent(g[0][1], g[0][8], 1337)]
    #g = create_Astar_graph(backing)
    #agent_list = [Agent(g[0][0], g[0][18], 1),Agent(g[0][18], g[0][0], 2)]

    g, items, workers = create_Astar_graph(big)
    agent_list = [Agent(g[0][0], g[8][11], 1, None), Agent(g[0][11], g[8][0], 2, None), Agent(g[8][0], g[0][11], 3, None), Agent(g[8][11], g[0][0], 4, None), 
    Agent(g[1][1],g[0][6],5, None)]

    #workers = generate_order_list(g, items, workers)
    for a in agent_list:
        print("Agent %d starts at %d and wants to get to %d" % (a.id, a.pos.id, a.goal.id))

    WHCA(g, agent_list, 10, 5)


    draw(agent_list, g)

    for a in agent_list:
        print("Agent %d walked the path:" % (a.id))
        print([x.id for x in a.walking_path])

    for i in range(0, len(agent_list[0].walking_path)):
        if agent_list[0].walking_path[i] == agent_list[1].walking_path[i]:
            print("CRASH!!!!!!!")

main()
