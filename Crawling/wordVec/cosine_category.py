import fasttext
import pandas as pd
from scipy.spatial.distance import cosine
import numpy as np
import io


# FastText 모델 로드
model = fasttext.load_model('cc.ko.100.bin')
"""
카테고리를 기준으로 영화간의 유사도를 분석하는 코드. 
"""


# 데이터 파일 로드 및 분리
def load_file(file_path):
    """
    split_index 로 빈줄을 찾고, 빈줄을 기준으로 데이터를 분리했다.
    io 를 사용하여 파일객체처럼 사용 할 수 있도록 해서 오류가 발생하지 않도록 헀다.
    호출하면 위쪽의 데이터와 아래쪽의 데이터를 받을 수 있다.
    :param file_path:
    :return:
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 데이터 블록 분리
    split_index = lines.index('\n')  # 빈 줄의 인덱스 찾기
    similarity_data = ''.join(lines[:split_index])  # 첫 번째 블록
    count_data = ''.join(lines[split_index+1:])  # 두 번째 블록

    # DataFrame 생성
    df_similarity = pd.read_csv(io.StringIO(similarity_data))
    df_count = pd.read_csv(io.StringIO(count_data))

    return df_similarity, df_count


# 데이터 로드 및 분리
category1_similarity, category1_count = load_file('src/filmelier/wordFile/csvfile/주토피아_categorized_words.csv')
category2_similarity, category2_count = load_file('src/filmelier/wordFile/csvfile/피라냐 3DD_categorized_words.csv')

# 카테고리 추출
top10_a = category1_count.head(10)['Category'].tolist()
top10_b = category2_count.head(10)['Category'].tolist()


# 벡터 계산 함수
def get_vector(category):
    return model.get_word_vector(category)


# 벡터 생성
vector_a = {cat: get_vector(cat) for cat in top10_a}
vector_b = {cat: get_vector(cat) for cat in top10_b}

rank_similarity = []
# 유사도 계산

# 유사도 출력
for i in range(min(len(top10_a), len(top10_b))):
    cat_a = top10_a[i]
    cat_b = top10_b[i]

    # 코사인 유사도를 계산 할 때 2차원 배열을 받기를 기대하므로, 2차원 배열로 변경
    # fasttext 는 보통 벡터 값을 1차원 배열로 반환한다.
    vector_a_i = vector_a[cat_a].reshape(1, -1)
    vector_b_i = vector_b[cat_b].reshape(1, -1)

    similar = 1 - cosine(vector_a_i, vector_b_i)
    rank_similarity.append(similar)
    print(f"랭크 {i+1} : 주토피아 : '{cat_a}' : 피라냐 : '{cat_b}' - 코사인 유사도: {similar:.4f}")
average = np.mean(rank_similarity)
print(f"두 영화의 유사도 : {average}")



