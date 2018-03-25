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
