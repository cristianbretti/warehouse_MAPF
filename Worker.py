class Worker(object):
	def __init__(self, new_id, coordinates):
		self.items = []
		self.id = new_id
		self.coordinates = coordinates

	def add_order(self, order):
		self.items.append(order)

	def remove_item(self,item):
		self.items[0].remove(item)
		if not self.items[0]:
			self.items.pop(0)