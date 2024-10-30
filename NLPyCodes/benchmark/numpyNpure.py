import math
import time
import random

import numpy as np

DIM_LENGTH = 100000

class FormulaCalculator:
    def __init__(self):
        self.initial = 1
    def getWeightFromGapBetweenWeight(self, x):
        return (-2 / np.pi) * np.arctan(2 * x - 2) + 1
    def getWeightFromGapBetweenDistance(self, x, maxdistance, max, min):
        if x > 10:
            x = 10
        return ((max-min)/2) * np.cos(x * (np.pi/maxdistance))+((max+min)/2)
    

class FormulaOne:
    def getWeightFromGapBetweenWeight(self, x):
        return (-2 / math.pi) * math.atan(2 * x - 2) + 1

    def getWeightFromGapBetweenDistance(self, x, maxdistance, max, min):
        if x > 10:
            x = 10
        return ((max - min) / 2) * math.cos(x * (math.pi / maxdistance)) + ((max + min) / 2)
    


if __name__ == "__main__":

    formula_calculator = FormulaCalculator()
    formula_one = FormulaOne()

    

    initial_array = [random.uniform(0, 1) for _ in range(DIM_LENGTH)]
    result_weight_array = []
    result_distance_array = []

    start_time = time.time()

    for i in range(DIM_LENGTH):
        result_weight_array.append(formula_one.getWeightFromGapBetweenWeight(initial_array[i]))
        result_distance_array.append(formula_one.getWeightFromGapBetweenDistance(initial_array[i], 10, 2, 0.2))
            
    print(f"Pure Python elapsed time : {time.time()-start_time}")

    result_weight_array = []
    result_distance_array = []

    some_time = time.time()
    for i in range(DIM_LENGTH):
        result_weight_array.append(formula_calculator.getWeightFromGapBetweenWeight(initial_array[i]))
        result_distance_array.append(formula_calculator.getWeightFromGapBetweenDistance(initial_array[i], 10, 2, 0.2))
    print(f"NumPy elapsed time : {time.time() - some_time}")