from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import numpy as np
import random
from functions import *

class DecisionTree(object):
	def __init__(self, file_name, type=1, file_type="first"):
		self.file_name = file_name
		self.file_type = file_type
		self.tree_score = 0
		if type==1:
			self.tree = tree.DecisionTreeClassifier(max_depth=15)
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
		self.tree_score = self.tree.score(test_x, test_y)
		print("Tree score is: %.3f" % (self.tree_score))
		print("Tree overfit score is %.3f" % (self.tree.score(train_x, train_y)))


	def get_rule(self, state, graph):
		x = []
		if self.file_type == "first":
			x = get_x_vector_from_state_first(state)
		elif self.file_type == "coordinates":
			x = get_x_vector_from_state_coordinates(state)
		elif self.file_type == "coordinates_small":
			x = get_x_vector_from_state_coordinates_small(state)
		elif self.file_type == "area":
			x = get_x_vector_from_state_area(state, graph)

		prediction = int(self.tree.predict([x])[0])
		return prediction
