import matplotlib.cm
import numpy as np
import matplotlib.pyplot as plt
from Node import *

colormap = matplotlib.cm.get_cmap('hot_r')


def visualize_neighborhood(objects):
    plt.cla()
    for obj in objects:
        if obj[0] == 'h':
            plt.scatter(obj[1][0], obj[1][1], s=150, c=[[99/255, 52/255, 14/255]])
            plt.text(obj[1][0], obj[1][1], "H", ha="center", va="center")
        if obj[0] == 'bT':
            plt.scatter(obj[1][0], obj[1][1], s=88, c=[[73/255, 112/255, 82/255]])
            plt.text(obj[1][0], obj[1][1], "bT", ha="center", va="center")
        if obj[0] == 'sT':
            plt.scatter(obj[1][0], obj[1][1], s=75, c=[[24/255, 99/255, 14/255]])
            plt.text(obj[1][0], obj[1][1], "sT", ha="center", va="center")
        if obj[0] == 'sh':
            plt.scatter(obj[1][0], obj[1][1], s=60, c=[[159/255, 124/255, 75/255]])
            plt.text(obj[1][0], obj[1][1], "sh", ha="center", va="center")
        if obj[0] == 'la':
            plt.scatter(obj[1][0], obj[1][1], s=100, c=[[46/255, 165/255, 73/255]])
            plt.text(obj[1][0], obj[1][1], "la", ha="center", va="center")
    plt.gca().invert_yaxis()
    plt.axis("equal")
    plt.show()
    return


def visualize_aftermath(heat_array, num_of_fires, title):
    plt.cla()
    for obj_type in heat_array.keys():
        for obj_coords in heat_array[obj_type].keys():
            heat_val = np.round(heat_array[obj_type][obj_coords] / num_of_fires, 2)
            coords = obj_coords
            color = np.array([colormap(heat_val)]) + np.array([0, 0, 0, -0.5])
            inverted_color = np.array([1, 1, 1, 2]) - np.array([colormap(heat_val)])
            inverted_color = [inverted_color[0][0], inverted_color[0][1], inverted_color[0][2], inverted_color[0][3]]
            if obj_type is House:
                plt.scatter(coords[0], coords[1], c=color, s=300)
                plt.text(coords[0], coords[1], "H", ha="center", va="center", c=inverted_color)
            elif obj_type is BigTree:
                plt.scatter(coords[0], coords[1], c=color, s=300)
                # plt.text(coords[0], coords[1], "bT", ha="center", va="center", c=inverted_color)
            elif obj_type is SmallTree:
                plt.scatter(coords[0], coords[1], c=color, s=300)
                # plt.text(coords[0], coords[1], "sT", ha="center", va="center", c=inverted_color)
            elif obj_type is Shrub:
                plt.scatter(coords[0], coords[1], c=color, s=300)
                # plt.text(coords[0], coords[1], "sh", ha="center", va="center", c=inverted_color)
            elif obj_type is Lawn:
                plt.scatter(coords[0], coords[1], c=color, s=300)
                # plt.text(coords[0], coords[1], "la", ha="center", va="center", c=inverted_color)
    plt.gca().invert_yaxis()
    plt.axis("equal")
    plt.show()
    return
