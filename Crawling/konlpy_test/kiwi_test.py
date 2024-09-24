from kiwipiepy import Kiwi
import codecs

kiwi = Kiwi()
fp = codecs.open("src/filmelier/Crawling/crawling/test_blog/마션_review.txt", 'r', encoding='utf-8')
text = fp.read()
fp.close()

text_dic = {}
lines = text.split("\n")
exword = ['영화', '리뷰', '소설', '원작']
for line in lines:
    kiwi_list = kiwi.tokenize(line)
    for word in kiwi_list:
        if len(word.form) > 1:
            if word.tag == 'NNG' and word.form not in exword:
                if word.form not in text_dic:
                    text_dic[word.form] = 0
                text_dic[word.form] += 1

words = sorted(text_dic.keys())
with open('마션_review_dic_min.txt', 'w', encoding='utf-8') as file:
    for word in words:
        file.write(f"{word}\n")
print("종료")

