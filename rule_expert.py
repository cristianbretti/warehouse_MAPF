import copy

class RuleExpertNode(object):
	def __init__(self, cost, simulation):
		self.cost = cost
		self.simulation = simulation
		self.state = None
		self.children = [None, None, None, None, None]


def build_tree(node):
	done = False
	node.state, node.cost, done = node.simulation.run()

	if done:
		return

	for i in range(0, 5):
		child = RuleExpertNode(node.cost, copy.deepcopy(node.simulation))
		if child.simulation.apply_rule(node.state, i):
			build_tree(child)
			node.children[i] = child


def get_rule(root):

	child0 = "INF"
	child1 = "INF"
	child2 = "INF"
	child3 = "INF"
	child4 = "INF"

	if root.children[0]:
		child0 = get_rule(root.children[0])
	if root.children[1]:
		child0 = get_rule(root.children[1])
	if root.children[2]:
		child0 = get_rule(root.children[2])
	if root.children[3]:
		child0 = get_rule(root.children[3])
	if root.children[4]:
		child0 = get_rule(root.children[4])

	return_str =  "(Cost:" + str(root.cost)

	return_str += "Children:" + str(child0) + ", " + str(child1) + ", " + str(child2) + ", " + str(child3) + ", " + str(child4) +")"

	return return_str
