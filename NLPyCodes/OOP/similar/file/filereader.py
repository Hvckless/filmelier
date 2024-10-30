import os
from io import StringIO

import pandas as pd

from similar.data.movie import MovieList
#from similar.data.dataframe import DataFrameList
from similar.csv.csv import CSV
from similar.csv.csv import CSVList
from similar.enum.CSVFormat import CSVFormat

class FileReader:
    def __init__(self):
        self.initial = 1

    def getMovieListFromReview(self, filepath:str)->MovieList:
        movielist:MovieList = []

        for filename in os.listdir(filepath):
            movielist.append(filename.split("_categorized_words.csv")[0])

        return movielist
    

    def readCSVTables(self, filepath:str, format:CSVFormat)->list[str]:
        """
        CSV 테이블 리스트를 반환하는함수.
        :return: 테이블 리스트는 최소 1개에서 여러개(2개 이상)일 수 있다.
        """

        tables:list[str] = []

        if format == CSVFormat.V1:
            with open(filepath, 'r', encoding="utf-8") as file:
                tables = file.read().split("\n\n")
            
        return tables