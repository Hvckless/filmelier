import time
import math

import os

from multiprocessing import Pool

from similar.file.filereader import FileReader

from similar.data.movie import MovieList

from similar.data.weight import WeightList
from similar.csv.csv import CSVList
from similar.csv.csv import CSVFormat

class Main:

    reviewFolderpath:str = "../../csvfile/"
    format:CSVFormat = CSVFormat.V1

    def __init__(self):
        if __name__ == "__main__":
            self.initial = 1

            filereader:FileReader = FileReader()
    
            hello_movie_list:MovieList = filereader.getMovieListFromReview(self.reviewFolderpath)


            start_time = time.time()
            
            with Pool(os.cpu_count()) as pool:
                results = pool.map(self.testwork, hello_movie_list)

            #print(len(results))
            print(f"elapsed time : {(time.time() - start_time)}")

    def testwork(self, arg):
        target_movie_weightlist:WeightList = self.getWeightFromMovieElement(self.reviewFolderpath+arg+"_categorized_words.csv", self.format, {})
        return target_movie_weightlist
    
    
    def getWeightFromMovieElement(self, filepath:str, format:CSVFormat, originalWeightList:WeightList)->WeightList:
        """
        파일에서 실제 가중치 목록(WeightList)을 불러와 기존 가중치 목록과 합치는 함수.

        :filepath: (str) 파일 경로
        :format: (CSVFormat) 파일 구조의 버전
        :originalWeightList: (WeightList) 기존의 WeightList가 없다면 {}으로 설정.

        return (WeightList) 결과물 가중치
        """
        csv_table:CSVList = FileReader().readCSVTables(filepath, format)

        #df1 = csv_table[0].getDataFrame()
        df2 = csv_table[1].getDataFrame()

        #category_avg_map:dict[str,float] = {}
        weightlist:WeightList = originalWeightList

        # df2를 카테고리별로 그룹화하여 평균과 카운트 계산
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

        for category in categories_list:
            summary_of_category_counts += category_count_map[category]


        #Count의 모든 값은 결국 모든 형태소의 갯수와 같다
        morphemeCNT:int = summary_of_category_counts
        count_amount:int = len(categories_list)

        for category in categories_list:

            category_avg = category_avg_map[category]
            category_cnt = category_count_map[category]

            category_index = categories_list.index(category)

            morph_cate_ratio:float = category_cnt / morphemeCNT


            percentage_multiplier:float = morph_cate_ratio * count_amount
            similarity_final_multiplier:float = category_avg * percentage_multiplier

            category_index:int = category_index

            if weightlist.get(category) == None:
                weightlist[category] = []

            weightlist[category].append((category_index, similarity_final_multiplier))

        return weightlist










#start_time = time.time()



app = Main()


#print(f"elapsed time : {(time.time() - start_time)}")