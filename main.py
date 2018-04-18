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

number_of_tests = 500

def main():
	global number_of_tests

	cost_WHCA = 0
	cost_DKBR = 0
	DKBR_total_crashes = 0
	DKBR_total_failed_tree_rules = 0

	impossible_problems = 0

	number_of_agents = 10
	file_name = "data_for_" + str(number_of_agents) + "_agents.input"
	dec_tree = DecisionTree(file_name)

	for test_number in range(0, number_of_tests):

		print("STARTING TEST %d" % (test_number))
		order_input = simulate_8020_orders(random.randint(2,15))

		graph_DKBR, pickup_nodes_DKBR, drop_off_nodes_DKBR = create_Astar_graph(warehouse)
		graph_WHCA, pickup_nodes_WHCA, drop_off_nodes_WHCA = create_Astar_graph(warehouse)

		workers_DKBR = create_workers(drop_off_nodes_DKBR)
		workers_WHCA = create_workers(drop_off_nodes_WHCA)

		orders_DKBR = create_orders(order_input, pickup_nodes_DKBR)
		orders_WHCA = create_orders(order_input, pickup_nodes_WHCA)

		distribute_orders(workers_DKBR, orders_DKBR)
		distribute_orders(workers_WHCA, orders_WHCA)

		agents_DKBR = create_agents(drop_off_nodes_DKBR, number_of_agents)
		agents_WHCA = create_agents(drop_off_nodes_WHCA, number_of_agents)

		assign_first_items(agents_DKBR, workers_DKBR)
		assign_first_items(agents_WHCA, workers_WHCA)

		current_WHCA_COST = WHCA(graph_WHCA, agents_WHCA, 20, 10, workers_WHCA)
		if current_WHCA_COST == -1:
			impossible_problems += 1
			continue


		sim = Simulation(graph_DKBR, agents_DKBR, workers_DKBR, dec_tree)
		_, _, done = sim.run()
		if not done:
			impossible_problems += 1
			continue

		cost_DKBR += sim.cost
		cost_WHCA += current_WHCA_COST
		DKBR_total_crashes += sim.crash_count
		DKBR_total_failed_tree_rules += sim.fail_tree_rule_count

	number_of_tests = number_of_tests - impossible_problems
	avg_cost_WHCA = cost_WHCA / number_of_tests
	avg_cost_DKBR = cost_DKBR / number_of_tests
	avg_dec_tree_fail_ratio = DKBR_total_failed_tree_rules / DKBR_total_crashes

	print("The average cost for WHCA: %.3f" % (avg_cost_WHCA))
	print("The average cost for DKBR: %.3f" % (avg_cost_DKBR))
	print("The decision tree picked a non working rule with a ratio: %.3f" % (avg_dec_tree_fail_ratio))
	print("%d impossible problems encountered" % (impossible_problems))

if __name__ == "__main__":
	main()
