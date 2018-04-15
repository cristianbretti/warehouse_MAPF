from Agent import *
from Worker import *
import numpy as np
from Nodes import *
#Init functions

def get_correct_node(pickup_nodes, node_id):
    for current in pickup_nodes:
        if current.id == node_id:
            return current
    raise Exception('Could not find id:%d in the list of pickup_nodes' %(node_id))


def create_workers(drop_off_nodes):
    return [Worker(node.id, node.coordinates) for node in drop_off_nodes]

def create_orders(order_input, pickup_nodes):
    orders = []
    for order_list in order_input:
        order = []
        for node_id in order_list:
            order.append(get_correct_node(pickup_nodes, node_id))
        orders.append(order)
    return orders

def distribute_orders(workers, orders):
    worker_number = 0
    while orders:
        workers[worker_number].add_order(orders.pop(0))
        worker_number = (worker_number + 1) % len(workers)

def create_agents(drop_off_nodes, number_of_agents):
    agent_list = []
    for i in range(0, number_of_agents):
        agent_list.append(Agent(drop_off_nodes[i % len(drop_off_nodes)], i))
    return agent_list

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

def reset_booked(graph, booked_items):
	# this might work since reset book should only happen
	# once a simulation is fully complete,
	# and the all nodes booked should be false.
	# for (x,y) in booked_items:
	# 	graph[x][y].booked = True
	for k in range(0, graph.shape[0]):
		for l in range(0, graph.shape[1]):
			if (k,l) in booked_items:
				graph[k][l].booked = True
			else:
				graph[k][l].booked = False

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

def extract_path(current, graph=None):
    path = [current]
    next_node = current.came_from
    while next_node:
        path.insert(0, next_node)
        next_node = next_node.came_from

    for node in path:
        node.came_from = None
    # if graph != None:
    #     reset_graph(graph)
    return path
