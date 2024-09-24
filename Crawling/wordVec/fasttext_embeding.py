import fasttext
import csv
import pandas as pd

with open('src/filmelier/Crawling/word_dic/마션_review_dic.txt', 'r', encoding='utf=8') as file:
    sentences = file.readlines()


token_sentences = [sentence.strip().split() for sentence in sentences]

model = fasttext.load_model('cc.ko.100.bin')

with open('마션.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    haeder = ['Word', 'sentence_index'] + [f"data{i+1}" for i in range(100)]
    writer.writerow(haeder)
    for sentence_index, sentence in enumerate(token_sentences):
        for word in sentence:
            embedding_vector = model.get_word_vector(word)
            row = [word, sentence_index] + embedding_vector.tolist()
            writer.writerow(row)
