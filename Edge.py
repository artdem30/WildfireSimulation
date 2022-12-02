import math

import numpy as np
from Node import House
import Paramaters as Par


def distance_risk_factor(r, k=1.5, q=4):
    """
    This function produces the distance factor of the direct risk equation using a sigmoid function normalized such that
        it fulfills the following criteria:
            i. The function must be bound to the range [0,1] over the domain [0,inf]
            ii. f(r = 0) = 1
            iii. f(a) >= f(b), a < b
            iv. r -> inf ==> f(r) -> 0
    :param r: the distance between nodes
    :param k: determines how steep the falloff is with respect to r, arbitrarily defaults to 1.5
    :param q: determines where the falloff occurs along the horizontal axis, arbitratily defaults to 4
    :return: the distance factor calculated as
                (np.exp(-k(-q/k)) + q) / np.exp(-k(-q/k)) * (np.exp(-k(r - q/k)) / (np.exp(-k(r - q/k)) + q))
    """
    norm_factor = (np.exp(-k * (-q / k)) + q) / np.exp(-k * (-q / k))
    distance_variable_factor = np.exp(-k * (r - q / k)) / (np.exp(-k * (r - q / k)) + q)
    return distance_variable_factor * norm_factor


# Not ready for 3D
def angle(node1, node2):
    return np.arctan2((node2.coords[1] - node1.coords[1]), (node2.coords[0] - node1.coords[0]))


# Ready for 3D
def distance(node1, node2):
    return np.sqrt(np.sum((np.array(node1.coords) - np.array(node2.coords)) ** 2))


# Factors in elevation by giving a maximum bonus probability of .2 if node2 is uphill from the spreading node.
# Does nothing if downhill.
def elevation(node1, node2):
    elev_diff = node2.elevation - node1.elevation
    bonus_prob = .2 / (1 + math.e ** (-.2 / (elev_diff - 10)))
    return bonus_prob


# A function to handle the distance prefactor; so that we can easily change it
def flat_distance_factor(dist):
    return 0.8 if dist == 1 else 0


class Edge:
    """This class represents the edges between houses. An edge holds the distance and edge angle between two houses, as
    well as other parameters. An edge determines the probability of fire spread between two houses."""

    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        ang = angle(node1, node2)  # determines the angle of an edge in relation to the East.
        dist = distance(node1, node2)  # distance between two coordinates.
        # associates distance with its probability of fire spread.
        distance_factor = distance_risk_factor(dist)
        elevation_factor = elevation(node1, node2)
        wind_angle = np.radians(Par.WIND_DIRECTION)  # converts wind angle to radians\
        # calculates wind multiplier using wind angle and edge angle.
        wind_multiplier = 0 if (wind_angle - ang) <= 0 else \
            np.cos(wind_angle - ang) * Par.WIND_SPEED_MULTIPLIER
        mitigation_factor = 1 if type(node2) is not House else (1 - node2.mitigation_level)
        spreadability_factor = node1.spreadability
        # This calculates the final probability that an edge holds.
        self.probability = spreadability_factor * mitigation_factor * distance_factor + elevation_factor

    '''___Getters___'''

    def get_probability(self):
        return self.probability
