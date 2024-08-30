import numpy as np
import fasttext


model = fasttext.load_model('cc.ko.100.bin')


def cosine_fast(vec1, vec2):
    return np.dot(vec1,vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


word1 = '우주'
word2 = '화성'
vec1 = model.get_word_vector(word1)
vec2 = model.get_word_vector(word2)

similar = cosine_fast(vec1,vec2)
print(f"유사도 ({word1}, {word2}): {similar}")
