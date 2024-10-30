from multiprocessing import Pool
from os import error
import sys
import os
import time
import math
import json
#import numpy as np
class FileReader:
    def __init__(self):
        self.initial = 1
    def getMovieListFromReview(self, filepath):
        movielist = []
        for filename in os.listdir(filepath):
            movielist.append(filename.split("_categorized_words.csv")[0])
        return movielist
    def readCSVTables(self, filepath):
        tables = []
        with open(filepath, 'r', encoding="utf-8") as file:
            tables = file.read().split("\n\n")
        return tables
class ParameterHandler:
    def __init__(self):
        self.initial = 1
    def getListFromParameter(self):
        movielist = []
        try:
            for arg in sys.argv[1][1:len(sys.argv[1])-1].split(","):
               movielist.append(arg.replace("'", "").replace("*", " "))
        except:
            print(error)
        finally:
            return movielist
    def getListFromInput(self, input_string):
        movielist = []
        try:
            for arg in input_string[1:len(input_string)-1].split(","):
               movielist.append(arg.replace("'", "").replace("*", " "))
        except:
            print(error)
        finally:
            return movielist
class FormulaCalculator:
    def __init__(self):
        self.initial = 1
    def getWeightFromGapBetweenWeight(self, x):
        return (-2 / math.pi) * math.atan(2 * x - 2) + 1
    def getWeightFromGapBetweenDistance(self, x, maxdistance, max, min):
        if x > 10:
            x = 10
        return ((max - min) / 2) * math.cos(x * (math.pi / maxdistance)) + ((max + min) / 2)
class WeightCalculator:
    filepath = None
    filereader = FileReader()
    movie_weight_map = {}
    formulacalculator = FormulaCalculator()
    def __init__(self):
        self.initial = 1
    def readAllMovieWeightList(self, reviewpath, movielist):
        some_movie_weightlist = {}
        self.filepath = reviewpath
        with Pool(os.cpu_count()) as pool:
            results = pool.map(self.getWeightFromMovieElement, movielist)
        for result in results:
            for k, v in result.items():
                some_movie_weightlist[k] = v
        self.movie_weight_map = some_movie_weightlist
        return some_movie_weightlist
    def getWeightBetweenMovies(self):
        result = {}
        return result
    def compareAllMovieWeightList(self, weightlist, mvlist_param, mvlist_review):
        scorelist = {}
        for review in mvlist_review:
            if review not in mvlist_param:
                score = 0
                target_movie_weightlist = self.movie_weight_map[review]
                for category in target_movie_weightlist.keys():
                    distance_multiplier = 0
                    similarity_multiplier = 0
                    if (weightlist.get(category) == None) or (target_movie_weightlist.get(category) == None):
                        continue
                    distance = weightlist[category][0][0]
                    similarity = weightlist[category][0][1]
                    target_distance = target_movie_weightlist[category][0][0]
                    target_similarity = target_movie_weightlist[category][0][1]
                    distance_multiplier = self.formulacalculator.getWeightFromGapBetweenDistance(abs(distance - target_distance), 10, 2, 0.2)
                    similarity_multiplier = self.formulacalculator.getWeightFromGapBetweenWeight(abs(similarity - target_similarity))
                    score = score + (similarity * distance_multiplier * similarity_multiplier)
                scorelist[score] = review
        return scorelist
    def getWeightFromMovieList(self, mvlist_param):
        something_like_this = {}
        for movie in mvlist_param:
            mvweight = self.movie_weight_map[movie]
            for category in mvweight:
                mvweight_index = mvweight[category][0][0]
                mvweight_weight = mvweight[category][0][1]
                if something_like_this.get(category) == None:
                    something_like_this[category] = []
                something_like_this[category].append((mvweight_index, mvweight_weight))
        weightpointsV2 = something_like_this
        return weightpointsV2
    def getWeightFromMovieElement(self, args):
        csv_table = self.filereader.readCSVTables(self.filepath+args+"_categorized_words.csv")
        df2 = csv_table[1]
        data_list = df2.split("\n")
        read_data_map = {}
        output_data_map = {}
        sum_of_mrpheme = 0
        for i in range(1, len(data_list)-1):
            data_list_split = data_list[i].split(",")
            sum_of_mrpheme += float(data_list_split[1])
            try:
                read_data_map[data_list_split[0]] = [(float(data_list_split[1]),float(data_list_split[2]))]
            except:
                continue
        morphemeCNT = sum_of_mrpheme
        read_data_map_keys = read_data_map.keys()
        read_data_map_length = len(read_data_map_keys)
        read_data_map_list = list(read_data_map_keys)
        for category in read_data_map_keys:
            category_avg = read_data_map[category][0][1]
            category_cnt = read_data_map[category][0][0]
            morph_cate_ratio = category_cnt / morphemeCNT
            percentage_multiplier = morph_cate_ratio * read_data_map_length
            similarity_final_multiplier = category_avg * percentage_multiplier
            category_index = read_data_map_list.index(category)
            if output_data_map.get(category) == None:
                output_data_map[category] = []
            output_data_map[category].append((category_index, similarity_final_multiplier))
        return {args:output_data_map}
    def getWeightFromMovieWithDistance(self, weightlist):
        result_weightlist = {}
        for category in weightlist.keys():
            similarity_list = weightlist.get(category,[(0,0)])
            sum_of_similarity = 0
            sum_of_distance = 0
            avg_of_similarity = 0
            avg_of_distance = 0
            for similarity in similarity_list:
                sum_of_similarity = sum_of_similarity + similarity[1]
                sum_of_distance = sum_of_distance + similarity[0]
            avg_of_similarity = sum_of_similarity / len(similarity_list)
            avg_of_distance = sum_of_distance / len(similarity_list)
            if result_weightlist.get(category) == None:
                result_weightlist[category] = []
            result_weightlist[category].append((avg_of_distance, avg_of_similarity))
        return result_weightlist
