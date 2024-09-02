from bs4 import BeautifulSoup
from konlpy.tag import Okt
import codecs

fp = codecs.open("src/filmelier/Crawling/crawling/blog_review/마션_review.txt", "r", encoding="utf-8")
text = fp.read()
okt = Okt()

text_dic = {}
lines = text.split("\n")
for line in lines:
    malist = okt.nouns(line)
    for word in malist:
        if len(word) > 1:
            if word not in text_dic:
                text_dic[word] = 0
            text_dic[word] += 1

words = sorted(text_dic.items(), key = lambda x: x[0])
with open('마션_category.txt', 'w', encoding='utf-8') as file:
    for word, count in words:
        file.write(f"{word}\t{count}\n")
print("종료")

