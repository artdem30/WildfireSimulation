import imageio.v2 as iio
import numpy as np
from visualization import visualize_neighborhood
from sys import exit

# Here, input the color values signifying different objects in yout png
HOUSE = [99, 52, 14]
SMALLTREE = [24, 99, 14]
BIGTREE = [73, 112, 82]
LAWN = [46, 165, 73]
SHRUB = [159, 124, 75]
# This is the image you will be loading and processing
img_name = 'WestCountyHawkWatch.png'


class NoObjectsError(Exception):
    """ This class exists to better describe to the user that none of the objects in the image are valid. """
    pass


def distance(coords1, coords2):
    return np.sqrt(np.sum((np.array(coords1) - np.array(coords2)) ** 2))


def process_image(img):
    print("extracting obj")
    objects = extract_objects(img)
    print("scaling map")
    objects = scale_map(objects)
    print("shifitng map")
    objects = shift_map(objects)
    return objects


def extract_objects(img):
    im = iio.imread(img)
    objects = list()
    for row in range(im.shape[0]):
        for col in range(im.shape[1]):
            definite_obj = None
            potential_obj = im[row][col]
            if (potential_obj == HOUSE).all():
                definite_obj = ('h', (col, row))
            elif (potential_obj == SMALLTREE).all():
                definite_obj = ('sT', (col, row))
            elif (potential_obj == BIGTREE).all():
                definite_obj = ('bT', (col, row))
            elif (potential_obj == LAWN).all():
                definite_obj = ('la', (col, row))
            elif (potential_obj == SHRUB).all():
                definite_obj = ('sh', (col, row))
            if definite_obj:
                objects.append(definite_obj)
    if len(objects) == 0:
        raise NoObjectsError
    else:
        return objects


def scale_map(objects):
    min_dist = None
    for obj1 in objects:
        if obj1[0] == 'h':
            for obj2 in objects:
                if obj1 is not obj2 and obj2[0] == 'h':
                    try:
                        dist = distance(obj1[1], obj2[1])
                        if dist <= min_dist:
                            print(f"{obj1[1]}")
                            min_dist = dist
                    except TypeError:
                        min_dist = distance(obj1[1], obj2[1])
    # Added to avoid overrepresentation of objects (accidentally putting down multiple pixels for one object)
    proceed = input(f"Min distance is {min_dist}. Proceed? Y/N")
    if proceed == "Y":
        for i in range(len(objects)):
            objects[i] = (objects[i][0], objects[i][1]/min_dist)
    else:
        exit()
    return objects


def shift_map(objects):
    min_x = objects[0][1][0]
    min_y = objects[0][1][1]
    for obj in objects:
        min_x = min(min_x, obj[1][0])
        min_y = min(min_y, obj[1][1])
    for i in range(len(objects)):
        objects[i] = (objects[i][0], (objects[i][1][0] - min_x + 1, objects[i][1][1] - min_y + 1))
    return objects


if __name__ == '__main__':
    obs = process_image(img_name)
    print(obs)
    visualize_neighborhood(obs)
