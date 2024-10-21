import time

from similar.file.filereader import FileReader

from similar.data.movie import MovieList

from similar.csv.csv import CSVList
from similar.csv.csv import CSVFormat



class Main:

    reviewFolderpath:str = "../../csvfile/"
    format:CSVFormat = CSVFormat.V1

    def __init__(self):
        self.initial = 1

        print("HELLO WORLD!")

        filereader:FileReader = FileReader()

        hello_movie_list:MovieList = filereader.getMovieListFromReview(self.reviewFolderpath)

        for movie_name in hello_movie_list:
            filepath:str = self.reviewFolderpath+movie_name+"_categorized_words.csv"

            csv_tables:CSVList = filereader.readCSVTables(filepath, self.format)

            df1 = csv_tables[0].getDataFrame()
            df2 = csv_tables[1].getDataFrame()

            print(f"영화 {movie_name} 단어 총량 {(df1['Frequency'].sum())}")
            print(f"영화 {movie_name} 카테고리 갯수 총량 {df2['Count'].sum()}")

        print(hello_movie_list)



start_time = time.time()

app = Main()

print(f"elapsed time : {(time.time() - start_time)}")