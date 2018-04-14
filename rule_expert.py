import copy
from draw_simulation import draw
from Simulation import *


min_so_far = 10**5
rules = [0,0,0,0,0]

def init_build():
	global min_so_far
	min_so_far = 10**5

class RuleExpertNode(object):
	def __init__(self, cost, simulation):
		self.cost = cost
		self.simulation = simulation
		self.state = None
		self.leaf = False
		self.children = [None, None, None, None, None]


def build_tree(node, prevCost, crash_prev):
	global min_so_far
	done = False
	node.state, node.cost, done = node.simulation.run()

	if done:
		#print("Reached GOOD end of simulation")
		node.leaf = True
		if node.cost < min_so_far:
			min_so_far = node.cost
		return

	if node.cost >= min_so_far:
		print("already surpassed min so far")
		node = None
		return

	# print("CRASH with cost: %d " % (node.cost))
	# print("agent 1 path")
	# print([x.id for x in node.state.agent1.path[:3]])
	# print("agent 2 path")
	# print([x.id for x in node.state.agent2.path[:3]])
	# print("")

	if node.cost == prevCost + 1:
		if crash_prev: # maybe more that 2 crashes in a row should be considered?
			node = None
			#print("Reached BAD end of simulation")
			return 10**5
		else:
			crash_prev = True
	else:
		crash_prev = False

	booked_items = get_booked_items(node.simulation.graph)

	for i in range(0, 5):
		new_sim = copy.copy(node.simulation)
		new_sim.agents = copy.deepcopy(node.simulation.agents)
		new_sim.workers = copy.deepcopy(node.simulation.workers)
		#new_sim = copy.deepcopy(node.simulation)
		reset_booked(new_sim.graph, booked_items)
		#reset_graph(new_sim.graph)
		child = RuleExpertNode(node.cost, new_sim)
		if child.simulation.apply_rule(node.state, i):
			global rules
			rules[i] += 1
			build_tree(child, node.cost, crash_prev)
			node.children[i] = child

def get_booked_items(graph):
		booked_items = []
		for i in range(0, graph.shape[0]):
			for j in range(0, graph.shape[1]):
				if graph[i][j].booked:
					booked_items.append((i,j))
		return booked_items


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
		print("one solution")
		draw(root.simulation.agents, root.simulation.graph)

def number_solutions(root):
	if not root.leaf:
		count = 0
		for i in range(0, 5):
			if root.children[i]:
				count += number_solutions(root.children[i])
		return count
	else:
		return 1

def number_diff_solutions(root, table):
	if not root.leaf:
		for i in range(0, 5):
			if root.children[i]:
				number_diff_solutions(root.children[i], table)
	else:
		table[root.cost] = True
		return

def cheapest_solution(root):
	if not root.leaf:
		min = 10**5
		for i in range(0, 5):
			if root.children[i]:
				cur = cheapest_solution(root.children[i])
				if cur < min:
					min = cur
		return min
	else:
		return root.cost


def compare_agents(agents1, agents2):
	if len(agents1) != len(agents2):
		print("NOT EQUAL LENGTH")
		return False
	for i in range(0, len(agents1)):
		if agents1[i].id != agents2[i].id:
			print("not same agent at index")
			return False

		for j in range(0, len(agents1[i].path)):
			if agents1[i].path[j] != agents2[i].path[j]:
				print("not same path for agent %d %d " % (agents1[i].id,agents2[i].id))
				print([x.id for x in agents1[i].path])
				print([x.id for x in agents2[i].path])
				return False
		if agents1[i].pickup:
			if agents1[i].pickup.state != agents2[i].pickup.state:
				return False
			for k in range(0, 3):
				if agents1[i].pickup.target_list[k].id !=  agents2[i].pickup.target_list[k].id:
					return False
			temp =  agents1[i].pickup.state
			agents1[i].pickup.state = 1337
			if agents2[i].pickup.state == 1337:
				agents1[i].pickup.state = temp
				return False
			agents1[i].pickup.state = temp
		if agents1[i].was_at_target != agents2[i].was_at_target:
			return False
		if agents1[i].is_copy != agents2[i].is_copy:
			return False
		if agents1[i].is_carrying_shelf != agents2[i].is_carrying_shelf:
			return False
		if agents1[i].pos.id != agents2[i].pos.id:
			return False
	return True

def compare_workers(workers1, workers2):
	if len(workers1) != len(workers2):
		return False
	for x in range(0, len(workers1)):
		work1 = workers1[x]
		work2 = workers2[x]
		if work1.id != work2.id:
			return False
		if work1.coordinates != work2.coordinates:
			return False
		if len(work1.items) != len(work2.items):
			return False
		for i in range(0, len(work1.items)):
			if len(work1.items[i]) != len(work2.items[i]):
				return False
			for j in range(0, len(work1.items[i])):
				if work1.items[i][j].id != work2.items[i][j].id:
					return False
	return True
