# import start

from parameter.parameterhandler import ParameterHandler
from file.filehandler import FileHandler


from data.movie import MovieList
from data.weight import WeightList

# import end




class Main:

    reviewFolderpath:str

    def __init__(self):
        self.initial = 1

    def getMovieListFromParameter(self) -> MovieList:
        return ParameterHandler().getListFromParameter()
    
    def getMovieListFromReviews(self) -> MovieList:
        return FileHandler().getListFromReviews(self.reviewFolderpath)


    def getWeightListFromMovieList(self):
        print("HELLO")

    
    def getWeightListBetweenMovies(self):
        print("HELLO")

    

    def setReviewFolderpath(self, filepath:str)->None:
        self.reviewFolderpath = filepath
    def getReviewFolderpath(self)->str:
        return self.reviewFolderpath

















app = Main()


app.setReviewFolderpath("../../csvfile")


hello:MovieList = app.getMovieListFromParameter()
bye:MovieList = app.getMovieListFromReviews()