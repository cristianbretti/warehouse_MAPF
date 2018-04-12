from orders import big_order_list as big
from warehouse import warehouse
from functions import *


number_of_agents = 5

def main():
	for order_input in big:
		graph, pickup_nodes, drop_off_nodes = create_Astar_graph(warehouse)

		workers = create_workers(drop_off_nodes)
		orders = create_orders(order_input, pickup_nodes)
		distribute_orders(workers, orders)

		agents = create_agents(drop_off_nodes, number_of_agents)

		for a in agents:
			assign_item_to_agent(a, workers)


if __name__ == "__main__":
	main()