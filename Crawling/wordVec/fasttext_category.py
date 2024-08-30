import fasttext
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# FastText 모델 로드
ft_model = fasttext.load_model('cc.ko.300.bin')

# 카테고리 데이터 로드
category_df = pd.read_csv('src/filmelier/Crawling/wordVec/category.csv')

# 카테고리 중심 벡터 계산
category_vectors = {}
for category in category_df.columns:
    words = category_df[category].dropna().tolist()
    if words:
        word_vectors = [ft_model.get_word_vector(word) for word in words]
        category_vectors[category] = np.mean(word_vectors, axis=0)
    else:
        category_vectors[category] = np.zeros(ft_model.get_dimension())

# 임계값 설정
SIMILARITY_THRESHOLD = 0.5

# 단어 분류 함수
def classify_word(word, category_vectors):
    word_vector = ft_model.get_word_vector(word).reshape(1, -1)
    similarities = {
        category: cosine_similarity(word_vector, vector.reshape(1, -1))[0][0]
        for category, vector in category_vectors.items()
    }

    # 각 카테고리와의 유사도를 출력
    print(f"Word: {word}")
    for category, similarity in similarities.items():
        print(f" - {category}: {similarity}")

    # 유사도가 임계값 이상인 카테고리만 선택
    filtered_similarities = {k: v for k, v in similarities.items() if v >= SIMILARITY_THRESHOLD}

    if filtered_similarities:
        return max(filtered_similarities, key=filtered_similarities.get)
    else:
        return "미분류"  # 유사도가 낮은 경우 '미분류'로 처리

# 분류할 단어 로드
words_df = pd.read_csv('마션.csv')
words = words_df['Word'].tolist()

# 각 단어를 분류
class_words = {category: [] for category in category_vectors.keys()}
class_words["미분류"] = []

for word in words:
    category = classify_word(word, category_vectors)
    class_words[category].append(word)

# 결과를 DataFrame으로 변환 및 저장
result_df = pd.DataFrame({
    k: pd.Series(v, dtype=object) for k, v in class_words.items()
})

result_df.to_csv('class_words.csv', index=False)

print("단어 분류 결과가 저장되었습니다.")
