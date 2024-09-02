import numpy as np
import fasttext
from scipy.spatial.distance import cosine


model = fasttext.load_model('./ignore/cc.ko.100.bin')

'''
def cosine_fast(vec1, vec2):
    return np.dot(vec1,vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
'''


def cosine_fast(vec1, vec2):
    return 1 - cosine(vec1, vec2)


word1 = '재밌는'
word2 = '유쾌하다'
vec1 = model.get_word_vector(word1)
vec2 = model.get_word_vector(word2)
print("vec1: ", vec1)
print("vec2: ", vec2)

similar = cosine_fast(vec1, vec2)
print(f"유사도 ({word1}, {word2}): {similar}")

