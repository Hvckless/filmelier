class File:
    filepath:str


    def __init__(self):
        self.initial = 1


    def getFilepath(self)->str:
        return self.filepath
    
    def setFilepath(self, filepath:str)->None:
        self.filepath = filepath



FileList = list[File]