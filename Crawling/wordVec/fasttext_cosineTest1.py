import numpy as np
from numpy.linalg import svd
import fasttext
from scipy.spatial.distance import cosine


model = fasttext.load_model('cc.ko.100.bin')

'''
def cosine_fast(vec1, vec2):
    return np.dot(vec1,vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
'''


# 코사인 유사도 분석 함수
def cosine_fast(vec1, vec2):
    return 1 - cosine(vec1, vec2)


word1 = '물'
word2 = '불'
vec1 = model.get_word_vector(word1) # word1의 벡터를 가져옴
vec1 = vec1.reshape(1, -1)
# vec2 = model.get_word_vector(word2)
# print("vec1: ", vec1)
# print("vec2: ", vec2)

U, s, Vt = svd(vec1)
print("U:", U, end='\n\n')
print("s:", s, end='\n\n')
print("Vt:", Vt)

# print("U:" + str(U.shape))
# print("s:" + str(s.shape))
# print("Vt:" + str(Vt.shape))

# similar = cosine_fast(vec1, vec2)
# print(f"유사도 ({word1}, {word2}): {similar}")

