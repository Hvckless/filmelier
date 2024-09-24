import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# 리뷰 데이터를 개별 파일에서 로드
def load_reviews(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reviews = [line.strip() for line in file if line.strip()]
    return reviews

# TF-IDF 벡터화 및 요약 단어 추출 (중복 단어 제거)
def extract_top_words_from_reviews(reviews, top_n=5):
    tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 3), stop_words=None)
    tfidf_matrix = tfidf.fit_transform(reviews)

    feature_array = np.array(tfidf.get_feature_names_out())
    top_words = []

    for i in range(tfidf_matrix.shape[0]):
        tfidf_sorting = np.argsort(tfidf_matrix[i].toarray()).flatten()[::-1]
        # 상위 n개의 단어 추출 후 중복 제거
        top_n_words = list(dict.fromkeys(feature_array[tfidf_sorting][:top_n]))
        top_words.append(top_n_words)

    return top_words

# 요약된 단어들을 파일에 저장 (리뷰 인덱스 없이)
def save_summary(file_path, top_words):
    summary_file = file_path.replace('.txt', '_summary.txt')
    with open(summary_file, 'w', encoding='utf-8') as f:
        for words in top_words:
            f.write(f"{' '.join(words)}\n")
    print(f"요약 파일 저장 완료: {summary_file}")

# 하나의 리뷰 파일을 로드, 요약, 저장하는 함수
def process_review_file(file_path):
    reviews = load_reviews(file_path)
    top_words = extract_top_words_from_reviews(reviews)
    save_summary(file_path, top_words)


# 리뷰 파일 경로 (하나의 영화 리뷰 파일)
file_path = 'src/filmelier/Crawling/crawling/test_blog/7번방의 선물_review.txt'  # 영화 리뷰 파일 경로 입력
process_review_file(file_path)

