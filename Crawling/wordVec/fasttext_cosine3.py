import fasttext
import csv
from scipy.spatial.distance import cosine

# FastText 모델 로드
model = fasttext.load_model('cc.ko.100.bin')

# 카테고리 파일 로드
with open('category.txt', 'r', encoding='utf-8') as file:
    categories = [line.strip() for line in file if line.strip()]

# 형태소 파일 로드
with open('Genre_test2.txt', 'r', encoding='utf-8') as file:
    morpheme_words = [line.strip() for line in file if line.strip()]

# 각 형태소 단어를 가장 유사한 카테고리에 할당
results = []

for morph_word in morpheme_words:
    best_category = None
    best_similarity = -1

    morph_vector = model.get_word_vector(morph_word)

    for category in categories:
        category_vector = model.get_word_vector(category)
        similarity = 1 - cosine(morph_vector, category_vector)

        if similarity > best_similarity:
            best_similarity = similarity
            best_category = category

    results.append((morph_word, best_category, best_similarity))

# 결과를 CSV 파일로 저장
output_file = 'categorized_words2.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Word', 'Category', 'Similarity'])

    for word, category, similarity in results:
        writer.writerow([word, category, similarity])

print('카테고리화 완료 및 CSV 저장 완료')
