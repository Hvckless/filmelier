import codecs
from bs4 import BeautifulSoup
from konlpy.tag import Okt
import os

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

    qlines = []

    for line in lines:
        if line.isspace():
            continue
        qlines.append(line)

    for line in qlines:
        malist = okt.pos(line)
        for word in malist:
            if word[1] == "Noun": 
                if not (word[0] in word_dic):
                    word_dic[word[0]] = 0
                word_dic[word[0]] += 1 

    keys = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)
    for word, count in keys:
        print("{0}({1}) ".format(word, count), end="")

    # 파일 이름을 사용하여 출력 파일을 만듭니다.
    with open(target + filename, 'w', encoding='utf-8') as fp:
        for word, count in keys:
            fp.write(f"{word},")
    
    print()
