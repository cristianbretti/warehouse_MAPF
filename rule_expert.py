import copy
#from draw_simulation import draw
from Simulation import *
import random
import gc

random.seed(9611122319)


min_so_far = 10**5
min_node = None
rules = [0,0,0,0,0]
handled_crashes = dict()

def get_crashes():
	return handled_crashes

def get_min_node():
	return min_node

def init_build():
	global min_so_far
	min_so_far = 10**5
	global min_node
	min_node = None
	global handled_crashes
	handled_crashes = dict()

def hash_two(a, b):
    return int((a+b)*(a+b+1)/2 + b)

def hash_crash(state, cost):
	a = hash_two(state.agent1.id, state.agent1.pos.id)
	b = hash_two(state.agent2.id, state.agent2.pos.id)
	c = 0
	for agent in state.agents:
		c += hash_two(agent.id, agent.pos.id)
	d = hash_two(a, b) % 100
	e = hash_two(d, c) % 100
	ret = hash_two(e, cost)
	# print("A crash between %d and %d at %d and %d with cost %d " % (state.agent1.id, state.agent2.id, state.agent1.pos.id, state.agent2.pos.id, cost))
	# for agent in state.agents:
	# 	print("Agent %d at %d " % (agent.id, agent.pos.id))
	# print("GOT HASH: %f" % (ret))
	return ret


class RuleExpertNode(object):
	def __init__(self, cost, simulation, parent=None, from_rule=None):
		self.cost = cost
		self.simulation = simulation
		self.state = None
		self.leaf = False
		self.parent = parent
		self.from_rule = from_rule
		self.children = [None, None, None, None, None]

class Crash(object):
	def __init__(self, state, cost, done):
		self.state = state
		self.cost = cost
		self.done = done

def build_tree(node, prevCost, crash_prev, crash_prev_agents=None, crash=None):
	global min_so_far
	global min_node
	done = False

	# if crash:
	# 	print("was crash")
	# 	node.state = crash.state
	# 	node.cost = crash.cost
	# 	done = crash.done
	# else:
	node.state, node.cost, done = node.simulation.run(min_so_far)


	if done:
		print("Reached GOOD end of simulation")
		node.leaf = True
		if node.cost < min_so_far:
			min_so_far = node.cost
			min_node = node
			gc.collect()
		return node.cost

	if node.cost >= min_so_far:
		#print("already surpassed min so far")
		node = None
		return 10**5

	# print("CRASH with cost: %d for agents %d and %d going to %d and %d" % (node.cost, node.state.agent1.id, node.state.agent2.id,node.state.agent1.pickup.get_target().id, node.state.agent2.pickup.get_target().id))
	# print("agent 1 path")
	# print([x.id for x in node.state.agent1.path[:3]])
	# print("agent 2 path")
	# print([x.id for x in node.state.agent2.path[:3]])
	# print("")
	# print("")

	if hash_crash(node.state, node.cost) in handled_crashes:
		node.cost = handled_crashes[hash_crash(node.state, node.cost)]
		node.leaf = True
		return node.cost
		# #print("			already seen this crash")
		# node = None
		# return node.cost


	if node.cost == prevCost + 1:
		if crash_prev and (node.state.agent1.id, node.state.agent2.id) == crash_prev_agents:
			print("Reached BAD end of simulation, to many crashes in a row for same agents!")
			#draw(node.simulation.agents, node.simulation.graph)
			node = None
			return 10**5
		else:
			crash_prev = True
			crash_prev_agents = (node.state.agent1.id, node.state.agent2.id)
	else:
		crash_prev = False
		crash_prev_agents = None

	#handled_crashes[hash_crash(node.state, node.cost)] = True
	booked_items = get_booked_items(node.simulation.graph)

	min = 10**5
	rule_list = [0,1,2,3,4]
	random.shuffle(rule_list)
	for j in range(0, 5):
		i = rule_list[j]
		reset_booked(node.simulation.graph, booked_items)
		#reset_graph(node.simulation.graph)
		ok, new_path1, new_path2 = node.simulation.can_apply_rule(node.state, i)
		if ok:
			#print("rule %d worked "% (i))
			global rules
			rules[i] += 1
			new_sim = create_new_sim_2(node.simulation)
			#new_sim_2 = create_new_sim_2(node.simulation)

			child = RuleExpertNode(node.cost, new_sim, node, i)
			#child2 = RuleExpertNode(node.cost, new_sim_2, node, i)
			copy1 = []
			copy2 = []
			copy3 = []
			copy4 = []
			if new_path1:
				copy1 = new_path1.copy()
				#copy3 = new_path1.copy()
			if new_path2:
				copy2 = new_path2.copy()
				#copy4 = new_path2.copy()

			child.simulation.apply_rule(node.state, i, copy1, copy2)

			#child2.simulation.apply_rule(node.state, i, copy3, copy4)
			#draw(child.simulation.agents, child.simulation.graph)

			#if not compare_agents(new_sim_1.agents, new_sim_2.agents):
			#	print("				AGNETS NOT SSAME AFTER DIRECTLY ")

			# done = False
			# count = 0
			# c = None
			# c2 = None
			# while (not done):
			# 	#print("one step new_sim_1")
			# 	state1, cost1, done1 = new_sim_1.one_iteration(p=False)
			# 	#print("one step new_sim_2")
			# 	#state2, cost2, done2 = new_sim_2.one_iteration(p=False)
			#
			#
			#
			# 	# if done1 != done2:
			# 	# 	print("				Not equal done")
			# 	# 	#return
			# 	#
			# 	# if cost1 != cost2:
			# 	# 	print("			COST NOT EQUAL")
			# 	#
			# 	# if state1:
			# 	# 	if state2:
			# 	# 		if not compare_state(state1, state2):
			# 	# 			print("			state not eq ater %d " % (count))
			# 	# 	else:
			# 	# 		print("satte 1 finns men inte state2")
			# 	# elif state2:
			# 	# 	print("satte 2 but not 1")
			# 	#
			# 	# if not compare_agents(new_sim_1.agents, new_sim_2.agents):
			# 	# 	print("				AGNETS NOT SSAME AFTER %d count" % (count))
			# 	#
			# 	# 	return
			#
			# 	if done1:
			# 		child2.leaf = True
			# 		break
			#
			# 	if state2:
			# 		c = Crash(state1, cost2, done2)
			# 		c2 = Crash(state2, cost2, done2)
			# 		break
			#
			# 	done = done2
			# 	count += 1

			current = build_tree(child, node.cost, crash_prev, crash_prev_agents)#, c)
			if current < min:
				min = current
			node.children[i] = child
		# else:
		# 	print("rule %d did not work" % (i))

	handled_crashes[hash_crash(node.state, node.cost)] = min
	return min

