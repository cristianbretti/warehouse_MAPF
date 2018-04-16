from orders import *
from warehouse import warehouse
from functions import *
from rule_expert import *
from Simulation import *
import cProfile

number_of_agents = 5
#big_order_list = simulate_big_order_list(uniform=False, num_simulations=1, num_orders=10, average_item_per_order=2)
big_order_list = big_temp

def get_x_vector_from_state(state):
	x_vector = []
	x_vector.append(state.agent1.pos.id)
	x_vector.append(state.agent2.pos.id)
	for agent in state.agents:
		x_vector.append(agent.pos.id)
	return x_vector


def extract_data(node):
	if not node.parent:
		return
	parent = node.parent
	y = node.from_rule
	x = get_x_vector_from_state(parent.state)
	print("X is:")
	print(x)
	print("Y is:")
	print(y)

	extract_data(parent)


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

		
		print("Rules")
		print(rules)
		#print(print_tree(root))
		sim_tree(root)
		print("one done:")
		print("number of solutions: %d" % (number_solutions(root)))
		print("cheapest solution: %d" % (cheapest_solution(root)))
		table = dict()
		number_diff_solutions(root, table)
		print("all different solutions:")
		for key in table.keys():
			print(key)

		print("GETRAGKLRAGMKRAE")
		print(get_min_node())
		extract_data(get_min_node())
		print("DONE")


if __name__ == "__main__":
	#cProfile.run('main()')
	main()
