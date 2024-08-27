import fasttext
from scipy.spatial.distance import cosine

model = fasttext.load_model('cc.ko.100.bin')

file_path = 'Genre_test.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    words = [line.strip() for line in file if line.strip()]

for word in words:
    vector = model.get_word_vector(word)

    #print(f"벡터'{word}':")
    #print(vector)

    neighbors = model.get_nearest_neighbors(word)
    print(f"유사한단어'{word}':")
    print(neighbors)
    print()

if len(words) >= 2:
    word1 = words[0]
    word2 = words[1]
    vector1 = model.get_word_vector(word1)
    vector2 = model.get_word_vector(word2)

    similarity = 1 - cosine(vector1, vector2)
    print(f"코사인유사도 '{word1}' and '{word2}: {similarity}")
else:
    print("파일 오류")
