class Agent(object):
    def __init__(self, pos, goal, id):
        self.id = id
        self.reachedGoal = pos == goal
        self.pos = pos
        self.goal = goal
        self.path = None
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