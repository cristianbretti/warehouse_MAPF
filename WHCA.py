from heapq import *
from Nodes import *
from Agent import *
import math
import copy

# The heuristic used in A* to estimate the h-value
def manhattan_distance(start, end):
    dist_x = abs(start.coordinates[1] - end.coordinates[1])
    dist_y = abs(start.coordinates[0] - end.coordinates[0])
    return dist_x + dist_y

#Find the closest item.
def assign_item_to_agent(agent, workers):
    agent_pos = agent.pos
    min_dist = 10**5
    chosen_worker = None
    chosen_item = None
    for worker in workers:
        if worker.items and worker.items[0]:
            for item in worker.items[0]:
                dist = manhattan_distance(agent_pos, item)
                if dist < min_dist:
                    min_dist = dist
                    chosen_worker = worker
                    chosen_item = item
    if chosen_worker:
        agent.pickup = Pickup(chosen_item, chosen_worker)
        if not agent.is_copy:
            chosen_worker.items[0].remove(chosen_item)
        return True
    agent.pickup = None
    return False

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

def reset_f_val_graph(graph):
    for i in range(0, graph.shape[0]):
        for j in range(0, graph.shape[1]):
            graph[i][j].g = None
            graph[i][j].h = None
            graph[i][j].f = None
            graph[i][j].came_from = None

def one_agent_has_pickup(agents):
    for a in agents:
        if a.pickup:
            return True
    return False

def agent_is_at_worker(agent, workers):
    for worker in workers:
        if agent.pos.coordinates == worker.coordinates:
            return True
    return False


def round_robin_shuffle(agents):
    agents.append(agents.pop(0))

def get_target(agent, workers, graph):
    if not agent.pickup:
        if not assign_item_to_agent(agent, workers):
            return None
    if agent.pickup.item:
        return agent.pickup.item
    else:
        return graph[agent.pickup.worker.coordinates[0]][agent.pickup.worker.coordinates[1]]

def set_target_to_none(agent):
    if agent.pickup.item:
        agent.pickup.item = None
    else:
        agent.pickup = None

def extract_path(current):
    path = [current]
    next_node = current.came_from
    while next_node:
        path.insert(0, next_node)
        next_node = next_node.came_from
    return path

def findPathAStar(graph, agent,start_pos, reservation_table, W, workers, K):
    # initialize starting node
    start = start_pos

    target = get_target(agent, workers, graph)
    if not target:
        return [start_pos]

    start.g = 0
    start.h = manhattan_distance(start, target)
    start.f = start.h
    #start.depth = 0

    neighbours = [(0,1),(1,0),(-1,0),(0,-1), (0,0)]

    open_list = []
    closed_list = set()

    # add start to open list
    heappush(open_list, start)

    reached_target_last_step = False
    while open_list:
        current = heappop(open_list)
        closed_list.add(current)

        if current.depth == W:
            # target is found, extract the path
            return extract_path(current)

        #Check if reached goal
        if current.coordinates == target.coordinates:
            if not reached_target_last_step:
                reached_target_last_step = True
            else:
                path_so_far = extract_path(current)
                if len(path_so_far) > K + 1:
                    agent = copy.deepcopy(agent)
                    agent.is_copy = True
                set_target_to_none(agent)
                current_depth = current.depth
                reset_f_val_graph(graph)
                current.came_from = None
                next_path = findPathAStar(graph, agent, current, reservation_table, W, workers, K+1-len(path_so_far))
                return path_so_far + next_path[1:]
        else:
            reached_target_last_step = False

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
                #print("neigbout %d depth %d has OBSTACLE" % (neighbour.id, neighbour.depth))
                continue

            if neighbour in closed_list:
                # neighbour case has already been considered
                #print("neigbout %d depth %d has CLOSED" % (neighbour.id, neighbour.depth))
                continue

            if collisionWillOccur(reservation_table, current, neighbour):
                # can't move to neighbour since another agent is there
                #print("neigbout %d depth %d has colliiiishhh" % (neighbour.id, neighbour.depth))
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

    print("IMPOSSIBLE PROBLEM")

def WHCA(graph, agents, W, K, workers):
    for a in agents:
        assign_item_to_agent(a, workers)

    reservation_table = dict()
    while one_agent_has_pickup(agents):

        round_robin_shuffle(agents)

        # Find collision free paths for each agent
        for a in agents:
            if not a.pickup:
                a.path = []
                continue
            reset_graph(graph)

            path = findPathAStar(graph, a, a.pos, reservation_table, W, workers, K)
            # Reserve path
            for time, value in enumerate(path):
                if time <= W:
                    if value.type == NodeType.DROPOFF:
                        continue
                    reservation_table[hash(value.depth, value.id)] = True

            # Save path
            a.path = path

        for a in agents:
            if not a.pickup and not a.path:
                continue
            a.move_on_path(K)

        reservation_table = dict()
