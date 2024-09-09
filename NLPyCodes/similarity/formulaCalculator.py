import numpy as np


def getWeightFromGapBetweenWeight(x:float)->float:
    return (-2 / np.pi) * np.arctan(2 * x - 2) + 1

def getWeightFromGapBetweenDistance(x:float, maxdistance:float, max:float, min:float)->float:
    if x > 10:
        x = 10
    return ((max-min)/2) * np.cos(x * (np.pi/maxdistance))+((max+min)/2)