# import start

import sys
import os
import math

import pandas as pd
import numpy as np
from io import StringIO


import dataframeHandler as dataframeHandler
from dataframeHandler import DataFrameList
import similarityCalculator as similarityCalculator
from similarityCalculator import UserSimilarityList

import formulaCalculator as formulaCalculator

# import end



# ✨ variable definition start

movieList:list = []
reviewList:list = []
weightList:UserSimilarityList



categoryDict:UserSimilarityList = {}


finalResult:dict[float, str] = {}


reviewFolderpath:str = "undefined"




#userPreferWeightList:dict[str, list[tuple[float, float]]] = {}


# ✨ variable definition end



















# 📚 function definition start

def getParameterValue() -> list:
    """
    파라메터에서 영화 목록을 불러오는 함수
    """
    _movieList:list = []
    try:
        _movieList:list = []

        for token in sys.argv[1][1:len(sys.argv[1])-1].split(","):
            _movieList.append(token.replace("*", " "))
            

        return _movieList
    except:
        print("파라메터 양식이 맞지 않습니다")

        return []


def getReviewList() -> list:
    """
    리뷰 폴더에서 리뷰 목록을 불러와 영화 목록으로 만드는 함수
    """

    _movieList:list = []
    for file in os.listdir(reviewFolderpath):
        _movieList.append(file.split("_categorized_words.csv")[0])

    return _movieList


def getWeightBetweenMovies(movies:list) -> UserSimilarityList:
    """
    영화 목록을 통해 가중치값을 산출해내는 함수

    :movies: - 사용자가 선택한 영화 목록
    :reviews: - 전체 영화 목록
    """
    categoryDict:UserSimilarityList = {}
    for movie in movies:
        _filepath:str = reviewFolderpath+movie+"_categorized_words.csv"
        # 데이터 프레임 리스트
        _dfList:DataFrameList = dataframeHandler.splitDataFrame22(_filepath)

        df1 = _dfList[0]
        df2 = _dfList[1]

        

        categoryDict = similarityCalculator.getMovieCalculatedWeight(df1, df2, categoryDict)

        """
        categoryDict가 List로 전달되야 하는 건 아닌지???
        찾아보니까 getMovieCalculatedWeight는 가중치 하나를 반환하는게 맞는데, 그걸 넘겨주면 
        """

    return similarityCalculator.getUserPreferWeightList(categoryDict)

def compareAllMovies(weightlist:UserSimilarityList, movielist:list[str], reviewlist:list[str]):

    


    for reviewComponent in reviewlist:
        if reviewComponent not in movielist:

            _totalScoreOfMovie:float = 0

            #print(reviewComponent)





            _filepath:str = reviewFolderpath+reviewComponent+"_categorized_words.csv"

            _dfList:DataFrameList = dataframeHandler.splitDataFrame22(_filepath)
            categoryDict:UserSimilarityList = {}

            df1 = _dfList[0]
            df2 = _dfList[1]

            #영화의 계산 가중치
            categoryDict = similarityCalculator.getMovieCalculatedWeight(df1, df2, categoryDict)

            for keyToken in categoryDict.keys():
                _distance_multiplier:float = 0
                _similarity_multiplier:float = 0

                if (categoryDict.get(keyToken) == None) or (weightlist.get(keyToken) == None):
                    continue

                _distance:float = weightlist[keyToken][0][0]
                _similarity:float = weightlist[keyToken][0][1]

                _distance2:float = categoryDict[keyToken][0][0]
                _similarity2:float = categoryDict[keyToken][0][1]


                _distance_multiplier = formulaCalculator.getWeightFromGapBetweenDistance(np.abs(_distance - _distance2), 10, 2, 0.2)
                _similarity_multiplier = formulaCalculator.getWeightFromGapBetweenWeight(np.abs(_similarity - _similarity2))

                _totalScoreOfMovie = _totalScoreOfMovie + (_similarity * _distance_multiplier * _similarity_multiplier)

            print(f"영화 최종 추천도 영화 : {reviewComponent} / 추천도 : {_totalScoreOfMovie}")

            finalResult[_totalScoreOfMovie] = reviewComponent

    sorted_result = dict(sorted(finalResult.items(), key=lambda item: item[0], reverse=True))

    #print(sorted_result)
    _ccnt = 0
    for sortToken in sorted_result:
        print(f"{_ccnt}위 : {sorted_result[sortToken]}")
        _ccnt = _ccnt + 1







    





# 📚 function definition end













# 📝 configuration start

reviewFolderpath = "../../csvfile/"

# 📝 configuration end









# system initial code start



# system initial code end







# 💻 initial code start

reviewList = getReviewList()
movieList = getParameterValue()
print(movieList)

weightList = getWeightBetweenMovies(movieList)





print(reviewList)


print("✨가중치 목록을 출력합니다")
print(weightList)

compareAllMovies(weightList, movieList, reviewList)

# 💻 initial code end