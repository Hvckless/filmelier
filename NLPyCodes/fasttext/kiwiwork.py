from kiwipiepy import Kiwi
kiwi = Kiwi()
for result, score in kiwi.analyze("형태소 분석 결과입니다", top_n=5):
    print(score, result, sep='\t')


#with open(file_path, 'r', encoding='utf-8') as file:
#    words = [line.strip() for line in file if line.strip()]

print("-----------------SPLIT TEST------------------")

result = kiwi.tokenize("형태소 분석 결과입니다")
print(result)