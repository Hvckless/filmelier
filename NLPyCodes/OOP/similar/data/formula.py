#import numpy as np
import math

class FormulaCalculator:
    def __init__(self):
        self.initial = 1
    # def getWeightFromGapBetweenWeight(self, x:float)->float:
    #     return (-2 / np.pi) * np.arctan(2 * x - 2) + 1
    # def getWeightFromGapBetweenDistance(self, x:float, maxdistance:float, max:float, min:float)->float:
    #     if x > 10:
    #         x = 10
    #     return ((max-min)/2) * np.cos(x * (np.pi/maxdistance))+((max+min)/2)
    
    def getWeightFromGapBetweenWeight(self, x:float)->float:
        return (-2 / math.pi) * math.atan(2 * x - 2) + 1

    def getWeightFromGapBetweenDistance(self, x:float, maxdistance:float, max:float, min:float)->float:
        if x > 10:
            x = 10
        return ((max - min) / 2) * math.cos(x * (math.pi / maxdistance)) + ((max + min) / 2)