from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import numpy as np
import random

def get_x_vector_from_state(state):
	x_vector = []
	x_vector.append(state.agent1.pos.id)
	x_vector.append(state.agent1.pickup.get_target().id)
	x_vector.append(state.agent2.pos.id)
	x_vector.append(state.agent2.pickup.get_target().id)
	for agent in state.agents:
		x_vector.append(agent.pos.id)
	return x_vector

class DecisionTree(object):
	def __init__(self, file_name, type=1):
		self.file_name = file_name
		if type==1:
			self.tree = tree.DecisionTreeClassifier()
		elif type==2:
			self.tree = RandomForestClassifier()
		elif type==3:
			self.tree = MLPClassifier()
		elif type==4:
			self.tree = AdaBoostClassifier(base_estimator=tree.DecisionTreeClassifier(max_depth=10))
		elif type==5:
			self.tree = SVC()
		elif type==6:
			self.tree = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2))
		self.train_tree()


	def train_tree(self):
		file = open(self.file_name, 'r')
		x = []
		y = []
		lines = []
		for line in file:
			lines.append(line)

		#random.shuffle(lines)

		for line in lines:
			elements = line.split()
			one_y = elements.pop()
			one_x = [int(elem) for elem in elements]
			x.append(one_x)
			y.append(one_y)

		number_of_inputs = len(x)
		train_index = int(number_of_inputs*0.7)

		train_x = x[:train_index]
		train_y = y[:train_index]

		test_x = x[train_index:]
		test_y = y[train_index:]

		self.tree.fit(train_x, train_y)
		print("Tree score is: %.3f" % (self.tree.score(test_x, test_y)))


	def get_rule(self, state):
		x = get_x_vector_from_state(state)
		prediction = int(self.tree.predict([x])[0])
		return prediction
