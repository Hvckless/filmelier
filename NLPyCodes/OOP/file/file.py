from .filehandler import FileHandler
from csv.csv import CSV

from enum.CSVFormat import CSVFormat

class File:
    filepath:str


    def __init__(self):
        self.initial = 1


    def getFilepath(self)->str:
        return self.filepath
    
    def setFilepath(self, filepath:str)->None:
        self.filepath = filepath




    def readFileAsCSV(self, filepath:str, format:CSVFormat)->CSV:
        return FileHandler().readCSV(filepath, format)


FileList = list[File]