from sklearn import tree

class DecisionTree(object):
	def __init__(self, file_name):
		self.file_name = file_name
		self.tree = tree.DecisionTreeClassifier()
		self.train_tree()


	def train_tree(self):
		file = open(self.file_name, 'r')
		x = []
		y = []
		for line in file:
			elements = line.split()
			one_y = elements.pop()
			one_x = [int(elem) for elem in elements]
			x.append(one_x)
			y.append(one_y)

		number_of_inputs = len(x)
		train_index = int(number_of_inputs*0.8)
		
		train_x = x[:train_index]
		train_y = y[:train_index]

		test_x = x[train_index:]
		test_y = y[train_index:]
		self.tree.fit(train_x, train_y)

		predicted_test_y = self.tree.predict(test_x)

		number_of_errors = 0
		for i in range(0, len(test_y)):
			if test_y[i] != predicted_test_y[i]:
				number_of_errors += 1

		print("Tree error rate is: %.3f" %(number_of_errors/len(test_y)))
