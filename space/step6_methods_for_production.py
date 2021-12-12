# -*- coding: utf-8 -*-
import joblib
import numpy as np
import os
import random
# define a function to calculate distance between two points from whom we have GPS coordinates
from math import sin, cos, sqrt, atan2, radians

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

model_filename = os.path.abspath(ROOT_DIR + "/finalized_model.sav")
faults_filename = os.path.abspath(ROOT_DIR + "/Nevada_faults.npy")

Nevada_faults = np.load(faults_filename)
loaded_model = joblib.load(model_filename)

height, width, _ = Nevada_faults.shape

# load the colors of the faults (colors from the ESRI legend)
colors = np.zeros((7, 3))
colors[0] = [255, 147, 142]
colors[1] = [255, 177, 151]
colors[2] = [242, 220, 161]
colors[3] = [166, 187, 138]
colors[4] = [136, 166, 211]
colors[5] = [128, 128, 128]
colors[6] = [167, 167, 167]


# approximate radius of earth in km
def distance_km(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def create_fault_features(longitude0, latitude0):
    """
    returns a list of 7 elements: the 7 distances to the nearest fault of each color

    notice: only works for Nevada, if outside of Nevada, returns random numbers
    """

    NEVADA_SOUTH, NEVADA_NORTH = 35, 42
    NEVADA_WEST, NEVADA_EAST = -120, -114
    HEIGHT = NEVADA_NORTH - NEVADA_SOUTH
    WIDTH = NEVADA_EAST - NEVADA_WEST

    # returns random values if we are not in Nevada
    if longitude0 < NEVADA_WEST or longitude0 > NEVADA_EAST or latitude0 < NEVADA_SOUTH or latitude0 > NEVADA_NORTH:
        distances = []
        for i in range(7):
            distances.append(random.random() * 10)
        return distances

    # initialize the new features with "infinite" values
    blue_colors = colors[:, 2]
    distances = [10000] * 7

    current_i = int((NEVADA_NORTH - latitude0) / HEIGHT * height)
    current_j = int((longitude0 - NEVADA_WEST) / WIDTH * width)

    start_i = max(0, current_i - 50)
    end_i = min(height, current_i + 50)

    start_j = max(0, current_j - 50)
    end_j = min(width, current_j + 50)

    for i in range(start_i, end_i):
        # if i % 100 == 0:
        #   print(i)
        for j in range(start_j, end_j):
            color_pix = Nevada_faults[i, j]
            # a small trick is to notice that all the 8 colors ( 7 feature colors and white) are uniquely determined
            # by their blue channel value:
            blue_intensity = color_pix[2]
            is_white = (blue_intensity == 255)
            if is_white:
                continue
            # now detect the feature color
            for idx, blue_color in enumerate(blue_colors):

                if blue_intensity == blue_color:
                    longitude1 = NEVADA_WEST + j / width * WIDTH
                    latitude1 = NEVADA_NORTH - i / height * HEIGHT
                    current_distance = distance_km(latitude0, longitude0, latitude1, longitude1)

                    distances[idx] = min(distances[idx], current_distance)

                    break
    return distances


def good_or_bad_location(long, lat):
    """
    returns the prediction of good or bad location for a well at these GPS coordinates
    output: 0 if bad and 1 if good
    most of the location will be bad, only a few will be good (maybe 3% of locations are good)
    """
    return loaded_model.predict([create_fault_features(long, lat)]).sum()


def predict(lat, lng, limit=20, tries=1000, scale=1):
    cnt, results = 0, []
    for i in range(tries):
        lat0, lng0 = lat + scale * (random.random() - random.random()), \
                     lng + scale * (random.random() - random.random())

        result = good_or_bad_location(lng0, lat0)

        if result > 0:
            results.append({"lat": lat0, "lng": lng0})

        if len(results) >= limit:
            break


    return results