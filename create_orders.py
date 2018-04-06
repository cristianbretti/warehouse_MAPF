from orders import small_order_list as small


def get_correct_node(items, node_id)
	for current in items:
		if current.id = node_id:
			return current
	raise Exception('Could not find id:%d in the list of items' %(node_id))


def generate_order_list(graph, items, workers):
	for order in small:
		for node_id in order:
			node = get_correct_node(items, node_id) 



