import fasttext
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

ft_model = fasttext.load_model('cc.ko.100.bin')

category_df = pd.read_csv('category.csv', header=None)

'''
# 카테고리 중심 벡터 계산
category_vectors = {}
for category in category_df.columns:
    words = category_df[category].dropna().tolist()
    if words:
        word_vectors = [ft_model.get_word_vector(word) for word in words]
        category_vectors[category] = np.mean(word_vectors, axis=0)
        print(f"Category: {category}, Vector: {category_vectors[category][:10]}")  # 일부 벡터 출력
    else:
        category_vectors[category] = np.zeros(ft_model.get_dimension())

# 단어 벡터 생성 및 출력 (디버깅용)
test_word = '사랑'  # 예시 단어
word_vector = ft_model.get_word_vector(test_word)
print(f"Word: {test_word}, Vector: {word_vector[:10]}")  # 일부 벡터 출력

for category, vector in category_vectors.items():
    print(f"Category: {category}, Vector: {vector[:10]}")

    print(f"Word vector shape: {word_vector.shape}")
for category, vector in category_vectors.items():
    print(f"Category: {category}, Vector shape: {vector.shape}")

# 단어 분류 함수
def classify_word(word, category_vectors):
    word_vector = ft_model.get_word_vector(word).reshape(1, -1)
    similarities = {
        category: cosine_similarity(word_vector, vector.reshape(1, -1))[0][0]
        for category, vector in category_vectors.items()
    }

    # 각 카테고리와의 유사도 출력 (디버깅용)
    print(f"Word: {word}")
    for category, similarity in similarities.items():
        print(f" - {category}: {similarity}")

    return max(similarities, key=similarities.get)

# 단어 분류 테스트
test_words = ['사랑', '전쟁', '미래']
for word in test_words:
    classify_word(word, category_vectors)
'''


def get_word_vector(word):
    if word in ft_model.words:
        vector = ft_model.get_word_vector(word)
        if np.all(vector == 0):
            print(f"Warning: The vector for '{word}' is all zeros.")
        return vector
    else:
        print(f"Warning: The word '{word}' is not in the FastText model vocabulary.")
        return None


for category in category_df.columns:
    words = category_df[category].dropna().tolist()
    for word in words:
        vector = get_word_vector(word)
        if vector is not None:
            print(f"Category: {category}, Word: {word}, Vector: {vector[:10]}")
