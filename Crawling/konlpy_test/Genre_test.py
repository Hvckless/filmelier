from bs4 import BeautifulSoup
from konlpy.tag import Okt
import codecs

fp = codecs.open("src/filmelier/Crawling/konlpy_test/martianALL.txt", "r", encoding="utf-8")
text = fp.read()
okt = Okt()

text_dic = {}
lines = text.split("\n")
for line in lines:
    malist = okt.pos(line)
    for word in malist:
        if word[1] == "Noun" and len(word[0]) >1:
            if not (word[0] in text_dic):
                text_dic[word[0]] = 0
            text_dic[word[0]] += 1

words = sorted(text_dic.keys())

with open('Genre_test.txt', 'w', encoding='utf-8') as file:
    for word in words:
        file.write(f"{word}\n")
print("종료")
