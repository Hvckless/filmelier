import fasttext
import pandas as pd
from scipy.spatial.distance import cosine
import numpy as np
import io

# FastText 모델 로드
model = fasttext.load_model('cc.ko.100.bin')
"""
가중치를 두고 영화간의 유사도를 분석하는 코드
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
category1_similarity, category1_count = load_file('src/filmelier/wordFile/csvfile/하모니_categorized_words_filter.csv')
category2_similarity, category2_count = load_file('src/filmelier/wordFile/csvfile/7번방의 선물_categorized_words_filter.csv')

# 카테고리 추출
top10_a = category1_count['Category'].tolist()
top10_b = category2_count['Category'].tolist()


# 벡터 계산 함수
def get_vector(category):
    return model.get_word_vector(category)


# 벡터 생성
vector_a = {cat: get_vector(cat) for cat in top10_a}
vector_b = {cat: get_vector(cat) for cat in top10_b}

rank_similarity = []
weighted_sum = 0
weight_total = 0

# 유사도 출력
for i in range(min(len(top10_a), len(top10_b))):
    cat_a = top10_a[i]
    cat_b = top10_b[i]

    vector_a_i = vector_a[cat_a].reshape(1, -1)
    vector_b_i = vector_b[cat_b].reshape(1, -1)

    similar = 1 - cosine(vector_a_i, vector_b_i)
    rank = i + 2
    weight = max(200 - rank, 1) # 가중치 적용.200으로 시작해 1까지 내려감 이후는 모두 1

    weighted_sum += similar * weight # 코사인유사도 * 랭크별 가중치
    weight_total += weight # 가중치의 합
    rank_similarity.append(similar)
    print(f"랭크 {i+1} : 하모니 : '{cat_a}' : 7번방 : '{cat_b}' - 코사인 유사도: {similar:.4f}")
average = weighted_sum / weight_total
print(f"두 영화의 유사도 : {average}")



