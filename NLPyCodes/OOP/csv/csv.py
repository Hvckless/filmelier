from pandas import DataFrame

class CSV:
    data:DataFrame
    def __init__(self):
        self.initial = 1

    def setDataFrame(self, data:DataFrame)->None:
        self.data = data
    def getDataFrame(self)->DataFrame:
        return self.data
    
CSVList = list[CSV]