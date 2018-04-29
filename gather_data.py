from orders import *
from warehouse import warehouse
from functions import *
from rule_expert import *
from Simulation import *
import cProfile
import _thread
import random

number_of_agents = 10
#file_name = "data_for_" + str(number_of_agents) + "_agents.txt"
#big_order_list = simulate_big_order_list(uniform=False, num_simulations=1, num_orders=8, average_item_per_order=2)
big_order_list = big_temp

graph = None


def extract_data(node, file1, file2, file3, file4):
	parent = node.parent
	number_of_datas = 0
	while parent:
		y = node.from_rule
		x1 = get_x_vector_from_state_first(parent.state)
		x2 = get_x_vector_from_state_area(parent.state)
		x3 = get_x_vector_from_state_coordinates(parent.state)
		x4 = get_x_vector_from_state_coordinates_small(parent.state)
		x1.append(y)
		x2.append(y)
		x3.append(y)
		x4.append(y)
		write_line_to_file(x1, file1)
		write_line_to_file(x2, file2)
		write_line_to_file(x3, file3)
		write_line_to_file(x4, file4)
		number_of_datas += 1
		node = parent
		parent = node.parent
	return number_of_datas


def main_thread(thread_name, file_name):
	while True:
		print("One simulation STARTED by thread %d" % (thread_name))
		order_input = simulate_8020_orders(random.randint(5,15))
		#order_input = big_temp[0]
		global graph
		graph, pickup_nodes, drop_off_nodes = create_Astar_graph(warehouse)

		workers = create_workers(drop_off_nodes)
		orders = create_orders(order_input, pickup_nodes)
		distribute_orders(workers, orders)

		agents = create_agents(drop_off_nodes, number_of_agents)

		for a in agents:
			assign_item_to_agent(a, workers)

		root_simulation = Simulation(graph, agents, workers)
		root = RuleExpertNode(0, root_simulation)
		init_build()
		#build_tree(root, 0, False)
		rule_expert = RuleExpert()
		rule_expert.build_tree(root, 0, False)


		#print("Rules")
		#print(rules)
		# #print(print_tree(root))
		# #sim_tree(root)
		# print("one done:")
		#print("cheapest solution: %d" % (cheapest_solution(root)))
		#print("min node_cost: %d " % (get_min_node().cost))
		#
		file1 = open(file_name + "_first.txt", "a")
		file2 = open(file_name + "_area.txt", "a")
		file3 = open(file_name + "_coordinates.txt", "a")
		file4 = open(file_name + "_coordinates_small.txt", "a")
		number_of_datas = extract_data(rule_expert.get_min_node(), file1, file2, file3, file4)
		#print("%d number of datas added" % (number_of_datas))
		print("One simulation DONE by thread %d" % (thread_name))
		file1.flush()
		file1.close()
		file2.flush()
		file2.close()
		file3.flush()
		file3.close()
		file4.flush()
		file4.close()

def main():
	file_name_1 = "data_for_" + str(number_of_agents) + "_agents_thread_1"
	file_name_2 = "data_for_" + str(number_of_agents) + "_agents_thread_2"
	file_name_3 = "data_for_" + str(number_of_agents) + "_agents_thread_3"
	file_name_4 = "data_for_" + str(number_of_agents) + "_agents_thread_4"
	# try:
	# 	_thread.start_new_thread(main_thread, (1, file_name_1, ))
	# 	_thread.start_new_thread(main_thread, (2, file_name_2, ))
	# 	_thread.start_new_thread(main_thread, (3, file_name_3, ))
	# except:
	# 	print("Error on starting threads")

	main_thread(3, file_name_3)

if __name__ == "__main__":
	#cProfile.run('main()')
	main()
