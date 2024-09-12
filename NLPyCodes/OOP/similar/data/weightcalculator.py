from similar.file.filereader import FileReader
from similar.file.file import File
from similar.csv.csv import CSV
from similar.csv.csv import CSVList

from similar.enum.CSVFormat import CSVFormat

from similar.data.weight import WeightList
from similar.data.movie import MovieList

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

        """
        TO-DO LIST

        1. 영화 목록 가져오기

        """

        for movie_name in mvlist_param:
            filepath:str = reviewpath+movie_name+"_categorized_words.csv"
            weightpoint:WeightList = {}
            weightpoint = self.getWeightFromMovieElement(filepath, CSVFormat.V1, weightpoint)


        return result
    
    def getWeightFromMovieElement(self, filepath:str, format:CSVFormat, originalWeightList:WeightList)->WeightList:
        csv_table:CSVList = FileReader().readCSVTables(filepath, format)

        df1 = csv_table[0].getDataFrame()
        df2 = csv_table[1].getDataFrame()

        category_avg_map:dict[str,float] = {}

        for category in df2["Category"]:
            #"Category"의 평균
            category_avg_map[category] = df1.loc[df1["Category"] == category].mean()

            percentage:int

            #Count의 모든 값은 결국 모든 형태소의 갯수와 같다
            morphemeCNT:int = df2["Count"].sum()