class Main:
    reviewFolderpath = None
    weightcalculator = WeightCalculator()
    parameterhandler = ParameterHandler()
    def __init__(self):
        self.initial = 1
    def getMovieListFromParameter(self):
        return self.parameterhandler.getListFromParameter()
    def getMovieListFromInput(self, input_string):
        return self.parameterhandler.getListFromInput(input_string)
    def getMovieListFromReviews(self):
        return FileReader().getMovieListFromReview(self.reviewFolderpath)
    def readAllMovieWeightList(self, mvlist):
        return self.weightcalculator.readAllMovieWeightList(self.reviewFolderpath, mvlist)
    def getWeightListFromMovieList(self, mvlist_param):
        return self.weightcalculator.getWeightFromMovieList(mvlist_param)
    def getWeightListBetweenMovies(self, mvlist_param, mvlist_review, avg_weightlist):
        return self.weightcalculator.compareAllMovieWeightList(avg_weightlist, mvlist_param, mvlist_review)
    def makeResult(self):
        movielist_string = input()
        if movielist_string == "end":
            return
        start_time = time.time()
        mvlist_param = self.getMovieListFromInput(movielist_string)
        score_dictionary = self.getWeightListBetweenMovies(
            mvlist_param,
            mvlist_review,
            self.getWeightListFromMovieList(mvlist_param)
        )
        sorted_dictionary = dict(sorted(score_dictionary.items(), key=lambda item: item[0], reverse=True))
        top_10 = {score: name for score, name in list(sorted_dictionary.items())[:10]}
        print(json.loads(json.dumps(top_10)))
        print(f"elapse time : {time.time() - start_time}")
        self.makeResult()
    def setReviewFolderpath(self, filepath):
        self.reviewFolderpath = filepath
    def getReviewFolderpath(self):
        return self.reviewFolderpath
if __name__ == "__main__":
    app = Main()
    app.setReviewFolderpath("../../csvfile/")
    mvlist_review = app.getMovieListFromReviews()
    hello_list = app.readAllMovieWeightList(mvlist_review)
    app.makeResult()