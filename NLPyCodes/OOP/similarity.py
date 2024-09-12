# import start

from similar.parameter.parameterhandler import ParameterHandler
from similar.file.filereader import FileReader

from similar.data.weightcalculator import WeightCalculator

from similar.data.movie import MovieList
from similar.data.weight import WeightList

# import end




class Main:

    reviewFolderpath:str

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
        return WeightCalculator().getWeightFromMovieList(self.reviewFolderpath, mvlist_param)

    
    def getWeightListBetweenMovies(self)->WeightList:
        return WeightCalculator().getWeightBetweenMovies()

    

    def setReviewFolderpath(self, filepath:str)->None:
        self.reviewFolderpath = filepath
    def getReviewFolderpath(self)->str:
        return self.reviewFolderpath

















app = Main()


app.setReviewFolderpath("../../csvfile/")


hello:MovieList = app.getMovieListFromParameter() #영화 파라메터 목록
bye:MovieList = app.getMovieListFromReviews() #영화 파일 목록