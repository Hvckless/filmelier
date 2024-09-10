import os

from data.movie import MovieList

from .file import File
from .file import FileList


class FileHandler:
    file:File
    def __init__(self):
        self.initial = 1


    """def createFile(self)->File:
        return File()
    """


    def getListFromReviews(self, filepath:str)->MovieList:
        movielist:MovieList = []
        for filename in os.listdir(filepath):
            movielist.append(filename.split("_categorized_words.csv")[0])

        return movielist


    def readFile(self, filepath:str)->File:

        filelist:File

        for filename in os.listdir(filepath):
            print(filename)


            

        return self.file
    

    def splitFile(self)->File:
        return self.file