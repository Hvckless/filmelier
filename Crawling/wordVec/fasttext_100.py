import fasttext
import fasttext.util

# 모델 로드
ft = fasttext.load_model('cc.ko.300.bin')

# 현재 모델의 차원 확인
print("Before reducing: ", ft.get_dimension())

# 차원 축소
fasttext.util.reduce_model(ft, 100)

# 축소 후 차원 확인
print("After reducing: ", ft.get_dimension())

# 단어 벡터 확인
vector = ft.get_word_vector('하늘')
print("Vector length:", len(vector))  # 벡터 길이 출력

# 이웃 단어 확인
neighbors = ft.get_nearest_neighbors('하늘')
print(neighbors)

ft.save_model('cc.ko.100.bin')

