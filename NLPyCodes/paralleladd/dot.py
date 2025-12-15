import numpy as np
import math

def betWeight(x:np.ndarray)->np.ndarray:
    return (-2/np.pi)*np.arctan(2*x-2)+1
def betDistance(x:np.ndarray,maxdistance:float, max:float, min:float)->np.ndarray:
    x_clamped = np.minimum(x, 10.0)

    return ((max-min)/2)*np.cos(x_clamped*(np.pi/maxdistance))+((max+min)/2)

A = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,9]
])

# B = np.array([
#     [2,2,2],
#     [2,2,2],
#     [2,2,2]
# ])

# C = A * B

# print(C)

D = betDistance(A, 10, 2, 0.2)

print(D)