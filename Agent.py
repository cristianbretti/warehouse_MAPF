class Pickup(object):
    def __init__(self, item, worker):
        self.target_list = [item, worker, item]
        self.state = 0

    def other_worker_that_needs_item(self, workers, is_copy):
        for worker in workers:
            if worker.items and worker.items[0]:
                for item in worker.items[0]:
                    if item.id == self.target_list[0].id:
                        if not is_copy:
                            worker.items[0].remove(item)
                            if not worker.items[0]:
                                worker.items.pop(0)
                        return worker
        return None

    def advance_pickup_state(self, workers, is_copy):
        if self.state == 1:
            other_worker = self.other_worker_that_needs_item(workers, is_copy)
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
            return True



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
        self.target_path = []
        self.is_copy = False
        self.is_carrying_shelf = False

    def move_on_path(self, steps, pickup):
        if len(self.path) <= steps:
            self.pos = self.path[-1]
            self.walking_path += self.path[1:]
            if pickup:
                self.target_path += [pickup.target_list[0].id for x in self.path[1:]]
            else:
                self.target_path += [-1 for x in self.path[1:]]
        else:
            self.pos = self.path[steps]
            self.walking_path += self.path[1:steps+1]
            if pickup:
                self.target_path += [pickup.target_list[0].id for x in self.path[1:steps+1]]
            else:
                self.target_path += [-1 for x in self.path[1:steps+1]]
        # reset pos node for next interation
        self.pos.g = None
        self.pos.h = None
        self.pos.f = None
        self.pos.came_from = None
        self.pos.depth = 0
