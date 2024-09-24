from os import error
import sys

from similar.data.movie import MovieList

class ParameterHandler:


    def __init__(self):
        self.initial = 1


    def getListFromParameter(self)->MovieList:
        movielist:MovieList = []
        try:
            for arg in sys.argv[1][1:len(sys.argv[1])-1].split(","):
               movielist.append(arg.replace("*", " "))
        except:
            print(error)
        finally:
            return movielist