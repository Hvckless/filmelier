# import start

from typing import Any

from similar.parameter.parameterhandler import ParameterHandler
from similar.file.filereader import FileReader

from similar.data.weightcalculator import WeightCalculator

from similar.data.weight import WeightList
from similar.data.movie import MovieList
from similar.data.movie import ScoredMovieList
from similar.data.movie import SortedScoreMovieList

from similar.csv.csv import CSVFormat

# import end


# similarity changes

class Main:

    reviewFolderpath:str
    format:CSVFormat = CSVFormat.V1

    def __init__(self):
        self.initial = 1

    def getMovieListFromParameter(self) -> MovieList:
        return ParameterHandler().getListFromParameter()
    
    def getMovieListFromReviews(self) -> MovieList:
        return FileReader().getMovieListFromReview(self.reviewFolderpath)


    def getWeightListFromMovieList(self, mvlist_param:MovieList)->WeightList:
        """
        파라메터로 받은 MovieList에서 추출한 영화 목록의 평균 가중치를 반환하는 함수
        :mvlist_param: 파라메터에서 가져온 MovieList 객체
        :return: 평균 가중치 WeightList 객체
        """
        return WeightCalculator().getWeightFromMovieList(self.reviewFolderpath, mvlist_param, self.format)
    
    
    def getWeightListBetweenMovies(self, mvlist_param:MovieList, mvlist_review:MovieList, avg_weightlist:WeightList)->ScoredMovieList:
        """
        원본 Similarity 코드의 compareAllMovies참조
        산출한 WeightList와 모든 영화의 WeightList를 비교해서 최종 Score 산출
        """
        return WeightCalculator().compareAllMovieWeightList(self.reviewFolderpath, avg_weightlist, mvlist_param, mvlist_review, self.format)

    

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



















app = Main()


# 설정 시작

app.setReviewFolderpath("../../csvfile/")
app.setCSVFormat(CSVFormat.V1)

# 설정 종료


mvlist_param:MovieList = app.getMovieListFromParameter() #영화 파라메터 목록
mvlist_review:MovieList = app.getMovieListFromReviews() #영화 파일 목록

score_dictionary:ScoredMovieList = app.getWeightListBetweenMovies(mvlist_param, mvlist_review, app.getWeightListFromMovieList(mvlist_param))
sorted_dictionary:SortedScoreMovieList = dict(sorted(score_dictionary.items(), key=lambda item: item[0], reverse=True))

print(sorted_dictionary)



#number = 0
#for movie_score in sorted_dictionary:
#    print(f"{number}위 : {sorted_dictionary[movie_score]} | 값 : {movie_score}")
#    number = number + 1