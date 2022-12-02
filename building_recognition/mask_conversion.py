import cv2
import numpy as np
import Paramaters as par

mask_path = "dataset/train/masks/austin34.png"


def to_image_array(tensor):
    t = (tensor > .5).int()
    img = t.cpu().numpy().squeeze(0).transpose(1, 2, 0).squeeze(2).astype('uint8')
    return img


def generate_bbox(image, mask):
    mask = to_image_array(mask)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = list()
    for cnt in contours:
        box = cv2.boundingRect(cnt)
        boxes.append(box)
    boxes = delete_small_boxes(boxes)
    for box in boxes:
        x, y, w, h = box
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return image, boxes


def box_area(box):
    return box[2] * box[3]


def delete_small_boxes(box_array):
    areas = np.empty(len(box_array))
    for i, box in enumerate(box_array):
        areas[i] = box_area(box)
    lower_limit = np.median(areas) / 3
    outliers = list()
    for i, area in enumerate(areas):
        if area < lower_limit:
            outliers.append(i)
    boxes = np.delete(box_array, outliers, 0)
    return boxes


def get_center_coordinates(box_array):  # gives coordinates on the pixel map. Need scale to determine true coordinates.
    coordinates = np.zeros(len(box_array), dtype=object)
    for i, box in enumerate(box_array):
        x, y, w, h = box
        coord = ('h',((x + w / 2)/par.MAP_SCALE, (y - h / 2)/par.MAP_SCALE))
        coordinates[i] = coord
    return coordinates

