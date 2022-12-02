class Node:
    """
    The node class represents a combustible object and its connections to other combustible objects. The node itself
    holds the state of the object, such as its property value, mitigation level, other parameters. Each node has a
    list of edges to other nodes as well as its state. A node state can be 0: not on fire, 1: on fire from primary,
    2: on fire from secondary, 3: burned down from primary, 4: burned down from secondary.
    """

    '''Node object is initialized by a number assigned to it and its 3D location coordinate.'''

    def __init__(self, node_num, coordinates):
        self.number = node_num
        self.elevation = 0
        self.coords = coordinates
        # IMPORTANT: Added this, which will be a factor used to specify that trees and other sort of vegetation are
        #               more or less prone to spreading fire; we should keep in <0,1]; suggest alternate names
        #               or alternate implementations of this - Artem did an exemplary job with the Node and House class!
        self.spreadability = 1
        self.edges = list()
        self.node_state = 0
        self.caught_primary = False  # true if node just caught primary
        self.caught_secondary = False  # true if node just caught secondary

    '''___Getters___'''
    def get_coords(self):
        return self.coords

    def get_edges(self):
        return self.edges

    def get_state(self):
        return self.node_state

    '''___Setters___'''
    def add_edge(self, edge):  # appends an edge to the node's list of edges.
        self.edges.append(edge)
        return

    def clear_edges(self):  # makes a node have no edges.
        self.edges.clear()

    def set_state(self, state):
        assert state in [0, 1, 2, 3, 4], \
            f"Expected combustion state in [0, 1, 2, 3, 4] but got {state}."
        self.node_state = state
        return

    '''___Fire_State_Functions___'''

    def primary_ignition(self):
        self.caught_primary = True
        return

    def secondary_ignition(self):
        self.caught_secondary = True
        return

    def burns_down(self):  # if a node is on fire, burns it down and changes its state.
        if self.node_state == 1:
            self.node_state = 3
        elif self.node_state == 2:
            self.node_state = 4
        return

    def reset(self):  # resets the node state.
        self.node_state = 0
        return

    def is_on_fire(self):  # determines if a node is currently on fire
        return self.node_state in [1, 2]

    def never_on_fire(self):  # determines if a node was ever on on fire.
        return not self.node_state


class House(Node):
    """This is an inner class representing a House. House class holds special functions regarding mitigation and
    property value."""

    def __init__(self, node_num, coordinates, property_val=0):
        super().__init__(node_num, coordinates)
        self.mitigation_level = 0
        self.property_val = property_val

    '''_Mitigation Functions'''

    def get_mitigation_level(self):
        return self.mitigation_level

    def is_mitigated(self):  # checks if house is mitigated.
        if self.mitigation_level == 0:
            return False
        else:
            return True

    def mitigate(self, mitigation_level):
        self.mitigation_level = mitigation_level
        return


class BigTree(Node):
    def __init__(self, node_num, coordinates):
        super(BigTree, self).__init__(node_num, coordinates)
        self.spreadability = 0.7


class SmallTree(Node):
    def __init__(self, node_num, coordinates):
        super(SmallTree, self).__init__(node_num, coordinates)
        self.spreadability = 0.5


class Shrub(Node):
    def __init__(self, node_num, coordinates):
        super(Shrub, self).__init__(node_num, coordinates)
        self.spreadability = 0.3


class Lawn(Node):
    def __init__(self, node_num, coordinates):
        super(Lawn, self).__init__(node_num, coordinates)
        self.spreadability = 0.1
