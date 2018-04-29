from orders import *
from warehouse import warehouse
from Agent import *
from Worker import *
#from draw_simulation import draw
from functions import *

from WHCA import *
from Simulation import *
from DecisionTree import *
import random
import numpy as np





number_of_tests = 1000

def main():
	global number_of_tests

	cost_WHCA = []
	cost_DKBR = []
	cost_RND = []
	DKBR_total_collisions = []
	RND_total_collisions = []
	DKBR_total_failed_tree_rules = []
	input_size_items = []
	input_size_orders = []

	impossible_problems_WHCA = 0
	impossible_problems_DKBR = 0
	impossible_problems_RND = 0
	failed_count = 0

	number_of_agents = 10
	#file_name = "data_for_" + str(number_of_agents) + "_agents.input"
	#file_name = "all_first.txt"
	file_name = "all_coordinates.input"
	#file_name3 = "all_coordinates_small.txt"
	#file_name4 = "all_area.txt"
	dec_tree = DecisionTree(file_name, file_type="coordinates")
	#dec_tree2 = DecisionTree(file_name2)
	#dec_tree3 = DecisionTree(file_name3)
	#dec_tree4 = DecisionTree(file_name4)

	for test_number in range(0, number_of_tests):

		print("STARTING TEST %d" % (test_number))
		order_input = simulate_8020_orders(random.randint(2,15))
		current_item_size = get_item_size(order_input)
		current_order_size = len(order_input)

		graph_DKBR, pickup_nodes_DKBR, drop_off_nodes_DKBR = create_Astar_graph(warehouse)
		graph_WHCA, pickup_nodes_WHCA, drop_off_nodes_WHCA = create_Astar_graph(warehouse)
		graph_RND, pickup_nodes_RND, drop_off_nodes_RND = create_Astar_graph(warehouse)

		workers_DKBR = create_workers(drop_off_nodes_DKBR)
		workers_WHCA = create_workers(drop_off_nodes_WHCA)
		workers_RND = create_workers(drop_off_nodes_RND)

		orders_DKBR = create_orders(order_input, pickup_nodes_DKBR)
		orders_WHCA = create_orders(order_input, pickup_nodes_WHCA)
		orders_RND = create_orders(order_input, pickup_nodes_RND)

		distribute_orders(workers_DKBR, orders_DKBR)
		distribute_orders(workers_WHCA, orders_WHCA)
		distribute_orders(workers_RND, orders_RND)

		agents_DKBR = create_agents(drop_off_nodes_DKBR, number_of_agents)
		agents_WHCA = create_agents(drop_off_nodes_WHCA, number_of_agents)
		agents_RND = create_agents(drop_off_nodes_RND, number_of_agents)

		assign_first_items(agents_DKBR, workers_DKBR)
		assign_first_items(agents_WHCA, workers_WHCA)
		assign_first_items(agents_RND, workers_RND)

		one_algorithm_failed = False
		current_WHCA_COST = WHCA(graph_WHCA, agents_WHCA, 20, 10, workers_WHCA)
		if current_WHCA_COST == -1:
			impossible_problems_WHCA += 1
			one_algorithm_failed = True


		sim_DKBR = Simulation(graph_DKBR, agents_DKBR, workers_DKBR, dec_tree)
		_, _, done = sim_DKBR.run()
		if not done:
			impossible_problems_DKBR += 1
			one_algorithm_failed = True

		sim_RND = Simulation(graph_RND, agents_RND, workers_RND)
		_, _, done = sim_RND.run(is_rnd=True)
		if not done:
			impossible_problems_RND += 1
			one_algorithm_failed = True

		if one_algorithm_failed:
			failed_count += 1
			continue

		cost_DKBR.append(sim_DKBR.cost)
		cost_WHCA.append(current_WHCA_COST)
		cost_RND.append(sim_RND.cost)
		RND_total_collisions.append(sim_RND.crash_count)
		DKBR_total_collisions.append(sim_DKBR.crash_count)
		DKBR_total_failed_tree_rules.append(sim_DKBR.fail_tree_rule_count)
		input_size_items.append(current_item_size)
		input_size_orders.append(current_order_size)

	number_of_tests = number_of_tests - failed_count
	if number_of_tests <= 0:
		print("No simulations were successful")
		return
	avg_cost_WHCA = np.sum(cost_WHCA) / number_of_tests
	avg_cost_DKBR = np.sum(cost_DKBR) / number_of_tests
	avg_cost_RND = np.sum(cost_RND) / number_of_tests
	avg_dec_tree_fail_ratio = 0
	if DKBR_total_collisions != 0:
		avg_dec_tree_fail_ratio = np.sum(DKBR_total_failed_tree_rules) / np.sum(DKBR_total_collisions)

	print("Tree score is: %.3f" % (dec_tree.tree_score))
	print("The average cost for WHCA: %.3f" % (avg_cost_WHCA))
	print("The average cost for DKBR: %.3f" % (avg_cost_DKBR))
	print("The average cost for RND: %.3f" % (avg_cost_RND))
	print("The decision tree picked a non working rule with a ratio: %.3f" % (avg_dec_tree_fail_ratio))
	print("impossible problems encountered: WHCA: %d, DKBR: %d, RND: %d" % (impossible_problems_WHCA, impossible_problems_DKBR, impossible_problems_RND))

	result_file = open("results_2.txt", 'w')
	write_line_to_file(cost_WHCA, result_file)
	write_line_to_file(cost_DKBR, result_file)
	write_line_to_file(cost_RND, result_file)
	result_file.close()

	item_size_file = open("item_size_2.txt", 'w')
	write_line_to_file(input_size_items, item_size_file)
	write_line_to_file(input_size_orders, item_size_file)
	
	item_size_file.close()

	tree_fail_file = open("tree_fail_file_2.txt", 'w')
	write_line_to_file(DKBR_total_failed_tree_rules, tree_fail_file)
	write_line_to_file(DKBR_total_collisions, tree_fail_file)
	write_line_to_file(RND_total_collisions, tree_fail_file)
	tree_fail_file.close()

if __name__ == "__main__":
	main()
