import fasttext
import csv
from scipy.spatial.distance import cosine
from collections import defaultdict

# FastText 모델 로드
model = fasttext.load_model('cc.ko.100.bin')

# 카테고리 파일 로드
with open('category.txt', 'r', encoding='utf-8') as file:
    categories = [line.strip() for line in file if line.strip()]

# 형태소 파일 로드 (단어와 빈도수를 함께 저장)
morpheme_words = []
word_frequencies = {}

with open('1번국도_review_dic.txt', 'r', encoding='utf-8') as file:
    for line in file:
        if line.strip():
            word, freq = line.split()
            morpheme_words.append(word)
            word_frequencies[word] = int(freq)

# 각 형태소 단어를 가장 유사한 카테고리에 할당
results = []
category_count = defaultdict(int)

for morph_word in morpheme_words:
    best_category = None
    best_similarity = 0.3

    morph_vector = model.get_word_vector(morph_word)

    for category in categories:
        category_vector = model.get_word_vector(category)
        similarity = 1 - cosine(morph_vector, category_vector)

        if similarity > best_similarity:
            best_similarity = similarity
            best_category = category

    if best_category:
        results.append((morph_word, best_category, best_similarity, word_frequencies[morph_word]))
        category_count[best_category] += 1

# 카테고리별로 단어 수를 정렬
sorted_categories = sorted(category_count.items(), key=lambda x: x[1], reverse=True)

# 결과를 CSV 파일로 저장
output_file = '1번국도_categorized_words1.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # 형태소 단어별 결과 작성 (빈도수 포함)
    writer.writerow(['Word', 'Category', 'Similarity', 'Frequency'])
    for word, category, similarity, frequency in results:
        writer.writerow([word, category, similarity, frequency])

    # 카테고리별 단어 수 추가
    writer.writerow([])  # 빈 줄 추가
    writer.writerow(['Category', 'Count'])  # 헤더 작성
    for category, count in sorted_categories:
        writer.writerow([category, count])

print('카테고리화 완료 및 CSV 저장 완료')