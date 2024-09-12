from .csv import CSV

class CSVHandler:
    def __init__(self):
        self.initial = 1

    def readCSV(self, filepath:str)->CSV:
        return CSV()