import fasttext
import numpy as np
import csv

# FastText 모델 로드
try:
    model = fasttext.load_model('cc.ko.100.bin')
    # 모델이 올바르게 로드되었는지 간단한 단어로 테스트
    test_word = "테스트"  # 한국어 단어로 벡터를 테스트
    test_vector = model.get_word_vector(test_word)
    print(f"'{test_word}'의 벡터가 성공적으로 로드되었습니다.")
except UnicodeDecodeError as e:
    print("모델 로딩 중 인코딩 오류 발생:", e)
    exit(1)

def get_word(word):
    try:
        if word in model.words:
            vector = model.get_word_vector(word)
            return vector
        else:
            print(f"오류: '{word}'가 존재하지 않음.")
            return None
    except Exception as e:
        print(f"'{word}'를 처리하는 중 오류 발생:", e)
        return None


file_path = 'category.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    category_words = [line.strip() for line in file if line.strip()]

valid_words = []
for word in category_words:
    vector = get_word(word)
    if vector is not None:
        valid_words.append(word)

# 유효한 단어들을 CSV 파일에 저장
output_file = 'category2.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(valid_words)

print('저장 완료')
