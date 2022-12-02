import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from warnings import warn

"""All the file writing and heatmap functions are stored here."""


def produce_heatmap(heat_arr, num_of_fires, title):
    warn("produce_heatmap() will be deprecated.", DeprecationWarning, stacklevel=2)
    heat_stat = np.round(np.array(heat_arr) / num_of_fires, 2)
    plt.imshow(heat_stat, cmap='hot_r', origin='lower')
    plt.yticks(np.arange(10))
    plt.xticks(np.arange(10))
    for i in range(len(heat_stat)):
        for j in range(len(heat_stat[0])):
            plt.text(j, i, heat_stat[i, j],
                     ha="center", va="center", color="k")
    plt.title(title)
    plt.colorbar(label="Probability of Fire")
    plt.clim(0, 1)
    plt.tight_layout()
    plt.savefig(os.path.join("Results", title))
    plt.show()


# writes csv stats for a simple simulation.
def write_simple_stats(csv_file_name, stats_dict, num_of_fires, heatmap_title='Heatmap'):
    with open(os.path.join("Results", csv_file_name), 'w') as csvfile:
        statwriter = csv.writer(csvfile)
        statwriter.writerow(list(stats_dict.keys()))
        data = list()
        for stat in stats_dict.keys():
            if stat == "Heatmap":
                produce_heatmap(stats_dict.get(stat), num_of_fires, heatmap_title)
            else:
                data.append(stats_dict.get(stat))
        statwriter.writerow(data)
    return


# writes csv stats for a mitigation level test simulation.
def write_2d_stats(csv_file_name, data):
    with open(os.path.join("Results", csv_file_name), 'w') as csvfile:
        statwriter = csv.writer(csvfile)
        for row in data:
            statwriter.writerow(row)
    return
