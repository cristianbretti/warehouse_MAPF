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

def main():
	order_input = small
	number_of_agents = 3

	graph, pickup_nodes, drop_off_nodes = create_Astar_graph(warehouse)

	workers = create_workers(drop_off_nodes)
	orders = create_orders(order_input, pickup_nodes)
	distribute_orders(workers, orders)

	agents = create_agents(drop_off_nodes, number_of_agents)

	WHCA(graph, agents, 20, 3, workers)

	for a in agents:
		print("					NEW AGENT!!")
		print([x.id for x in a.walking_path])
		print([x for x in a.target_path])

	draw(agents, graph)


if __name__ == "__main__":
	main()
