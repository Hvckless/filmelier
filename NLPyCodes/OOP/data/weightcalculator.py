from file.filehandler import FileHandler
from file.file import File
from csv.csv import CSV

from enum.CSVFormat import CSVFormat

from data.weight import WeightList
from data.movie import MovieList

class WeightCalculator:
    def __init__(self):
        self.initial = 1

    
    def getWeightBetweenMovies(self)->WeightList:
        result:WeightList = {}

        return result
    

    def getWeightFromMovieList(self, reviewpath:str, mvlist_param:MovieList)->WeightList:
        """
        영화 목록에서 가중치를 가져오는 함수
        :reviewpath: 리뷰 파일이 실제로 있는 위치
        :mvlist_param: 파라메터에서 가져온 (MovieList)타입 데이터
        """
        result:WeightList = {}

        for movie_name in mvlist_param:
            file = File()

            file.setFilepath(reviewpath+movie_name+"_categorized_words.csv")

            csv_data:CSV = file.readFileAsCSV(file.getFilepath(), CSVFormat.V1)


        return result