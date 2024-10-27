import os
import math
import time

from multiprocessing import Pool
#from functools import reduce

import numpy as np

from similar.data.formula import FormulaCalculator
from similar.file.filereader import FileReader
from similar.file.file import File
from similar.csv.csv import CSV
from similar.csv.csv import CSVList

from similar.enum.CSVFormat import CSVFormat
from similar.data.color import COLOR

from similar.data.weight import WeightList
from similar.data.weight import MovieWeightList
from similar.data.movie import MovieList
from similar.data.movie import ScoredMovieList


class WeightCalculator:

    filepath:str
    format:CSVFormat
    filereader:FileReader = FileReader()
    movie_weight_map:MovieWeightList

    def __init__(self):
        self.initial = 1

        


    def readAllMovieWeightList(self, reviewpath:str, movielist:MovieList, format:CSVFormat)->MovieWeightList:
        some_movie_weightlist:MovieWeightList = {}
        
        self.filepath = reviewpath
        self.format = format

        with Pool(os.cpu_count()) as pool:
            results = pool.map(self.getWeightFromMovieElement, movielist)

        for result in results:
            for k, v in result.items():
                some_movie_weightlist[k] = v

        # some_movie_weightlist = reduce(lambda x, y: x | y, results)

        self.movie_weight_map = some_movie_weightlist

        return some_movie_weightlist
    
    def getWeightBetweenMovies(self)->WeightList:
        result:WeightList = {}

        return result
    
    def compareAllMovieWeightList(self, weightlist:WeightList, mvlist_param:MovieList, mvlist_review:MovieList)->ScoredMovieList:
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
        for index, review in enumerate(mvlist_review):
            #리뷰가 입력된 파라메터에 없다면 -> 비교 대상 영화
            if review not in mvlist_param:

                #start_time = time.time()

                score:float = 0

                target_movie_weightlist:WeightList = self.movie_weight_map[review]
                #target_movie_weightlist:WeightList = self.getWeightFromMovieElement(review)

                #print(f"파일 읽기 : {time.time() - start_time}")

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

                #print(f"영화 {review} 비교 완료 ({index}/{len(mvlist_review)})")
                # print(f"비교 경과 시간 {time.time() - start_time}")

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
        # weightpoints:WeightList = {}
        # for movie_name in mvlist_param:
        #     filepath:str = reviewpath+movie_name+"_categorized_words.csv"
            
        #     weightpoints = self.getWeightFromMovieElement(filepath, format, weightpoints)
        something_like_this:WeightList = {}
        for movie in mvlist_param:
            mvweight:WeightList = self.movie_weight_map[movie]
            for category in mvweight:
                
                # if category == "부도덕":
                #     print(movie)
                #     print(self.movie_weight_map[movie][category][0][0])
                #print(self.movie_weight_map[movie][category][0][0] + self.movie_weight_map[movie][category][0][1])
                mvweight_index = mvweight[category][0][0]
                mvweight_weight = mvweight[category][0][1]

                if something_like_this.get(category) == None:
                    something_like_this[category] = []
                something_like_this[category].append((mvweight_index, mvweight_weight))
            #print(movie)



            # print(self.movie_weight_map[movie])

        



        # with Pool(os.cpu_count()) as pool:
        #     results = pool.map(self.getWeightFromMovieElement, mvlist_param)

        # result_dict:dict = {}
        # for result in results:
        #     for k, v in result.items():
        #         result_dict[k] = v

        # print(len(results))



        # some:dict = {}
        # for movie in mvlist_param:
        #     self.getWeightFromMovieElement(movie)


        # for movie in mvlist_param:
        #     _dict:dict = self.getWeightFromMovieElement(movie)
        #     for key in _dict:
        #         some[key] = _dict[key]

        # print(len(some))

        
        #print(some['마션'])
        
        weightpointsV2:WeightList = something_like_this
        # weightpointsV2:WeightList = self.getWeightFromMovieWithDistance(weightpoints)

        return weightpointsV2
        #return weightpointsV2
    
    def getWeightFromMovieElement(self, args)->dict[str, WeightList]:
        """
        파일에서 실제 가중치 목록(WeightList)을 불러와 기존 가중치 목록과 합치는 함수.

        :args: 영화 이름

        return (WeightList) 결과물 가중치
        """
        csv_table:list[str] = self.filereader.readCSVTables(self.filepath+args+"_categorized_words.csv", self.format)

        # df1 = csv_table[0]
        # one_data_list = df1.split("\n")

        # tot_cnt = 0
        # for i in range(1, len(one_data_list)-1):
        #     one_data_list_split = one_data_list[i].split(",")

        #     if(one_data_list_split[1] == "만화"):
        #         tot_cnt += int(one_data_list_split[3])
        #         print(one_data_list_split[0])

        # print(tot_cnt)














        df2 = csv_table[1]
        data_list = df2.split("\n")

        read_data_map:WeightList = {}
        output_data_map:WeightList = {}


        sum_of_mrpheme:float = 0

        for i in range(1, len(data_list)-1):
            data_list_split = data_list[i].split(",")
            sum_of_mrpheme += float(data_list_split[1])
            try:
                read_data_map[data_list_split[0]] = [(float(data_list_split[1]),float(data_list_split[2]))]
            except:
                continue

        #Count의 모든 값은 결국 모든 형태소의 갯수와 같다
        morphemeCNT:float = sum_of_mrpheme
        read_data_map_keys = read_data_map.keys()
        read_data_map_length = len(read_data_map_keys)
        read_data_map_list = list(read_data_map_keys)

        # print(read_data_map_list)

        for category in read_data_map_keys:
            #카테고리에 포함되는 형태소 갯수를 의미한다.
            category_avg:float = read_data_map[category][0][1]
            category_cnt:float = read_data_map[category][0][0]

            morph_cate_ratio:float = category_cnt / morphemeCNT


            percentage_multiplier:float = morph_cate_ratio * read_data_map_length
            similarity_final_multiplier:float = category_avg * percentage_multiplier

            category_index:int = read_data_map_list.index(category)

            if output_data_map.get(category) == None:
                output_data_map[category] = []
            output_data_map[category].append((category_index, similarity_final_multiplier))
        return {args:output_data_map}

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