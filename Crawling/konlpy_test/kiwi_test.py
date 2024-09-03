from kiwipiepy import Kiwi
import codecs

kiwi = Kiwi()
fp = codecs.open("src/filmelier/Crawling/crawling/blog_review/인사이드아웃_review.txt", 'r', encoding='utf-8')
text = fp.read()
fp.close()

text_dic = {}
lines = text.split("\n")

for line in lines:
    kiwi_list = kiwi.tokenize(line)
    for word in kiwi_list:
        if len(word.form) > 1:
            if word.tag == 'NNG':
                if word.form not in text_dic:
                    text_dic[word.form] = 0
                text_dic[word.form] += 1

words = sorted(text_dic.items(), key=lambda x: x[0])
with open('인사이드아웃_review_dic.txt', 'w', encoding='utf-8') as file:
    for word, count in words:
        file.write(f"{word}\t{count}\n")
print("종료")

