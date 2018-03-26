from enum import Enum
class NodeType(Enum):
    DEFAULT = 0
    OBSTACLE = 1
    PICKUP = 2
    DROPOFF = 3


class BasicNode(object):
    def __init__(self, new_id, new_type):
        self.id = new_id
        self.type = new_type

class AStarNode(BasicNode):
    def __init__(self, new_id, new_type, new_coordinaters):
        BasicNode.__init__(self, new_id, new_type)
        self.coordinates = new_coordinaters
        self.g = None
        self.h = None
        self.f = None
        self.came_from = None
        self.wait_count = 0

    def __lt__(self, other):
        if self.f == None or other.f == None:
            raise Exception("Some f value not initialized!")
        else:
            return self.f < other.f

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id
