from orders import small_order_list as small
from warehouse import warehouse
from create_graphs import *
from Agent import * 
from WHCA import *
from draw_simulation import draw

def get_correct_node(items, node_id):
	for current in items:
		if current.id == node_id:
			return current
	raise Exception('Could not find id:%d in the list of items' %(node_id))


def generate_order_list(graph, items, workers):
	for order in small:
		for node_id in order:
			node = get_correct_node(items, node_id) 



def main():
	g, items, workers = create_Astar_graph(warehouse)
	agent_list = [Agent(g[1][0], g[15][25], 1, None), Agent(g[15][25], g[1][0], 2, None)]

    #workers = generate_order_list(g, items, workers)
    #for a in agent_list:
    #   print("Agent %d starts at %d and wants to get to %d" % (a.id, a.pos.id, a.goal.id))

	WHCA(g, agent_list, 10, 5)


	draw(agent_list, g)

	for i in range(0, len(agent_list[0].walking_path)):
		if agent_list[0].walking_path[i] == agent_list[1].walking_path[i]:
			print("CRASH!!!!!!!")


if __name__ == "__main__":
	main()