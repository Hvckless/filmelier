import fasttext
import fasttext.util

# 모델 로드
ft = fasttext.load_model('./ignore/cc.ko.300.bin')

# 현재 모델의 차원 확인
print("Before reducing: ", ft.get_dimension())

# 차원 축소
fasttext.util.reduce_model(ft, 100)

# 축소 후 차원 확인
print("After reducing: ", ft.get_dimension())

ft.save_model('./ignore/cc.ko.100.bin')