from Neighborhood import Neighborhood
import numpy as np


class Simulation:
    """
    This class handles a single run of a number of fire spread simulations, and provides stats.
    """

    def __init__(self, desired_statistics, objects):
        self.statistics = dict()
        for desired_stat in desired_statistics:
            self.statistics[desired_stat] = list()
        self.objects = objects

    def run_simulation(self, num_of_iterations):
        neighborhood = Neighborhood(self.objects)
        if "Heatmap" in self.statistics.keys():
            self.statistics["Heatmap"] = dict()
        for iteration in range(num_of_iterations):
            neighborhood.simulate_random_border_fire()
            desired_vals = neighborhood.data_handler(self.statistics.keys())
            for key in self.statistics.keys():
                if key == "Heatmap":
                    for node in desired_vals[key]:
                        if node[0] not in self.statistics[key].keys():
                            self.statistics[key].update({node[0]: {node[1]: node[2]}})
                        else:
                            if node[1] not in self.statistics[key][node[0]]:
                                self.statistics[key][node[0]].update({node[1]: node[2]})
                            else:
                                self.statistics[key][node[0]][node[1]] += node[2]
                else:
                    self.statistics[key].append(desired_vals[key])
            neighborhood.reset_neighborhood()
        for key in self.statistics.keys():
            if key == "Standard Deviation of # of Affected Houses":
                self.statistics[key] = np.std(self.statistics[key])
            elif key == "Heatmap":
                pass
            else:
                self.statistics[key] = np.mean(self.statistics[key])
        return

    def get_statistics(self):
        return self.statistics
