import math

import numpy as np

from similar.data.formula import FormulaCalculator
from similar.file.filereader import FileReader
from similar.file.file import File
from similar.csv.csv import CSV
from similar.csv.csv import CSVList

from similar.enum.CSVFormat import CSVFormat
from similar.data.color import COLOR

from similar.data.weight import WeightList
from similar.data.movie import MovieList
from similar.data.movie import ScoredMovieList


class WeightCalculator:
    def __init__(self):
        self.initial = 1

    
    def getWeightBetweenMovies(self)->WeightList:
        result:WeightList = {}

        return result
    
    def compareAllMovieWeightList(self, review_folderpath:str, weightlist:WeightList, mvlist_param:MovieList, mvlist_review:MovieList, format:CSVFormat)->ScoredMovieList:
        """
        평균 가중치와 개별 영화의 가중치를 비교하는 함수

        :review_folderpath: (str) 리뷰 폴더의 경로
        :weightlist: (WeightList) 평균가중치
        :mvlist_param: (MovieList) 파라메터에서 가져온 영화 목록
        :mvlist_review: (MovieList) 리뷰 파일에서 가져온 영화 목록
        :format: (CSVFormat) csv 구조 버전

        return (ScoredMovieList) 점수가 부여된 영화 목록
        """

        scorelist:ScoredMovieList = {}

        #리뷰 == 영화, review == movie
        for review in mvlist_review:
            #리뷰가 입력된 파라메터에 없다면 -> 비교 대상 영화
            if review not in mvlist_param:

                score:float = 0

                target_movie_weightlist:WeightList = self.getWeightFromMovieElement(review_folderpath+review+"_categorized_words.csv", format, {})

                for category in target_movie_weightlist.keys():
                    distance_multiplier:float = 0
                    similarity_multiplier:float = 0

                    if (weightlist.get(category) == None) or (target_movie_weightlist.get(category) == None):
                        continue

                    distance:float = weightlist[category][0][0]
                    similarity:float = weightlist[category][0][1]

                    target_distance:float = target_movie_weightlist[category][0][0]
                    target_similarity:float = target_movie_weightlist[category][0][1]

                    distance_multiplier:float = FormulaCalculator().getWeightFromGapBetweenDistance(np.abs(distance - target_distance), 10, 2, 0.2)
                    similarity_multiplier:float = FormulaCalculator().getWeightFromGapBetweenWeight(np.abs(similarity - target_similarity))

                    score = score + (similarity * distance_multiplier * similarity_multiplier)

                    
                scorelist[score] = review

        return scorelist
    

    def getWeightFromMovieList(self, reviewpath:str, mvlist_param:MovieList, format:CSVFormat)->WeightList:
        """
        영화 목록에서 가중치를 가져와서 하나로 합치는 함수.
        결과 파일은 '유쾌':[(1,0.23),(10,1.2)]와 비슷한 형식으로 구성된다.

        :reviewpath: 리뷰 파일이 실제로 있는 위치
        :mvlist_param: 파라메터에서 가져온 (MovieList)타입 데이터

        return (WeightList) 최종 평균가중치
        """

        """
        TO-DO LIST

        1. 영화 목록 가져오기

        """
        weightpoints:WeightList = {}
        for movie_name in mvlist_param:
            filepath:str = reviewpath+movie_name+"_categorized_words.csv"
            
            weightpoints = self.getWeightFromMovieElement(filepath, format, weightpoints)
            
        weightpointsV2:WeightList = self.getWeightFromMovieWithDistance(weightpoints)

        return weightpointsV2
    
    def getWeightFromMovieElement(self, filepath:str, format:CSVFormat, originalWeightList:WeightList)->WeightList:
        """
        파일에서 실제 가중치 목록(WeightList)을 불러와 기존 가중치 목록과 합치는 함수.

        :filepath: (str) 파일 경로
        :format: (CSVFormat) 파일 구조의 버전
        :originalWeightList: (WeightList) 기존의 WeightList가 없다면 {}으로 설정.

        return (WeightList) 결과물 가중치
        """
        csv_table:CSVList = FileReader().readCSVTables(filepath, format)

        df1 = csv_table[0].getDataFrame()
        df2 = csv_table[1].getDataFrame()

        category_avg_map:dict[str,float] = {}
        weightlist:WeightList = originalWeightList

        if type("10") == int:
            print("HI")
        elif type("10") == str:
            print("BYE")

        #Count의 모든 값은 결국 모든 형태소의 갯수와 같다
        morphemeCNT:int = df2["Count"].sum()

        for category in df2["Category"]:
            #"Category"의 평균. 쉬운 접근을 위해 만들었다. 싫으면 df1.loc[df["Category"] == category]["Similarity"].sum()으로 접근하던지.
            category_avg_map[category] = df1.loc[df1["Category"] == category]["Similarity"].mean()

            #적절한 색 값을 입히기 위해 만든 인덱스. 알고리즘상으로 의미는 없다. 그냥 보기 편하라고.
            color_index = math.floor(category_avg_map[category]*10)

            #카테고리에 포함되는 형태소 갯수를 의미한다.
            category_cnt:int = df2.loc[df2["Category"] == category]["Count"].iloc[0]

            morph_cate_ratio:float = category_cnt / morphemeCNT


            percentage_multiplier:float = morph_cate_ratio * df2.count().iloc[1]
            similarity_final_multiplier:float = category_avg_map[category] * percentage_multiplier

            category_index:int = df2[df2["Category"] == category].index[0]

            if weightlist.get(category) == None:
                weightlist[category] = []
            weightlist[category].append((category_index, similarity_final_multiplier))

            print(f"{COLOR[color_index]}{category} : {category_avg_map[category]:.3f}\t| {category_cnt} \t {percentage_multiplier} \t {similarity_final_multiplier}")

        return weightlist
        """
        category_avg_map의 key는 사실 df2["Category"]의 category기 때문에
        아래 코드는 쓸데 없는 반복이다.
        """
           
        """
        for category in category_avg_map.keys():
            print(category)
        """

    def getWeightFromMovieWithDistance(self, weightlist:WeightList)->WeightList:
        """
        위치, 유사도 테이블을 받아서 평균 거리와 유사도를 반환하는 함수

        :weightlist: (WeightList) 각 카테고리에 여러개의 (1~. 보통 2 이상) 위치, 유사도 값들이 있는 WeightList

        return (WeightList) 카테고리당 위치,유사도 쌍이 한개씩 들어있는 평균 유사도 맵
        """

        result_weightlist:WeightList = {}

        #모든 카테고리에 대해 반복
        for category in weightlist.keys():
            similarity_list:SimilarityList = weightlist.get(category,[(0,0)])



            sum_of_similarity:float = 0
            sum_of_distance:float = 0

            avg_of_similarity:float = 0
            avg_of_distance:float = 0

            #유사도 튜플의 모든 요소에 대해 반복
            for similarity in similarity_list:
                sum_of_similarity = sum_of_similarity + similarity[1]
                sum_of_distance = sum_of_distance + similarity[0]

            #모든 유사도 튜플의 합에 대한 평균 계산
            avg_of_similarity = sum_of_similarity / len(similarity_list)
            avg_of_distance = sum_of_distance / len(similarity_list)


            if result_weightlist.get(category) == None:
                result_weightlist[category] = []
            result_weightlist[category].append((avg_of_distance, avg_of_similarity))
        
        return result_weightlist








SimilarityList = list[tuple[float, float]]