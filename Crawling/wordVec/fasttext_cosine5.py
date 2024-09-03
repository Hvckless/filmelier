import fasttext
import csv
from scipy.spatial.distance import cosine
from collections import defaultdict

# FastText 모델 로드
model = fasttext.load_model('cc.ko.100.bin')

# 카테고리 파일 로드
with open('category.txt', 'r', encoding='utf-8') as file:
    categories = [line.strip() for line in file if line.strip()]

# 형태소 파일 로드
with open('Genre_test5.txt', 'r', encoding='utf-8') as file:
    morpheme_words = [line.strip() for line in file if line.strip()]

# 각 형태소 단어를 가장 유사한 카테고리에 할당
results = []
category_count = defaultdict(int)
threshold = 0.3


for morph_word in morpheme_words:
    morph_vector = model.get_word_vector(morph_word)
    matched_categories = []

    for category in categories:
        category_vector = model.get_word_vector(category)
        similarity = 1 - cosine(morph_vector, category_vector)

        if similarity >= threshold:
            matched_categories.append((category, similarity))
            category_count[category] += 1

    if matched_categories:
        for category, similarity in matched_categories:
            results.append((morph_word, category, similarity))


# 결과를 CSV 파일로 저장
output_file = 'categorized_words_and_counts3.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # 형태소 단어별 결과 작성
    writer.writerow(['Word', 'Category', 'Similarity'])
    for word, category, similarity in results:
        writer.writerow([word, category, similarity])

    # 카테고리별 단어 수 추가
    writer.writerow([])  # 빈 줄 추가
    writer.writerow(['Category', 'Count'])  # 헤더 작성
    for category, count in category_count.items():
        writer.writerow([category, count])

print('카테고리화 완료 및 CSV 저장 완료')
