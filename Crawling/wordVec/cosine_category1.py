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
category1_similarity, category1_count = load_and_split_file('주토피아_categorized_words.csv')
category2_similarity, category2_count = load_and_split_file('categorized_words7.csv')

# 카테고리 추출 및 정렬
top10_a = category1_count.sort_values(by='Count', ascending=False).head(10).reset_index(drop=True)
top10_b = category2_count.sort_values(by='Count', ascending=False).head(10).reset_index(drop=True)

# 벡터 계산 함수
def get_vector(df, category):
    file_df = df[df['Category'] == category]
    if file_df.empty:
        return np.zeros(model.get_dimension())
    word_vectors = [model.get_word_vector(word) for word in file_df['Word']]
    return np.mean(word_vectors, axis=0)

# 벡터 생성
vector_a = np.array([get_vector(category1_similarity, cat) for cat in top10_a['Category']])
vector_b = np.array([get_vector(category2_similarity, cat) for cat in top10_b['Category']])

# 유사도 계산 및 출력
for i in range(10):
    cat_a = top10_a.iloc[i]['Category']
    cat_b = top10_b.iloc[i]['Category']
    vector_a_i = vector_a[i].reshape(1, -1)
    vector_b_i = vector_b[i].reshape(1, -1)
    similarity = cosine_similarity(vector_a_i, vector_b_i)[0, 0]
    print(f"랭크 {i+1}: 주토피아 : '{cat_a}' : 마션 : '{cat_b}' - 코사인 유사도: {similarity:.4f}")
