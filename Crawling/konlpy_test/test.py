from bs4 import BeautifulSoup
from konlpy.tag import Okt
import codecs

fp = codecs.open("src/konlpy_test/animation/insideout.txt", "r", encoding="utf-8")
text = fp.read()
okt = Okt()

text_dic = {}
lines = text.split("\n")
for line in lines:
    malist = okt.pos(line)
    for word in malist:
        if word[1] == "Noun":
            if not (word[0] in text_dic):
                text_dic[word[0]] = 0
            text_dic[word[0]] += 1


keys = sorted(text_dic.items(), key=lambda x:x[1], reverse=True)
for word, count in keys[:50]:
    print("{0}({1})".format(word, count), end="")
print("종료")
