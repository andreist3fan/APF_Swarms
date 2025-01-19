class Node:
    """
        Node class for A* algorithm.
        Converts the grid coordinates to an equivalent graph version.
        :param x: x-coordinate
        :param y: y-coordinate
        :param g: Cost from start
        :param h: Heuristic cost
        :param parent: Parent node
    """
    def __init__(self, x, y, g, h, parent=None):
        self.x = x
        self.y = y
        self.g = g  # Cost from start
        self.h = h  # Heuristic cost
        self.f = g + h  # Total cost
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f