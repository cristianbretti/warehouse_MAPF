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
        self.depth = 0
        self.booked = False

    def __lt__(self, other):
        if self.f == None or other.f == None:
            raise Exception("Some f value not initialized!")
        else:
            return self.f < other.f

    def __eq__(self, other):
        return (self.id == other.id and self.depth == other.depth)

    def __hash__(self):
        return self.id

    def compare(self, other):
        ok = True
        if self.id != other.id:
            print("1")
            return False
        if self.type != other.type:
            print("2")
            return False
        if self.coordinates != other.coordinates:
            print("3")
            return False
        if self.g != other.g:
            print("4")
            #return False
            ok = False
        if self.h != other.h:
            print("5")
            #return False
            ok = False
        if self.f != other.f:
            print("6")
            #return False
            ok = False
        if self.came_from and other.came_from:
            if self.came_from.id != other.came_from.id:
                print("7")
                ok = False
        elif self.came_from and not other.came_from:
            print("8")
            ok = False
        elif other.came_from and not self.came_from:
            print("9")
            ok = False
        if self.depth != other.depth:
            print("10")
            ok = False
        if self.booked != other.booked:
            print("11")
            ok = False

        if not ok:
            return False
        return True
