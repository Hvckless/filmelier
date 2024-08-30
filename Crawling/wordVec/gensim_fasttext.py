import gensim
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


model = gensim.models.fasttext.load_facebook_model('cc.ko.100.bin')

category_df = pd.read_csv('src/filmelier/Crawling/wordVec/category.csv')

category_vectors = {}
for category in category_df.columns:
    words = category_df[category].dropna().tolist()
    if words:
        word_vectors = [model[word] for word in words if word in model]
        category_vectors[category] = np.mean(word_vectors, axis=0)
    else:
        category_vectors[category] = np.zeros(model.vector_size)


for category, vector in category_vectors.items():
    print(f"Category: {category}, Vector: {vector[:10]}")  # 첫 10개 값만 출력


def classify_word(word, category_vectors):
    if word not in model:
        print(f"Warning: '{word}' not in vocabulary.")
        return None

    word_vector = model[word].reshape(1, -1)
    similarities = {
        category: cosine_similarity(word_vector, vector.reshape(1, -1))[0][0]
        for category, vector in category_vectors.items()
    }

    return max(similarities, key=similarities.get)


test_words = ['사랑', '전쟁', '미래']
for word in test_words:
    category = classify_word(word, category_vectors)
    print(f"Word: {word}, Category: {category}")