def create_new_sim_1(old_sim):
	new_sim = copy.copy(old_sim)
	test2 = copy.deepcopy(old_sim.agents)
	new_sim.agents = test2
	new_sim.workers = copy.deepcopy(old_sim.workers)
	#new_sim.cost = copy.deepcopy(old_sim.cost)
	return new_sim

def create_new_sim_2(old_sim):
	new_sim = copy.copy(old_sim)
	test2 = [agent.copy() for agent in old_sim.agents]
	new_sim.agents = test2
	new_sim.workers = copy.deepcopy(old_sim.workers)
	#new_sim.cost = copy.deepcopy(old_sim.cost)
	return new_sim


def create_new_sim_with_graph(old_sim):
	return copy.deepcopy(old_sim)

def get_booked_items(graph):
		booked_items = []
		for i in range(0, graph.shape[0]):
			for j in range(0, graph.shape[1]):
				if graph[i][j].booked:
					booked_items.append((i,j))
		return booked_items

def compare_graph(graph1, graph2):
	for i in range(0, graph1.shape[0]):
		for j in range(0, graph1.shape[1]):
			if not graph1[i][j].compare(graph2[i][j]):
				return False
	return True

def compare_state(state1, state2):
	ok = True
	if state1.agent1.id != state2.agent1.id:
		print("agent1 not eq")
		ok = False
	if state1.agent2.id != state2.agent2.id:
		print("agent2 not eq")
		ok = False
	if state1.agent1.pos.id != state2.agent1.pos.id:
		print("agent1 pos not eq")
		ok = False
	if state1.agent2.pos.id != state2.agent2.pos.id:
		print("agent2 pos not eq")
		ok = False
	if not compare_agents(state1.agents, state2.agents):
		print("state agents not equal")
		ok = False
	return ok



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
			#print(agents1[i].path[j].depth)
			#print(agents2[i].path[j].depth)
			if agents1[i].path[j] != agents2[i].path[j]:
				print("not same path for agent %d %d " % (agents1[i].id,agents2[i].id))
				print([x.id for x in agents1[i].path])
				print([x.id for x in agents2[i].path])
				return False
		if agents1[i].pickup:
			if agents1[i].pickup.state != agents2[i].pickup.state:
				print("PICKUP sate not same")
				return False
			for k in range(0, 3):
				if agents1[i].pickup.target_list[k].id !=  agents2[i].pickup.target_list[k].id:
					print("PICKUP target list not same")
					return False
			temp =  agents1[i].pickup.state
			agents1[i].pickup.state = 1337
			if agents2[i].pickup.state == 1337:
				agents1[i].pickup.state = temp
				print("CHange one  pickup change other BAD!")
				return False
			agents1[i].pickup.state = temp
		if agents1[i].was_at_target != agents2[i].was_at_target:
			print("Was at target not same")
			return False
		if agents1[i].is_copy != agents2[i].is_copy:
			print("copy not same")
			return False
		if agents1[i].is_carrying_shelf != agents2[i].is_carrying_shelf:
			print("carryshelft not same")
			return False
		if agents1[i].pos.id != agents2[i].pos.id:
			print("pos id not same")
			print("agent 1 id: %d" % (agents1[i].pos.id))
			print("agent 2 id: %d" % (agents2[i].pos.id))
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
