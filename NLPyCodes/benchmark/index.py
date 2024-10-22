import time
import math

from threading import Thread
from multiprocessing import Process, Queue

from similar.file.filereader import FileReader

from similar.data.fuckingpandas import FuckingPandas
from similar.data.movie import MovieList

from similar.data.weight import WeightList
from similar.csv.csv import CSVList
from similar.csv.csv import CSVFormat



class Main:

    reviewFolderpath:str = "../../csvfile/"
    format:CSVFormat = CSVFormat.V1

    def __init__(self):
        self.initial = 1

        filereader:FileReader = FileReader()

        hello_movie_list:MovieList = filereader.getMovieListFromReview(self.reviewFolderpath)

        for movie_name in hello_movie_list:

            target_movie_weightlist:WeightList = self.getWeightFromMovieElement(self.reviewFolderpath+movie_name+"_categorized_words.csv", self.format, {})

            for category in target_movie_weightlist.keys():
                distance_multiplier:float = 0
                similarity_multiplier:float = 0

                target_distance:float = target_movie_weightlist[category][0][0]
                target_similarity:float = target_movie_weightlist[category][0][1]

                #print(f"추출 결과 : {target_distance} / {target_similarity}")

            # filepath:str = self.reviewFolderpath+movie_name+"_categorized_words.csv"

            # csv_tables:CSVList = filereader.readCSVTables(filepath, self.format)

            # df1 = csv_tables[0].getDataFrame()
            # df2 = csv_tables[1].getDataFrame()

            # print(f"영화 {movie_name} 단어 총량 {(df1['Frequency'].sum())}")
            # print(f"영화 {movie_name} 카테고리 갯수 총량 {df2['Count'].sum()}")

        print(hello_movie_list)
    
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
        


        #Count의 모든 값은 결국 모든 형태소의 갯수와 같다
        morphemeCNT:int = df2["Count"].sum()
        count_amount:int = df2.count().iloc[1]
        #morphemeCNT:int = 1

        #heros_of_the_storm = ['액션', '여행', '기대', '교육', '음악', '사랑', '우주', '드라마', '방송', '기쁨', '도시', '불안', '열정', '미술', '발견', '환경', '학교', '가족', '다큐멘터리', '경제', '전투', '꿈', '대화', '만화', '희망', '성장', '음식', '심리', '컴퓨터', '혼란', '후회', '철학', '인형', '가상현실', '고문', '고통', '공포', '생존', '상실', '고독', '갈등', '개그', '독재', '헌신', '정치', '욕망', '수색', '질서', '신화', '춤', '충격', '좀비', '정글', '바다', '괴담', '전기', '용기', '자존심', '절망', '판타지', '무력감', '질병', '과학', '윤리', '권력', '슬픔', '동물', '종교', '탐험', '미래', '상처', '모험', '뮤지컬', '스포츠', '유쾌', '음모론', '음모', '부도덕', '추격', '군대', '폭력', '시민운동', '코미디', '의심', '이별', '시골', '유령', '군사', '로맨스', '인간성', '외계인', '재난', '의료', '자아', '감옥', '저항', '부조리']

        for category in category_avg_map.keys():

            category_avg = category_avg_map[category]
            category_cnt = category_count_map[category]

            category_index = categories_list.index(category)


            #"Category"의 평균. 쉬운 접근을 위해 만들었다. 싫으면 df1.loc[df["Category"] == category]["Similarity"].sum()으로 접근하던지.
            #category_avg_map[category] = df1.loc[df1["Category"] == category]["Similarity"].mean()

            #original_data = df1.loc[df1["Category"] == category]["Similarity"].mean()
            ###category_avg_map[category] = df2.loc[df2["Category"] == category]["average"].iloc[0]
            #category_avg_map[category] = 0.2
            #print(f"가중치 비교 {original_data} : {category_avg_map[category]}")

            #적절한 색 값을 입히기 위해 만든 인덱스. 알고리즘상으로 의미는 없다. 그냥 보기 편하라고.
            #color_index = math.floor(category_avg_map[category]*10)

            #카테고리에 포함되는 형태소 갯수를 의미한다.
            #category_cnt:int = category_count_map[category]#df2.loc[df2["Category"] == category]["Count"].iloc[0]
            #category_cnt:int = 10

            morph_cate_ratio:float = category_cnt / morphemeCNT


            percentage_multiplier:float = morph_cate_ratio * count_amount
            similarity_final_multiplier:float = category_avg * percentage_multiplier

            category_index:int = category_index
            #category_index:int = 2

            if weightlist.get(category) == None:
                weightlist[category] = []
            weightlist[category].append((category_index, similarity_final_multiplier))

            #print(f"{COLOR[color_index]}{category} : {category_avg_map[category]:.3f}\t| {category_cnt} \t {percentage_multiplier} \t {similarity_final_multiplier}")

        return weightlist
        """
        category_avg_map의 key는 사실 df2["Category"]의 category기 때문에
        아래 코드는 쓸데 없는 반복이다.
        """
           
        """
        for category in category_avg_map.keys():
            print(category)
        """



# def work(id, start, end, result):
#     total = 0
#     for i in range(start, end):
#         total += i
#     result.put(total)
#     return


# start_time = time.time()

# if __name__ == "__main__":
#     START, END = 0, 100000000
#     result = Queue()
#     th1 = Process(target=work, args=(1, START, END//4, result))
#     th2 = Process(target=work, args=(2, (END//4), 2*(END//4), result))
#     th3 = Process(target=work, args=(3, 2*(END//4), 3*(END//4), result))
#     th4 = Process(target=work, args=(4, 3*(END//4), END, result))
    
#     th1.start()
#     th2.start()
#     th3.start()
#     th4.start()
#     th1.join()
#     th2.join()
#     th3.join()
#     th4.join()

#     result.put('STOP')
#     total = 0
#     while True:
#         tmp = result.get()
#         if tmp == 'STOP':
#             break
#         else:
#             total += tmp
#     print(f"Result: {total}")

#     print(f"elapsed time : {(time.time() - start_time)}")

#print(f"Result: {sum(result)}")






start_time = time.time()



app = Main()


print(f"elapsed time : {(time.time() - start_time)}")