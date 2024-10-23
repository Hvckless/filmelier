from io import StringIO
import os
import time

from concurrent.futures import ThreadPoolExecutor
import pandas as pd

dictionaryLegend = dict[str, list[tuple[int, float]]]

class FuckingPandas:
    helloworld:dict[str, pd.DataFrame] = {}

    kinggodworld:dict[str, dictionaryLegend] = {}

    def threadExecutor(self):
        filepath:str = "../../csvfile/"

        movielist = [filename.split("_categorized_words.csv")[0] 
                     for filename in os.listdir(filepath)]
        
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=6) as executor:
            results = executor.map(
                lambda movie: self.use_fs(movie, filepath), movielist
            )

        somelist = []

        for result in results:
            somelist.append(result)

        print(len(somelist))
        print(f"elapsed time: {time.time() - start_time}")

    def use_fs(self, moviename, filepath):
        self.initial = 1

        with open(filepath+moviename+"_categorized_words.csv", 'r', encoding="utf-8") as file:

            data_list = file.read().split("\n\n")[1].split("\n")

            somedict:dictionaryLegend = {}

            for i in range(1, len(data_list)):
                data_list_split = data_list[i].split(",")

                try:
                    somedict[data_list_split[0]] = [(int(data_list_split[1]), float(data_list_split[2]))]
                except:
                    continue

            return {moviename:somedict}


        # movielist = []


        # movielist = [filename.split("_categorized_words.csv")[0] 
        #              for filename in os.listdir(filepath)]

        # for movie in movielist:
        #     with open(filepath+movie+"_categorized_words.csv", 'r', encoding="utf-8") as file:

        #         data_list = file.read().split("\n\n")[1].split("\n")
                
        #         somedict:dictionaryLegend = {}
        #         for i in range(1, len(data_list)):
        #             data_list_split = data_list[i].split(",")
                    
        #             try:
        #                 somedict[data_list_split[0]] = [(int(data_list_split[1]), float(data_list_split[2]))]
        #             except:
        #                 continue
        #         self.kinggodworld[movie] = somedict
    
    def use_pd(self):
        self.initial = 1

        filepath:str = "../../csvfile/"
        movielist:list[str] = []

        start_time = time.time()

        for filename in os.listdir(filepath):
            movielist.append(filename.split("_categorized_words.csv")[0])

        for movie in movielist:
            df2 = self.readCSVTables(filepath+movie+"_categorized_words.csv")[1]

            category_stats = df2.groupby("Category").agg({
                "average": "mean",
                "Count": "sum"
            }).reset_index()

            

            # 카테고리 통계를 dictionary로 변환
            category_avg_map = dict(zip(category_stats["Category"], category_stats["average"]))
            category_stats_sorted = category_stats.sort_values(by="Count", ascending=False)
            category_count_map = dict(zip(category_stats_sorted["Category"], category_stats_sorted["Count"]))

            categories_list = list(category_count_map.keys())

            summary_of_category_counts:int = 0

            self.helloworld[movie] = category_stats

        print(f"{self.helloworld.keys()}")
        print(f"elapsed time : {time.time()-start_time}")
        

    def readCSVTables(self, filepath:str)->list[pd.DataFrame]:
        """
        CSV 테이블 리스트를 반환하는함수.
        :return: 테이블 리스트는 최소 1개에서 여러개(2개 이상)일 수 있다.
        """
        tables:list[pd.DataFrame] = []

        with open(filepath, 'r', encoding="utf-8") as file:
            content:str = file.read()

        for table_content in content.split("\n\n"):
            dataframe:pd.DataFrame
            dataframe = pd.read_csv(StringIO(table_content))
            tables.append(dataframe)
        

        return tables


app = FuckingPandas()

app.threadExecutor()