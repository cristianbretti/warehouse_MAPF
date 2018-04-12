from Agent import *

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
                if not item.booked:
                    dist = manhattan_distance(agent_pos, item)
                    if dist < min_dist:
                        min_dist = dist
                        chosen_worker = worker
                        chosen_item = item
    if chosen_worker:
        if not agent.is_copy:
            chosen_item.booked = True
        agent.pickup = Pickup(chosen_item, chosen_worker)
        if not agent.is_copy:
            chosen_worker.remove_item(chosen_item)
        return True
    agent.pickup = None
    return False

def one_agent_has_pickup(agents):
    for a in agents:
        if a.pickup:
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
            
def extract_path(current):
    path = [current]
    next_node = current.came_from
    while next_node:
        path.insert(0, next_node)
        next_node = next_node.came_from
    return path
