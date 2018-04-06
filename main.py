from orders import small_order_list as small
from warehouse import warehouse
from create_graphs import *
from Agent import *
from Worker import *
from WHCA import *
from draw_simulation import draw

def get_correct_node(pickup_nodes, node_id):
	for current in pickup_nodes:
		if current.id == node_id:
			return current
	raise Exception('Could not find id:%d in the list of pickup_nodes' %(node_id))


def create_workers(drop_off_nodes):
	return [Worker(new_id) for new_id, x in enumerate(drop_off_nodes)]

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

def main():
	order_input = small
	number_of_agents = 5

	graph, pickup_nodes, drop_off_nodes = create_Astar_graph(warehouse)

	workers = create_workers(drop_off_nodes)
	orders = create_orders(order_input, pickup_nodes)
	distribute_orders(workers, orders)

	agents = create_agents(drop_off_nodes, number_of_agents)
	available_agents = [a for a in agents]

	#agents = [Agent(graph[1][0], graph[15][25], 1, None), Agent(graph[15][25], graph[1][0], 2, None)]
    #for a in agents:
    #   print("Agent %d starts at %d and wants to get to %d" % (a.id, a.pos.id, a.goal.id))

	#WHCA(graph, agents, 10, 5)


	#draw(agents, graph)

	for i in range(0, len(agents[0].walking_path)):
		if agents[0].walking_path[i] == agents[1].walking_path[i]:
			print("CRASH!!!!!!!")


if __name__ == "__main__":
	main()