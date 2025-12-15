import numpy as np

WeightNPList = dict[str, list[np.ndarray]]
WeightList = dict[str, list[tuple[float, float]]]
"""
영화를 데이터로 바꿀 때 사용하는 가중치 구조체\n
{"키 문자열" : [(위치:float,유사도:float),((위치:float,유사도:float))]}\n
위 형식으로 구현되어있음
"""
MovieWeightList = dict[str, WeightList]
MovieWeightNPList = dict[str,WeightNPList]