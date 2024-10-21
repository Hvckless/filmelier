import fasttext
import numpy as np
from scipy.spatial.distance import cosine
import torch
import torch.nn.functional as F


model = fasttext.load_model('./ignore/cc.ko.100.bin')


def cosine_fast(vec1, vec2):
    return np.dot(vec1,vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


word1 = "치킨"
word2 = "국밥"
vec1 = model.get_word_vector(word1)
vec2 = model.get_word_vector(word2)
similar3 = F.cosine_similarity(torch.tensor(vec1).unsqueeze(0), torch.tensor(vec2).unsqueeze(0), dim=1)
print(similar3)

# while(True):

#     input1 = input("단어 선택 1 : ")
#     if(input1 == "END"):
#         break
#     input2 = input("단어 선택 2 : ")

#     word1 = input1
#     word2 = input2

#     vec1 = model.get_word_vector(word1)
#     vec2 = model.get_word_vector(word2)

#     similar = cosine_fast(vec1,vec2)
#     print(f"유사도 ({word1}, {word2}): {similar}")
#     similar2 = 1-cosine(vec1, vec2)
#     print(f"spatial distance ({word1}, {word2}: {similar2})")
#     similar3 = F.cosine_similarity(torch.tensor(vec1), torch.tensor(vec2))
#     print(f"nn.functional ({word1}, {word2}: {similar3})")

#     print("")
#     print("")
#     print("")

