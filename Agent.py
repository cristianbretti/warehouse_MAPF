class Pickup(object):
    def __init__(self, item, worker):
        self.item = item
        self.worker = worker

class Agent(object):
    def __init__(self, pos, id):
        self.id = id
        self.pos = pos
        self.path = None
        self.pickup = None
        self.walking_path = []
        self.is_copy = False

    def move_on_path(self, steps):
        if len(self.path) <= steps:
            self.pos = self.path[-1]
            self.walking_path += self.path[1:]
        else:
            self.pos = self.path[steps]
            self.walking_path += self.path[1:steps+1]
        # reset pos node for next interation
        self.pos.g = None
        self.pos.h = None
        self.pos.f = None
        self.pos.came_from = None
        self.pos.depth = 0
