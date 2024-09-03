# IMPORT START

import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine

from kiwipiepy import Kiwi
import fasttext

import codecs

# IMPORT END





# 모델 정의 영역 START

model = fasttext.load_model('./ignore/cc.ko.100.bin')
kiwi = Kiwi()

# 모델 정의 영역 END











# 코사인 유사도 함수 START

#@deprecated
def cosine_fast(vec1, vec2):
    return np.dot(vec1,vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# 코사인 유사도 함수 END









# configuration 값 정의 start


similarityThreshold = 0
categoryFilepath = "undefined"
reviewFolderpath = "undefined"



# configuration 값 정의 end










# configuration handler start

def setSimilarityThreshold(criticality:int):
    similarityThreshold = criticality

def setCategoryFilepath(filepath:str):
    categoryFilepath = filepath

def setReviewFolderpath(folderpath:str):
    reviewFolderpath = folderpath




# configuration handler end









# CSV 파일 출력 함수 START

def exportCSV(movie_name):
    reviewFile = codecs.open(reviewFolderpath+movie_name+".txt", 'r', encoding='utf-8')
    reviewTextContent = reviewFile.read()

    categoryFile = codecs.open(categoryFilepath, 'r', encoding='utf-8')
    categoryTextContent = categoryFile.read()



    # 정의 start

    text_dict = {}
    category_dict = categoryTextContent.split("\n")



    # 정의 end


    # kiwi 형태소분석 start

    lines = reviewTextContent.split("\n") # 텍스트 컨텐츠 라인 반복
    for line in lines:

        kiwi_list = kiwi.tokenize(line) # kiwi 토큰 반복
        for word in kiwi_list:

            if len(word.form) > 1:
                if word.tag == 'NNG':
                    if word.form not in text_dict:
                        text_dict[word.form] = 0
                    text_dict[word.form] += 1

    # kiwi 형태소분석 end







    wordList = []
    contentList = [] # 카테고리, 유사도, 빈도수 + [각 카테고리별 유사도]

    # fasttext 유사도분석 start

    for textToken in text_dict:

        texttoken_vector = model.get_word_vector(textToken)
        


        topRankWord = "undefined"
        topRankSimilarity = 0

        similarityArray = []

        for category in category_dict:
            category_vector = model.get_word_vector(category)

            #currentSimilarity = cosine_fast(texttoken_vector, category_vector)
            currentSimilarity = 1 - cosine(texttoken_vector, category_vector)

            if currentSimilarity > similarityThreshold:
                similarityArray.append(currentSimilarity)
            else:
                similarityArray.append("")


            #print(f"현재 단어 : {textToken} | 비교군 : {category} | 유사도 : {currentSimilarity}")
            
            if currentSimilarity > similarityThreshold:
                if currentSimilarity > topRankSimilarity:
                    topRankSimilarity = currentSimilarity
                    topRankWord = category



        if topRankSimilarity != 0:
            wordList.append(textToken)

            alpha = np.array([topRankWord, topRankSimilarity, text_dict[textToken]])
            beta = np.array(similarityArray)

            theta = np.concatenate((alpha, beta), axis=0)

            #theta = alpha

            contentList.append(theta)

    # fasttext 유사도분석 end


    # 추가 유사도 start


    # 추가 유사도 end








    # CSV 출력 START

    _cate_dict = ['카테고리', '유사도', '빈도']

    alpha = np.array(_cate_dict)
    beta = np.array(category_dict)

    theta = np.concatenate((alpha, beta), axis=0)

    #theta = _cate_dict

    df = pd.DataFrame(contentList, index=wordList, columns=theta)
    df.to_csv(reviewFolderpath+movie_name+"_data.csv")



    #print(theta)

    # CSV 출력 END






    # 마지막 정리 코드 모음

    reviewFile.close() # 리뷰 파일 닫기

# CSV 파일 출력 함수 END







# configuration 설정 start

setSimilarityThreshold(0.4) # 유사도 최솟값

setCategoryFilepath("./movielist/categoryList.txt") # 카테고리 목록 경로
setReviewFolderpath("./review/") # 리뷰 파일이 있는 경로

# configuration 설정 end



# 시작 코드 START

exportCSV("martianALL") # 리뷰 파일 이름 (.txt 제외한 이름)
                        # setReviewFolderpath로 지정한 폴더 아래에 있어야 합니다.


# 시작 코드 END