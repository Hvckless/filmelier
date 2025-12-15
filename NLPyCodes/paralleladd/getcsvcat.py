from multiprocessing import Pool
import os

class Main:

    reviewFolderpath:str
    movielist:list[str]

    def setReviewFolderpath(self, filepath:str)->None:
        self.reviewFolderpath = filepath
    def getReviewFolderpath(self)->str:
        return self.reviewFolderpath
    def readCSVTables(self, filepath)->list[str]:
        tables:list[str] = []

        with open(filepath, 'r', encoding="utf-8") as file:
            tables = file.read().split("\n\n")

        return tables

    def getMovieListFromFolder(self,filepath:str)->list[str]:
        movielist:list[str] = []

        for filename in os.listdir(filepath):
            movielist.append(filename.split("_categorized_words.csv")[0])

        return movielist
    
    def getCatListFromCSV(self, args)->list[str]:

        allcats:list[str] = []

        csv_table:list[str] =self.readCSVTables(self.reviewFolderpath+args+"_categorized_words.csv")

        df2 = csv_table[1]
        data_list = df2.split("\n")

        for i in range(1, len(data_list)-1):
            data_list_split = data_list[i].split(",")
            allcats.append(data_list_split[0])

        return allcats
    
    def readAllMovieWeightList(self, movielist:list[str]):

        somearray = set()

        with Pool(os.cpu_count()) as pool:
            results = pool.map(self.getCatListFromCSV, movielist)

        for result in results:
            somearray.update(result)
            # for k in result:
            #     if k not in somearray:
            #         somearray.append(k)
            # if result not in somearray:
            #     somearray.append(result)

        category_list = list(somearray)

        with open("category_list.txt", "w", encoding="utf-8") as file:
            for cat in category_list:
                file.write(cat+",")

    

if __name__ == "__main__":

    app = Main()

    app.setReviewFolderpath("../../csvfile/")
    app.movielist = app.getMovieListFromFolder(app.getReviewFolderpath())

    app.readAllMovieWeightList(app.movielist)