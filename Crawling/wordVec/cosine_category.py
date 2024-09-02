import fasttext
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import io

# FastText 모델 로드
model = fasttext.load_model('cc.ko.100.bin')

# 데이터 파일 로드 및 분리
def load_and_split_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 데이터 블록 분리
    split_index = lines.index('\n') + 1
    similarity_data = ''.join(lines[:split_index])
    count_data = ''.join(lines[split_index:])

    # DataFrame 생성
    df_similarity = pd.read_csv(io.StringIO(similarity_data))
    df_count = pd.read_csv(io.StringIO(count_data))

    return df_similarity, df_count

# 데이터 로드 및 분리
category1_similarity, category1_count = load_and_split_file('categorized_words7.csv')
category2_similarity, category2_count = load_and_split_file('categorized_words8.csv')

# 카테고리 추출
top10_a = category1_count.sort_values(by='Count', ascending=False).head(10)['Category'].tolist()
top10_b = category2_count.sort_values(by='Count', ascending=False).head(10)['Category'].tolist()

# 벡터 계산 함수
def get_vector(df, category):
    file_df = df[df['Category'] == category]
    if file_df.empty:
        return np.zeros(model.get_dimension())
    word_vectors = [model.get_word_vector(word) for word in file_df['Word']]
    return np.mean(word_vectors, axis=0)

# 벡터 생성
vector_a = np.array([get_vector(category1_similarity, cat) for cat in top10_a])
vector_b = np.array([get_vector(category2_similarity, cat) for cat in top10_b])

# 유사도 계산
similarity = cosine_similarity(vector_a, vector_b)

# 유사도 출력
for i in range(10):
    for j in range(10):
        similar = similarity[i, j]
        print(f"랭크 {i+1}: 주토피아 : '{top10_a[i]}' : 마션 : '{top10_b[j]}' - 코사인 유사도: {similar:.4f}")

