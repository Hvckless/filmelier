from pandas import DataFrame

from similar.file.file import File
from similar.enum.CSVFormat import CSVFormat



class CSV(File):
    data:DataFrame
    def __init__(self):
        self.initial = 1

    def setDataFrame(self, data:DataFrame)->None:
        self.data = data
    def getDataFrame(self)->DataFrame:
        return self.data
    


CSVList = list[CSV]