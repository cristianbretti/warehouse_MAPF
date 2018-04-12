import copy
from draw_simulation import draw

class RuleExpertNode(object):
	def __init__(self, cost, simulation):
		self.cost = cost
		self.simulation = simulation
		self.state = None
		self.leaf = False
		self.children = [None, None, None, None, None]


def build_tree(node, prevCost, crash_prev):
	done = False
	node.state, node.cost, done = node.simulation.run()

	if done:
		node.leaf = True
		return True
	if node.cost == prevCost + 1:
		if crash_prev: # maybe more that 2 crashes in a row should be considered?
			node.cost = 10**5
			node.leaf = True
			return False
		else:
			crash_prev = True
	else:
		crash_prev = False

	print("CRASH with cost: %d at: %d and: %d who wants to go to: %d" % (node.cost, node.state.agent1.pos.id, node.state.agent2.pos.id, node.state.agent1.path[1].id))
	print("")

	for i in range(0, 5):
		child = RuleExpertNode(node.cost, copy.deepcopy(node.simulation))
		if child.simulation.apply_rule(node.state, i):
			#print("could applly rult %d " % (i))
			build_tree(child, node.cost, crash_prev)
			node.children[i] = child
		# else:
		# 	print("could NOT applly rult %d " % (i))


def print_tree(root):
	return_str =  "(Cost: " + str(root.cost) + " "

	if not root.leaf:
		return_str += "Children: ["
		if root.children[0]:
			child = print_tree(root.children[0])
			return_str += " Rule 0: " + child + ", "
		if root.children[1]:
			child = print_tree(root.children[1])
			return_str += " Rule 1: " + child + ", "
		if root.children[2]:
			child = print_tree(root.children[2])
			return_str += " Rule 2: " + child + ", "
		if root.children[3]:
			child = print_tree(root.children[3])
			return_str += " Rule 3: " + child + ", "
		if root.children[4]:
			child = print_tree(root.children[4])
			return_str += " Rule 4: " + child + ", "
		return_str += "])"
	else:
		return_str += "LEAF )"
	return return_str

def sim_tree(root):
	if not root.leaf:
		for i in range(0, 5):
			if root.children[i]:
				sim_tree(root.children[i])
	else:
		draw(root.simulation.agents, root.simulation.graph)
