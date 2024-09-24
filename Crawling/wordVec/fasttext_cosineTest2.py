import fasttext

model = fasttext.load_model('cc.ko.100.bin')

word = '씨네필운'
similar_words = model.get_nearest_neighbors(word, k=10)
print(f"'{word}'와 유사한 단어")
for similar_word, similarity in similar_words:
    print(f"'{similar_word}': '{similarity}'")




