import os
import math
import time

from multiprocessing import Pool
#from functools import reduce

import numpy as np

from similar.data.formula import FormulaCalculator
from similar.file.filereader import FileReader
#from similar.file.file import File
#from similar.csv.csv import CSV
#from similar.csv.csv import CSVList

from similar.enum.CSVFormat import CSVFormat
#from similar.data.color import COLOR

from similar.data.weight import WeightList
from similar.data.weight import WeightNPList
from similar.data.weight import MovieWeightList
from similar.data.weight import MovieWeightNPList
from similar.data.movie import MovieList
from similar.data.movie import ScoredMovieList


class WeightCalculator:

    filepath:str
    format:CSVFormat
    filereader:FileReader = FileReader()
    movie_weight_map:MovieWeightList

    category_index:list[str]

    title_list:list[str]
    title_dict:dict[str, int]
    distance_list:np.ndarray
    weight_list:np.ndarray

    def __init__(self):
        self.initial = 1

        
    def getCategoryNumPyArrayIndex(self, category_filepath:str)->list[str]:
        with open(category_filepath, "r", encoding="utf-8") as file:
            return file.read().split(",")

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
    
    def readAllMovieWeightNPList(self, reviewpath:str, movielist:MovieList, format:CSVFormat)->tuple[MovieList ,dict[str, int], np.ndarray, np.ndarray]:
        
        self.filepath = reviewpath
        self.format = format


        _N = len(movielist)
        _C = len(self.category_index)

        _movie_title_list:list[str] = ["" for _ in range(_N)]
        _movie_title_dict:dict[str, int] = {}

        _movie_distance_list:np.ndarray = np.zeros((_N, _C), dtype=np.float64)
        _movie_weight_list:np.ndarray = np.zeros((_N, _C), dtype=np.float64)

        with Pool(os.cpu_count()) as pool:
            results = pool.map(self.getWeightNpFromMovieElement, movielist)

        for i, result_dict in enumerate(results):
            k, v = next(iter(result_dict.items()))
            # 여기서 k, v는 self.getWeightNpFromMovieElement의 반환값이 영화:유사도 표이므로 k는 영화 이름, v는 유사도 표가 된다

            _movie_title_list[i] = k # 인덱스 마다 영화 이름을 담는 배열
            _movie_title_dict[k] = i # 영화 목록 (인덱스)로 영화 제목을 찾기 위한 검색용 테이블
            _movie_distance_list[i] = v[0] # 인덱스로 실제 영화가 배열의 몇번 인덱스에 있는지 찾기 위한 배열
            _movie_weight_list[i] = v[1] # 인덱스로 실제 영화의 유사도 맵을 찾는 배열

        self.title_list = _movie_title_list
        self.title_dict = _movie_title_dict
        self.distance_list = _movie_distance_list
        self.weight_list = _movie_weight_list

        return _movie_title_list, _movie_title_dict, _movie_distance_list, _movie_weight_list

        pass
    
    # def getWeightBetweenMovies(self)->WeightList:
    #     result:WeightList = {}

    #     return result

    def compareAllMovieWeightNPList(self, avg_distance:np.ndarray, avg_weight:np.ndarray, mvlist_param:MovieList, mvlist_review:MovieList)->np.ndarray:

        

        max_distance:float = 10.0
        max:float = 2.0
        min:float = 0.2

        #distance_multiplier:np.ndarray = ((max-min)/2)*np.cos(np.abs(self.distance_list - avg_distance)*(np.pi/max_distance))+((max+min)/2)
        distance_multiplier:np.ndarray = ((max-min)/2)*np.cos(np.clip(np.abs(self.distance_list - avg_distance), a_min=None, a_max=10.0)*(np.pi/max_distance))+((max+min)/2)
        similarity_multiplier:np.ndarray = (-2/np.pi)*np.atan((2*np.abs(self.weight_list - avg_weight))-2)+1

        result_array:np.ndarray = ((avg_weight * distance_multiplier) * similarity_multiplier).sum(axis=1)

        return result_array

        pass
    
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

        combined_weightlist:WeightList = self.getAverageWeight(weightlist)

        start_time = time.perf_counter()

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

                    if (combined_weightlist.get(category) == None) or (target_movie_weightlist.get(category) == None):
                        continue

                    distance:float = combined_weightlist[category][0][0]
                    similarity:float = combined_weightlist[category][0][1]

                    target_distance:float = target_movie_weightlist[category][0][0]
                    target_similarity:float = target_movie_weightlist[category][0][1]

                    distance_multiplier:float = FormulaCalculator().getWeightFromGapBetweenDistance(abs(distance - target_distance), 10, 2, 0.2)
                    similarity_multiplier:float = FormulaCalculator().getWeightFromGapBetweenWeight(abs(similarity - target_similarity))

                    score = score + (similarity * distance_multiplier * similarity_multiplier)

                    
                scorelist[score] = review

                #print(f"영화 {review} 비교 완료 ({index}/{len(mvlist_review)})")
                # print(f"비교 경과 시간 {time.time() - start_time}")
        
        print(f"elapse time : {(time.perf_counter() - start_time):.9f}")

        return scorelist
    

    def getAverageWeight(self, weightlist:WeightList)->WeightList:

        result:WeightList = {}

        if weightlist == None:
            result.append([(0,0)])
            return result
        
        for category in weightlist:
            result[category] = []
            result[category].append((sum(item[0] for item in weightlist[category])/len(weightlist[category]),(sum(item[1] for item in weightlist[category])/len(weightlist[category]))))

        return result
    
    def getWeightNpFromMovieList(self, reviewpath:str, mvlist_param:MovieList, format:CSVFormat)->tuple[np.ndarray,np.ndarray]:
        """
        :return: avg_distance, avg_weight
        """

        _avg_distance:np.ndarray = np.zeros(len(self.category_index))
        _avg_weight:np.ndarray = np.zeros(len(self.category_index))

        indices:np.ndarray = np.array([self.title_dict[movie] for movie in mvlist_param]) # 사용자가 DB에 없는 영화를 요청하면 오류가 발생하기 때문에 아래로 대체

        # valid_indices_list:list[int] = [self.title_dict[movie] for movie in mvlist_param if movie in self.title_dict]
        # indices:np.ndarray = np.array(valid_indices_list)

        selected_distances:np.ndarray = self.distance_list[indices]
        selected_weights:np.ndarray = self.weight_list[indices]

        _sum_of_distance = selected_distances.sum(axis=0)
        _sum_of_weight = selected_weights.sum(axis=0)

        # for movie in mvlist_param:
        #     _avg_distance = _avg_distance + self.distance_list[self.title_list.index(movie)]
        #     _avg_weight = _avg_weight + self.weight_list[self.title_list.index(movie)]
        
        # _avg_distance = _avg_distance / len(mvlist_param)
        # _avg_weight = _avg_weight / len(mvlist_param)

        _avg_distance = _sum_of_distance / len(mvlist_param)
        _avg_weight = _sum_of_weight / len(mvlist_param)
        


        return _avg_distance, _avg_weight
    
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
            if movie in self.movie_weight_map:
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

    def getWeightNpFromMovieElement(self, args)->WeightNPList:
        """
        NumPy를 이용한 병렬 연산을 위해 NumPy 벡터로 반환하는 함수
        """
        csv_table:list[str] = self.filereader.readCSVTables(self.filepath+args+"_categorized_words.csv", self.format)

        df2 = csv_table[1] # csv 테이블은 유사도 테이블과 사전 연산된 유사도 점수표로 이루어져 있다. 필요한 테이블은 유사도 점수표이므로 1번 인덱스를 가져온다
        data_list = df2.split("\n")

        read_data_index_map:np.ndarray = np.zeros(len(self.category_index)) # 카테고리와 같은 크기의 배열
        read_data_freq_map:np.ndarray = np.zeros(len(self.category_index)) # 각 카테고리와 연결된 등장 빈도 배열
        read_data_similarity_map:np.ndarray = np.zeros(len(self.category_index)) # 각 카테고리와 연결된 유사도 배열

        # 위 데이터는 세개로 나뉘어져 있지만 실제로는 3 by len(index) 크기의 행렬으로 볼 수 있다

        sum_of_mrpheme:float = 0 # 모든 형태소 등장 횟수. 각 형태소가 어느 정도 비율로 나오는지 계산하는 목적으로 사용된다

        for i in range(1, len(data_list)-1):
            data_list_split = data_list[i].split(",") # 여기서 인덱스 0이 형태소의 종류, 인덱스 1이 형태소의 등장 횟수
            sum_of_mrpheme += float(data_list_split[1])
            try:
                read_data_freq_map[self.category_index.index(data_list_split[0])] = float(data_list_split[1]) # 빈도 배열. 현재 작업중인 형태소의 빈도값을 해당 형태소가 해당하는 배열의 index에 넣는다
                read_data_similarity_map[self.category_index.index(data_list_split[0])] = float(data_list_split[2]) # 유사도 배열. 현재 작업중인 형태소의 유사도 값을 넣는다
                read_data_index_map[self.category_index.index(data_list_split[0])] = i - 1 # 인덱스 배열. 미리 지정된 형태소의 인덱스 위치에 현재 작업한 데이터의 인덱스를 넣는다
            except:
                continue

        #Count의 모든 값은 결국 모든 형태소의 갯수와 같다
        morphemeCNT:float = sum_of_mrpheme
        #read_data_map_keys = read_data_map.keys() # 필요 없을듯
        #read_data_map_length = len(read_data_map_keys) #얘는 아마 len(data_list)-2랑 같을듯?

        read_data_map_length = len(data_list)-2

        if(morphemeCNT == 0):
            # 리뷰에서 추출한 형태소 데이터가 없는 경우
            # 0으로 나눌 수 없기 때문에 예외처리한다
            morph_cate_ratio:np.ndarray = read_data_freq_map
        else:
            morph_cate_ratio:np.ndarray = read_data_freq_map / morphemeCNT # 전체 빈도 배열을 최종 형태소 갯수로 나누어서 저장한다. 이렇게 하면 이 ratio 배열은 각 형태소의 등장빈도가 된다
        percentage_multiplier:np.ndarray = morph_cate_ratio * read_data_map_length # 형태소 등장 비율을 형태소 종류의 갯수만큼 곱한다. 이렇게 하면 형태소의 종류가 너무나도 많을 때 주요 키워드의 의미가 사라지는 문제를 해결할 수 있다
        similarity_final_multiplier:np.ndarray = read_data_similarity_map * percentage_multiplier
        """
        최종 유사도는 사전 계산된 유사도에서 형태소의 종류와 갯수에 따른 보정값의 곱이 된다.
        이렇게 하면 사전 계산된 유사도가 비슷하더라도, 형태소가 얼마나 더 빈번하게 등장하는지에 따라
        어떤 형태소가 이 영화에서 더 중요하게 여겨지는지 알 수 있다.
        """

        result:list[np.ndarray] = [read_data_index_map, similarity_final_multiplier]

        # for category in read_data_map_keys:
            #카테고리에 포함되는 형태소 갯수를 의미한다.
            # category_avg:float = read_data_map[category][0][1] # read_data_similarity_map
            # category_cnt:float = read_data_map[category][0][0] # read_data_freq_map

            # morph_cate_ratio:float = category_cnt / morphemeCNT


            # percentage_multiplier:float = morph_cate_ratio * read_data_map_length
            # similarity_final_multiplier:float = category_avg * percentage_multiplier


            # if output_data_map.get(category) == None:
            #     output_data_map[category] = []
            # output_data_map[category].append((category_index, similarity_final_multiplier))
        return {args:result}

        pass
    
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