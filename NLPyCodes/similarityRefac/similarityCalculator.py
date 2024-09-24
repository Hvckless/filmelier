import math

import pandas as pd

from colorama import Fore, Style, init






# variable definition

COLOR:list[str] = [Fore.RED, Fore.RED, Fore.RED, Fore.RED, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.YELLOW, Fore.MAGENTA, Fore.MAGENTA, Fore.MAGENTA]









# initial code

init(autoreset=True)











# type definition

UserSimilarityList = dict[str, list[tuple[float, float]]]













def getUserPreferWeightList(categoryDict:UserSimilarityList)->UserSimilarityList:
    """
    위치, 유사도 테이블을 받아서 평균 거리와 유사도를 반환하는 함수
    :categoryDict: 각 카테고리에 여러개의 (1~. 보통 2 이상) 위치, 유사도 값들이 있는 UserSimilarityList
    :return: 카테고리당 위치,유사도 쌍이 한개씩 들어있는 평균 유사도 맵
    """

    _userPreferWeightList:UserSimilarityList = {}

    for categoryToken in categoryDict.keys():
        _sum_of_similarity:float = 0
        _avg_of_similarity:float = 0

        _sum_of_distance:float = 0
        _avg_of_distance:float = 0

        _list_of_similarity:list[tuple[float, float]] = categoryDict.get(categoryToken,[(0,0)])
        

        for simil in _list_of_similarity:
            _sum_of_similarity = _sum_of_similarity + simil[1]
            _sum_of_distance = _sum_of_distance + simil[0]

        _avg_of_similarity = _sum_of_similarity/len(_list_of_similarity)
        _avg_of_distance = _sum_of_distance/len(_list_of_similarity)


        if _userPreferWeightList.get(categoryToken) == None:
            _userPreferWeightList[categoryToken] = []
        _userPreferWeightList[categoryToken].append((_avg_of_distance, _avg_of_similarity))

        

        #print(f"avg(similarity) : {_avg_of_similarity:.3f}\t\tavg(distance) : {_avg_of_distance}\t\tToken : {categoryToken}")

    return _userPreferWeightList



def getMovieCalculatedWeight(df1:pd.DataFrame, df2:pd.DataFrame, referCategory:UserSimilarityList)->UserSimilarityList:
    # 카테고리 - 유사도 쌍 Map
    _categoryAVG:dict[str,float] = {}
    categoryDict:UserSimilarityList = referCategory





    for token in df2["Category"]:
        _categoryAVG[token] = df1.loc[df1["Category"] == token]["Similarity"].mean()

    percentage = 0

    totalcnt = df2["Count"].sum()

    #print(df2.count().iloc[1])
    #print(movie)
    for token in _categoryAVG.keys():
        # 유사도 -> 레벨 변환값. 수준에 따른 색 변경에 사용
        value = (math.floor(_categoryAVG[token]*10));
        cnt = df2.loc[df2["Category"] == token]["Count"].iloc[0]
        
        percentage = cnt/totalcnt

        percentage_multiplier:float = percentage*df2.count().iloc[1]
        calculated_multiplier:float = _categoryAVG[token] * percentage_multiplier

        _index:int = df2[df2["Category"] == token].index[0]

        if categoryDict.get(token) == None:
            categoryDict[token] = []
        categoryDict[token].append((_index, calculated_multiplier))

        print(f"{COLOR[value]}{token} : {_categoryAVG[token]:.3f}\t| {cnt} \t {percentage_multiplier} \t {calculated_multiplier}")


    return categoryDict