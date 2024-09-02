from kiwipiepy import Kiwi
import codecs

kiwi = Kiwi()
fp = codecs.open("./reviews/martianALL.txt", 'r', encoding='utf-8')
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

words = sorted(text_dic.keys())
with open('./reviews/martian_dict.txt', 'w', encoding='utf-8') as file:
    for word in words:
        file.write(f"{word}\n")
print("종료")
