import fasttext
from collections import Counter

# FastText 모델 로드
model = fasttext.load_model('cc.ko.100.bin')

# 형태소가 저장된 파일 경로
file_path = 'Genre_test.txt'

# 형태소를 리스트로 읽어오기
with open(file_path, 'r', encoding='utf-8') as file:
    words = [line.strip() for line in file if line.strip()]

# 유사한 단어들을 저장할 리스트
similar_words = []

# 각 형태소에 대해 유사한 단어 찾기
for word in words:
    try:
        neighbors = model.get_nearest_neighbors(word)
        # 유사한 단어를 상위 5개까지 추가
        for _, neighbor in neighbors[:5]:
            similar_words.append(neighbor)
    except Exception as e:
        print(f"Error processing word '{word}': {e}")

# 유사한 단어의 빈도 수 계산
word_counts = Counter(similar_words)

# 빈도수가 높은 단어 출력
print("빈도수가 높은 단어:")
for word, count in word_counts.most_common():
    print(f"{word}: {count}")

# 가장 빈번한 단어 출력
if word_counts:
    most_word, _ = word_counts.most_common(1)[0]
    print(f"영화의 장르: {most_word}")
else:
    print("단어가 없음")
