class Worker(object):
	def __init__(self, new_id):
		self.items = []
		self.id = new_id

	def add_order(self, order):
		self.items.append(order)