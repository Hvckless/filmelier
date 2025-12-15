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
               movielist.append(arg.replace("'", "").replace("*", " "))
        except:
            print(error)
        finally:
            return movielist
        
    def getListFromInput(self, input_string:str)->MovieList:
        movielist:MovieList = []
        try:
            for arg in input_string[1:len(input_string)-1].split(","):
               movielist.append(arg.replace("'", "").replace("*", " "))
        except:
            print(error)
        finally:
            return movielist