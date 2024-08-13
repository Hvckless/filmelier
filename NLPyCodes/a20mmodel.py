import codecs
from bs4 import BeautifulSoup
from konlpy.tag import Okt
import os
from gensim.models import word2vec

path = "./reviews/"
target = "./results/"
file_list = os.listdir(path)
fplist = []

print(file_list)

# 파일 이름 리스트를 만들기 위한 코드
for file in file_list:
    fplist.append((file, codecs.open(path+file, "r", encoding="utf-8")))

# fplist는 (파일 이름, 파일 객체) 쌍의 리스트입니다.
for filename, fpcontent in fplist:
    okt = Okt()
    word_dic= {}
    lines = fpcontent.readlines()

    writeFp = codecs.open(target+filename.split(".")[0]+".gubun", "w", encoding="utf-8")


    qlines = []

    for line in lines:
        if line.isspace():
            continue
        qlines.append(line)

    for line in qlines:
        malist = okt.pos(line, norm=True, stem=True)
        for word in malist:
            if word[1] == "Noun": 
                if not (word[0] in word_dic):
                    word_dic[word[0]] = 0
                word_dic[word[0]] += 1 
            if not word[1] in ["Josa", "Eomi", "Punctuation"]:
            #if word[1] in ["Noun"]:
                writeFp.write(word[0] + " ")

    writeFp.close()

    data = word2vec.Text8Corpus(target+filename.split(".")[0]+".gubun")
    model = word2vec.Word2Vec(data, vector_size=100)
    model.save(target+filename.split(".")[0]+".model")
    print("DONE")
                

    keys = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)
    for word, count in keys:
        print("{0}({1}) ".format(word, count), end="")

    # 파일 이름을 사용하여 출력 파일을 만듭니다.
    with open(target + filename, 'w', encoding='utf-8') as fp:
        for word, count in keys:
            fp.write(f"{word},")
    
    print()
