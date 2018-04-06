class Agent(object):
    def __init__(self, pos, id):
        self.id = id
        self.reachedGoal = False
        self.pos = pos
        self.goal = None
        self.path = None
        self.pickup = None
        self.walking_path = []

    def move_on_path(self, steps):
        self.pos = self.path[steps]
        self.walking_path += self.path[1:steps+1]

        if self.pos.coordinates == self.goal.coordinates:
            self.reachedGoal = True
        else:
            self.reachedGoal = False

        # reset pos node for next interation
        self.pos.g = None
        self.pos.h = None
        self.pos.f = None
        self.pos.came_from = None
        self.pos.depth = 0