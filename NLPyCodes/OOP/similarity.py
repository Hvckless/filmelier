# import start

import json
import time

from typing import Any

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


    def getWeightListFromMovieList(self, mvlist_param:MovieList)->WeightList:
        """
        파라메터로 받은 MovieList에서 추출한 영화 목록의 평균 가중치를 반환하는 함수

        :mvlist_param: 파라메터에서 가져온 MovieList 객체

        return 평균 가중치 WeightList 객체
        """
        return self.weightcalculator.getWeightFromMovieList(self.reviewFolderpath, mvlist_param, self.format)
    
    
    def getWeightListBetweenMovies(self, mvlist_param:MovieList, mvlist_review:MovieList, avg_weightlist:WeightList)->ScoredMovieList:
        """
        원본 Similarity 코드의 compareAllMovies참조
        산출한 WeightList와 모든 영화의 WeightList를 비교해서 최종 Score 산출
        """
        return self.weightcalculator.compareAllMovieWeightList(avg_weightlist, mvlist_param, mvlist_review)
    
    def makeResult(self):

        movielist_string:str = input()

        if movielist_string == "end":
            return

        #mvlist_param: MovieList = app.getMovieListFromParameter()  # 영화 파라메터 목록

        mvlist_param: MovieList = self.getMovieListFromInput(movielist_string)  # 영화 파라메터 목록

        start_time = time.time()


        score_dictionary: ScoredMovieList = self.getWeightListBetweenMovies(
            mvlist_param,
            mvlist_review,
            self.getWeightListFromMovieList(mvlist_param)
        )

        # 점수로 정렬
        sorted_dictionary: SortedScoreMovieList = dict(sorted(score_dictionary.items(), key=lambda item: item[0], reverse=True))

        # 상위 10개 항목만 추출
        top_10 = {score: name for score, name in list(sorted_dictionary.items())[:10]}

        # 결과 출력
        print(json.loads(json.dumps(top_10)))

        print(f"elapse time : {time.time() - start_time}")

        self.makeResult()

    

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
    

    app = Main()


    # 설정 시작

    app.setReviewFolderpath("../../csvfile/")
    app.setCSVFormat(CSVFormat.V1)

    # 설정 종료


    
    mvlist_review: MovieList = app.getMovieListFromReviews()    # 영화 파일 목록

    hello_list:MovieWeightList = app.readAllMovieWeightList(mvlist_review)


    app.makeResult()

    

