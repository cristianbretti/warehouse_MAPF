class Worker(object):
	def __init__(self, new_id, coordinates):
		self.items = []
		self.id = new_id
		self.coordinates = coordinates

	def add_order(self, order):
		self.items.append(order)