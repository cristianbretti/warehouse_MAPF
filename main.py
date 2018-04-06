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
	workers = [Worker(new_id) for new_id, x in enumerate(drop_off_nodes)]

def create_orders(order_input, pickup_nodes):
	orders = []
	for order_list in order_input:
		order = []
		for node_id in order_list:
			order.append(get_correct_node(pickup_nodes, node_id))
		orders.append(order)

def distribute_orders(workers, orders):
	worker_number = 0
	while orders:
		workers[worker_number].add_order(orders.pop(0))
		worker_number = (worker_number + 1) % len(workers)


def main():
	order_input = small
	number_of_agents = 5

	graph, pickup_nodes, drop_off_nodes = create_Astar_graph(warehouse)

	workers = create_workers(drop_off_nodes)
	orders = create_orders(order_input, pickup_nodes)
	distribute_orders(workers, orders)


	agent_list = [Agent(graph[1][0], graph[15][25], 1, None), Agent(graph[15][25], graph[1][0], 2, None)]
    #for a in agent_list:
    #   print("Agent %d starts at %d and wants to get to %d" % (a.id, a.pos.id, a.goal.id))

	WHCA(graph, agent_list, 10, 5)


	draw(agent_list, graph)

	for i in range(0, len(agent_list[0].walking_path)):
		if agent_list[0].walking_path[i] == agent_list[1].walking_path[i]:
			print("CRASH!!!!!!!")


if __name__ == "__main__":
	main()