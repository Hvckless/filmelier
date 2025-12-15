# import start

import json
import time

import sys
import io

from typing import Any

import numpy as np

from similar.parameter.parameterhandler import ParameterHandler
from similar.file.filereader import FileReader

from similar.data.weightcalculator import WeightCalculator

from similar.data.weight import WeightList
from similar.data.weight import MovieWeightList
from similar.data.movie import MovieList
from similar.data.movie import ScoredMovieList
from similar.data.movie import SortedScoreMovieList

from similar.csv.csv import CSVFormat

# import end

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdout.flush()

# similarity changes

class Main:

    reviewFolderpath:str
    format:CSVFormat = CSVFormat.V1
    weightcalculator:WeightCalculator = WeightCalculator()

    def __init__(self):
        self.initial = 1

    def getMovieListFromParameter(self) -> MovieList:
        return ParameterHandler().getListFromParameter()
    
    def getMovieListFromInput(self, input_string:str)->MovieList:
        return ParameterHandler().getListFromInput(input_string)
    
    def getMovieListFromReviews(self) -> MovieList:
        return FileReader().getMovieListFromReview(self.reviewFolderpath)
    

    def readAllMovieWeightList(self, mvlist:MovieList)->MovieWeightList:
        return self.weightcalculator.readAllMovieWeightList(self.reviewFolderpath, mvlist, self.format)
    
    def readAllMovieWeightNPList(self, mvlist:MovieList)->tuple[MovieList, dict[str, int], np.ndarray, np.ndarray]:
        return self.weightcalculator.readAllMovieWeightNPList(self.reviewFolderpath, mvlist, self.format)

    def getWeightNpFromMovieList(self, mvlist_param:MovieList)->tuple[np.ndarray,np.ndarray]:
        return self.weightcalculator.getWeightNpFromMovieList(self.reviewFolderpath, mvlist_param, self.format)

    def getWeightListFromMovieList(self, mvlist_param:MovieList)->WeightList:
        """
        파라메터로 받은 MovieList에서 추출한 영화 목록의 평균 가중치를 반환하는 함수

        :mvlist_param: 파라메터에서 가져온 MovieList 객체

        return 평균 가중치 WeightList 객체
        """
        return self.weightcalculator.getWeightFromMovieList(self.reviewFolderpath, mvlist_param, self.format)
    
    def getWeightNPListBetweenMovies(self, mvlist_param:MovieList, mvlist_review:MovieList, avg_distance:np.ndarray, avg_weight:np.ndarray)->np.ndarray:
        return self.weightcalculator.compareAllMovieWeightNPList(avg_distance, avg_weight, mvlist_param, mvlist_review)
    def getWeightListBetweenMovies(self, mvlist_param:MovieList, mvlist_review:MovieList, avg_weightlist:WeightList)->ScoredMovieList:
        """
        원본 Similarity 코드의 compareAllMovies참조
        산출한 WeightList와 모든 영화의 WeightList를 비교해서 최종 Score 산출
        """
        return self.weightcalculator.compareAllMovieWeightList(avg_weightlist, mvlist_param, mvlist_review)
    
    def findHighestNMovies(self, scored_array:np.ndarray, mvlist_param:list[str], n:int)->ScoredMovieList:



        pass

    def makeResult(self):
        while True:
            movielist_string:str = input()

            if movielist_string == "end":
                break

            #mvlist_param: MovieList = app.getMovieListFromParameter()  # 영화 파라메터 목록

            mvlist_param: MovieList = self.getMovieListFromInput(movielist_string)  # 영화 파라메터 목록

            #start_time = time.time()


            # score_dictionary: ScoredMovieList = self.getWeightListBetweenMovies(
            #     mvlist_param,
            #     mvlist_review,
            #     self.getWeightListFromMovieList(mvlist_param)
            # )

            

            valid_movie_list:MovieList = [movie for movie in mvlist_param if movie in self.weightcalculator.title_dict]

            if not valid_movie_list:
                print(json.dumps({}, ensure_ascii=False))
                continue

            # start_time = time.perf_counter()

            avg_distance, avg_weight = self.getWeightNpFromMovieList(valid_movie_list) # 선택한 영화들의 평균 유사도 / 거리값을 계산한다. 사용자가 좋아하는 영화들을 하나로 묶어 계산하는데 사용한다

            

            score_array: np.ndarray = self.getWeightNPListBetweenMovies(
                valid_movie_list,
                mvlist_review,
                avg_distance,
                avg_weight
            ) # 형태소별 가중치와 거리를 이용해 점수를 계산한다

            # print(f"elapse time : {(time.perf_counter() - start_time):.9f}")


            target_count = 10

            selected_indices = [self.weightcalculator.title_dict[movie] for movie in valid_movie_list]
            """
            파라메터에서 가져온 영화 목록을 title_dict에서 가져온다
            이를 통해 final_scores를 탐색할 때 파라메터에 입력한 영화의 점수를 0으로 만들어 추천하지 않도록 한다
            """

            final_scores = score_array.copy()
            final_scores[selected_indices] = 0

            top_indices = np.argsort(final_scores)[::-1][:target_count] # 배열의 처음부터 끝까지를 step -1로 배열한다. 그 중 처음부터 target_count까지를 얻는다.

            # print(top_indices)

            result: dict[float, str] = {}

            for idx in top_indices:
                if final_scores[idx] == 0:
                    break
                result[float(score_array[idx])] = self.weightcalculator.title_list[idx]

            print(json.dumps(result, ensure_ascii=False))
        """
        
        #self.findHighestNMovies(score_array, 10)

        # 점수로 정렬
        #sorted_dictionary: SortedScoreMovieList = dict(sorted(score_dictionary.items(), key=lambda item: item[0], reverse=True))

        # 상위 10개 항목만 추출
        #top_10 = {score: name for score, name in list(sorted_dictionary.items())[:10]}
        n = 10

        #sorted_list:np.ndarray = np.argsort(score_array)[len(score_array)-10:]
        sorted_list:np.ndarray = np.argsort(score_array)[::-1]
        print(score_array)
        print(sorted_list)

        sel_mv_list:np.ndarray = np.zeros(len(mvlist_param))
        for i, movie in enumerate(mvlist_param):
            sel_mv_list[i] = np.where(sorted_list == self.weightcalculator.title_dict[movie])[0].item()
            #sel_mv_list.append(sorted_list.index(self.weightcalculator.title_list.index(movie)))

        #print(sel_mv_list[::-1])

        for i in sel_mv_list[::-1]:
            if i < n:
                n += 1

        sorted_list = sorted_list[:n]

        #np.array(sel_mv_list)

        #self.weightcalculator.title_list.index()
        
        #print(self.weightcalculator.title_list[sorted_list[0]])

        result:dict[float,str] = {}

        for i in range(n):
            if i in sel_mv_list:
                continue
            else:
                #print(self.weightcalculator.title_list[sorted_list[i]] + " : " + str(score_array[sorted_list[i]]))
                result[float(score_array[sorted_list[i]])] = self.weightcalculator.title_list[sorted_list[i]]

        
        #print(result)
            #score_array[sorted_list[i]]

        #top_10 = self.findHighestNMovies(score_array, mvlist_param, 10)
        # 결과 출력
        print(json.dumps(result, ensure_ascii=False))

        self.makeResult()
        """

    

    def setReviewFolderpath(self, filepath:str)->None:
        self.reviewFolderpath = filepath
    def getReviewFolderpath(self)->str:
        return self.reviewFolderpath
    
    def setCSVFormat(self, format:CSVFormat)->None:
        self.format = format
    def getCSVFormat(self)->CSVFormat:
        return self.format
    

    def findKeyByValue(self, value:Any, object:dict)->Any:
        for key in object.keys():
            if object[key] == value:
                return key

















if __name__ == "__main__":

    try:
        app = Main()


        # 설정 시작

        app.setReviewFolderpath("../../csvfile/")
        app.setCSVFormat(CSVFormat.V1)

        # 설정 종료

        app.weightcalculator.category_index = app.weightcalculator.getCategoryNumPyArrayIndex("./category_list.txt")

        
        mvlist_review: MovieList = app.getMovieListFromReviews()    # 영화 파일 목록

        #hello_list:MovieWeightList = app.readAllMovieWeightList(mvlist_review)
        title_list, title_dict, distance_list, weight_list = app.readAllMovieWeightNPList(mvlist_review)

        avg_distance, avg_weight = app.weightcalculator.getWeightNpFromMovieList(app.getReviewFolderpath, ['마션'], CSVFormat.V1)

        app.makeResult()

    except Exception as e:
        print(f"파이썬 프로세스 에러 발생됨 : {e}", file=sys.stderr)
        print(json.dumps({}, ensure_ascii=False))

