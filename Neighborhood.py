from Node import House, BigTree, SmallTree, Shrub, Lawn
from Edge import Edge
import numpy as np
import Paramaters as Par
from warnings import warn


class Neighborhood:
    """This class holds all the house objects in the neighborhood and sets up the edges between houses. Simulates
    fire spread and primary fire ignition"""
    def __init__(self, objects):
        self.mitigation_level = Par.MITIGATION_LEVEL
        self.wind_direction = Par.WIND_DIRECTION
        self.wind_speed_multiplier = Par.WIND_SPEED_MULTIPLIER
        self.nodes = self.assign_nodes(objects)
        self.houses = [node for node in self.nodes if type(node) is House]
        self.border_nodes = self.assign_border_nodes()
        self.mitigate_houses_random()
        self.connect_nodes()
        self.just_on_fire = False

    # Appends Node objects from a list of coordinates
    def assign_nodes(self, objects):
        nodes = list()
        i = 1
        for obj in objects:
            obj_type = obj[0]
            obj_coords = obj[1]
            if obj_type == "h":
                nodes.append(House(i, obj_coords))
            elif obj_type == "bT":
                nodes.append(BigTree(i, obj_coords))
            elif obj_type == "sT":
                nodes.append(SmallTree(i, obj_coords))
            elif obj_type == "sh":
                nodes.append(Shrub(i, obj_coords))
            elif obj_type == "la":
                nodes.append(Lawn(i, obj_coords))
            i += 1
        return nodes

    def assign_border_nodes(self):
        border = list()
        for node in self.nodes:
            (x, y) = node.coords
            if (y < 5 or y > 29) or (x < 5 or x > 32):
                border.append(node)
        return border

    # Connects each node object to each other. Populates list of edges in each House object.
    def connect_nodes(self):
        nodes = self.nodes
        for node1 in nodes:
            for node2 in nodes:
                if node1 is not node2:
                    node1.add_edge(Edge(node1, node2))
        return

    # Mitigates a random sample of houses.
    def mitigate_houses_random(self):
        num_to_mitigate = round(len(self.houses) * self.mitigation_level)
        rand_sample = np.random.choice(self.houses, num_to_mitigate, False)
        for house in rand_sample:
            house.mitigate(1)
        return

    '''Getters'''

    # Gets the dimensions of the neighborhood for non positive coordinates.
    def get_dimensions(self):
        max_x = 0
        max_y = 0
        for node in self.nodes:
            max_x = max(max_x, node.coords[0])
            max_y = max(max_y, node.coords[1])
        return max_x + 1, max_y + 1

    '''_________The following functions perform primary fire ignition and fire spread simulation_________'''

    def node_one_ignition(self):  # Starts a primary fire at house 1.
        self.nodes[0].primary_ignition()
        self.just_on_fire = True
        return

    def border_random_ignition(self, num_to_ignite=1):  # ignites a random house on the border.
        nodes_to_ignite = np.random.choice(self.border_nodes, num_to_ignite, False)
        for node in nodes_to_ignite:
            node.primary_ignition()
        self.just_on_fire = True
        return

    def ignite_nodes_random(self, num_to_ignite=1):  # Ignites a random sample of houses by primary fire.
        nodes_to_ignite = np.random.choice(self.nodes, num_to_ignite, False)
        for node in nodes_to_ignite:
            node.primary_ignition()
        self.just_on_fire = True
        return

    def neighborhood_burned(self):  # Checks if neighborhood is on fire currently.
        if self.just_on_fire:
            return False
        else:
            for node in self.nodes:
                if node.get_state() in [1, 2]:
                    return False
            return True

    def update_neighborhood(self):  # Updates all house that were caught on fire to fire spreading state.
        for node in self.nodes:
            node.burns_down()
            if node.caught_primary:
                node.caught_primary = False
                node.set_state(1)
            if node.caught_secondary:
                node.caught_secondary = False
                node.set_state(2)
        return

    # Simulates Fire Spread. If a node is on fire, passes on a fire to the node's edges, dependent on the probability
    # of those edges. Updates the neighborhood after each iteration.
    def simulate_fire_spread(self):
        while not self.neighborhood_burned():
            self.update_neighborhood()
            for node in self.nodes:
                if node.is_on_fire():
                    for edge in node.edges:
                        if edge.node2.never_on_fire():
                            if np.random.random() < edge.get_probability():
                                edge.node2.secondary_ignition()
            self.just_on_fire = False
        return

    # Fire spread simulation based on only setting house #1 on fire.
    def simulate_node_one_fire(self):
        self.node_one_ignition()
        self.simulate_fire_spread()
        return

    def simulate_random_border_fire(self):  # fire spread simulation with only border house setting on fire.
        self.border_random_ignition(1)
        self.simulate_fire_spread()
        return

    # Simulates fire spread with random primary ignition of specified number of houses.
    def simulate_random_fire(self, num_to_ignite=1):
        self.ignite_nodes_random(num_to_ignite)
        self.simulate_fire_spread()
        return

    # resets the neighborhood completely. Useful for running simulation trials.
    def reset_neighborhood(self):  # resets the neighborhood
        for node in self.nodes:
            node.set_state(0)
            node.caught_primary = False
            node.caught_secondary = False
            if type(node) is House:
                node.mitigate(0)
            node.clear_edges()
        self.mitigate_houses_random()
        self.connect_nodes()
        return

    '''The following functions handle data from the simulation'''

    # Statistics handler
    def data_handler(self, desired_data):
        """
        Handles processing of data for a single neighborhood.
        """
        returned_dict = dict()
        if "# of Houses Affected by Primary" in desired_data:
            returned_dict["# of Houses Affected by Primary"] = self.get_num_of_houses_set_alight_by_primary()
        if "# of Houses Affected by Secondary" in desired_data:
            returned_dict["# of Houses Affected by Secondary"] = self.get_num_of_houses_set_alight_by_secondary()
        if "Total # of Houses Affected" in desired_data:
            returned_dict["Total # of Houses Affected"] = self.get_num_of_houses_set_alight()
        if "Standard Deviation of # of Affected Houses" in desired_data:
            returned_dict["Standard Deviation of # of Affected Houses"] = self.get_num_of_houses_set_alight()
        if "Number of Houses Mitigated" in desired_data:
            returned_dict["Number of Houses Mitigated"] = self.get_num_of_houses_mitigated()
        if "Heatmap" in desired_data:
            returned_dict["Heatmap"] = self.get_heatdata()
        return returned_dict

    def get_num_of_houses_set_alight_by_primary(self):
        num_of_houses = 0
        for house in self.houses:
            if house.get_state() in [1, 3]:
                num_of_houses += 1
        return num_of_houses

    def get_num_of_houses_set_alight_by_secondary(self):
        num_of_houses = 0
        for house in self.houses:
            if house.get_state() in [2, 4]:
                num_of_houses += 1
        return num_of_houses

    def get_num_of_houses_set_alight(self):
        return self.get_num_of_houses_set_alight_by_primary() + self.get_num_of_houses_set_alight_by_secondary()

    def get_num_of_houses_mitigated(self):
        num_mitigated = 0
        for house in self.houses:
            if house.is_mitigated():
                num_mitigated += 1
        return num_mitigated

    def get_heatmap(self):
        warn("get_heatmap() will be deprecated.", DeprecationWarning, stacklevel=2)
        dim = self.get_dimensions()
        heatmap_array = list()
        for _ in range(dim[1]):
            row = list()
            for _ in range(dim[0]):
                row.append(0)
            heatmap_array.append(row)
        for node in self.nodes:
            if node.get_state() in [1, 2, 3, 4]:
                heatmap_array[node.get_coords()[0]][node.get_coords()[1]] = 1
        return heatmap_array

    def get_heatdata(self):
        """ This method replaces get_heatmap, which will be deprecated, in returning heat information. """
        heatmap_data = list()
        for node in self.nodes:
            if node.get_state():
                heatmap_data.append((type(node), node.get_coords(), 1))
            else:
                heatmap_data.append((type(node), node.get_coords(), 0))
        return heatmap_data
