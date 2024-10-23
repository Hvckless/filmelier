import os
import time

from multiprocessing import Pool

dictionaryLegend = dict[str, list[tuple[int, float]]]

class FuckingPandas:
    kinggodworld:dict[str, dictionaryLegend] = {}
    reviewFolderpath:str = "../../csvfile/"

    def __init__(self):
        if __name__ == "__main__":
            self.initial = 1

            

            self.use_fs()

            
            


    def use_fs(self):
        self.initial = 1

        movielist:list[str] = []

        start_time = time.time()

        for filename in os.listdir(self.reviewFolderpath):
            movielist.append(filename.split("_categorized_words.csv")[0])

        with Pool(os.cpu_count()) as pool:
            results = pool.map(self.testwork, movielist)

        results_dict:dict = {}
        for result in results:
            for k, v in result.items():
                results_dict[k] = v


        print(f"{results_dict['마션']}")
        
        print(f"elapsed time : {(time.time() - start_time)}")



    def testwork(self, args):
        with open(self.reviewFolderpath+args+"_categorized_words.csv", 'r', encoding="utf-8") as file:
            data_list = file.read().split("\n\n")[1].split("\n")
            somedict:dictionaryLegend = {}
            for i in range(1, len(data_list)):
                data_list_split = data_list[i].split(",")
                
                try:
                    somedict[data_list_split[0]] = [(int(data_list_split[1]), float(data_list_split[2]))]
                except:
                    continue

            return {args:somedict}


app = FuckingPandas()