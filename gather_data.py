from orders import *
from warehouse import warehouse
from functions import *
from rule_expert import *
from Simulation import *
import cProfile

number_of_agents = 20
big_order_list = simulate_big_order_list(uniform=False, num_simulations=1, num_orders=10, average_item_per_order=2)
#big_order_list = big_temp

def main():
	for order_input in big_order_list:
		print(order_input)
		graph, pickup_nodes, drop_off_nodes = create_Astar_graph(warehouse)

		workers = create_workers(drop_off_nodes)
		orders = create_orders(order_input, pickup_nodes)
		distribute_orders(workers, orders)

		agents = create_agents(drop_off_nodes, number_of_agents)

		for a in agents:
			assign_item_to_agent(a, workers)

		root_simulation = Simulation(graph, agents, workers, False)
		root = RuleExpertNode(0, root_simulation)
		init_build()
		build_tree(root, 0, False)

		print("handled_crashes:")
		for key in get_crashes():
			print(get_crashes()[key])
		print("")
		print("Rules")
		print(rules)
		#print(print_tree(root))
		#sim_tree(root)
		print("one done:")
		print("number of solutions: %d" % (number_solutions(root)))
		print("cheapest solution: %d" % (cheapest_solution(root)))
		table = dict()
		number_diff_solutions(root, table)
		print("all different solutions:")
		for key in table.keys():
			print(key)


		print("DONE")


if __name__ == "__main__":
	cProfile.run('main()')
	#main()
