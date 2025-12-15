import numpy as np
import time
import random


def generate_predata(element_length):
    """
    """
    data = [random.random() for _ in range(element_length)]

    numpy_data = np.array(data)
    
    return data, numpy_data

def numpy_sum_experiment(numpy_data):
    """
    Numpy를 이용해 부동소숫점을 더하는 함수
    """

    total_sum = np.sum(numpy_data)

    return total_sum

def python_sum_experiment(data):
    """
    """
    total_sum = 0.0

    for value in data:
        total_sum += value

    return total_sum



if __name__ == "__main__":
    data, npdata = generate_predata(1500)

    start_time = time.perf_counter()

    py_result = python_sum_experiment(data)

    end_time = time.perf_counter()

    print(f"파이썬 코드 결과 : {py_result} {(end_time-start_time):.9f}")

    np_start_time = time.perf_counter()

    np_result = numpy_sum_experiment(npdata)

    np_end_time = time.perf_counter()

    print(f"NumPy 코드 결과 : {np_result} {(np_end_time-np_start_time):.9f}")
    pass