from orders import *
from warehouse import warehouse
from Agent import *
from Worker import *
from draw_simulation import draw
from functions import *

from WHCA import *
from Simulation import *
from DecisionTree import *

def main():
	order_input = big_temp[0]
	number_of_agents = 5
	file_name = "data_for_" + str(number_of_agents) + "_agents.txt"

	graph, pickup_nodes, drop_off_nodes = create_Astar_graph(warehouse)

	workers = create_workers(drop_off_nodes)
	orders = create_orders(order_input, pickup_nodes)
	distribute_orders(workers, orders)

	agents = create_agents(drop_off_nodes, number_of_agents)

	for a in agents:
		assign_item_to_agent(a, workers)

	#WHCA(graph, agents, 20, 10, workers)
	dec_tree = DecisionTree(file_name)
	sim = Simulation(graph, agents, workers, dec_tree)
	sim.run()
	#state, cost, done = sim.run()

	# if state:
	# 	print("crash with agents %d and %d at %d and %d" % (state.agent1.id, state.agent2.id, state.agent1.pos.id, state.agent2.pos.id))
	# 	print("cost so far %d" % (cost))
	# 	print(done)

	draw(agents, graph)


if __name__ == "__main__":
	main()
