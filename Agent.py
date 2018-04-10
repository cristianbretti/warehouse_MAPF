class Pickup(object):
    def __init__(self, item, worker):
        self.target_list = [item, worker, item]
        self.state = 0
    
    def advance_pickup_state(self, workers):
        if self.state == 1:
            other_worker = other_worker_that_needs_item(workers)
            if other_worker:
                self.target_list[1] = other_worker
                return True
            else:
                self.state += 1
                return True
        elif self.state == 2:
            self.target_list[0].booked = False
            return False
        else:
            self.state += 1

    def other_worker_that_needs_item(self, workers):
        for worker in workers:
            if worker.items and worker.items[0]:
                for item in worker.items[0]:
                    if item.id == self.target_list[0].id:
                        return worker
        return None

    def get_target(self):
        return self.target_list[self.state]

    def is_carrying_shelf(self):
        return self.state > 0

class Agent(object):
    def __init__(self, pos, id):
        self.id = id
        self.pos = pos
        self.path = None
        self.pickup = None
        self.walking_path = []
        self.is_copy = False
        self.is_carrying_shelf = False

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
