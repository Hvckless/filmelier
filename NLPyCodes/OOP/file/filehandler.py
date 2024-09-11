import os
from io import StringIO


import pandas as pd



from data.movie import MovieList

from .file import File
from .file import FileList
from data.dataframe import DataFrameList

from csv.csv import CSV
from csv.csv import CSVList

from enum.CSVFormat import CSVFormat


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
    
    def readFileFromIO(self, data:StringIO)->None:
        print("A")
    




    def readCSV(self, filepath:str, format:CSVFormat)->CSV:

        csv_data:CSV = CSV()

        if format == CSVFormat.V1:
            tables:DataFrameList = []
            content:str = "undefined"

            with open(filepath, 'r', encoding="utf-8") as file:
                content = file.read()

            for table in content.split("\n\n"):
                tables.append(pd.read_csv(StringIO()))
            
        return CSV()
    
    def readCSVList(self, filepath:str, format:CSVFormat)->CSVList:
        csv_tables:CSVList = []

        if format == CSVFormat.V1:
            content:str

            with open(filepath, 'r', encoding="utf-8") as file:
                content = file.read()

            for table_content in content.split("\n\n"):
                csv:CSV = CSV()
                csv.setDataFrame(pd.read_csv(StringIO(table_content)))
                csv_tables.append(csv)

        return csv_tables

    

    def splitFile(self)->File:
        return self.file