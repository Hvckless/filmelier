import fasttext
import csv
from scipy.spatial.distance import cosine
from collections import defaultdict
from kiwipiepy import Kiwi


# FastText 모델 로드
def load_model(model_path):
    return fasttext.load_model(model_path)


# 영화 제목 파일 로드 및 제목 리스트 저장
def load_movies(movie_file):
    with open(movie_file, 'r', encoding='utf-8') as file:
        movie_oldnames = file.read().splitlines()
        movie_names = [name.replace('/', '_')
                           .replace('\\', '_')
                           .replace(':', '_')
                           .replace('*', '_')
                           .replace('?', '_')
                           .replace('"', '_')
                           .replace('<', '_')
                           .replace('>', '_')
                           .replace('|', '_')
                    for name in movie_oldnames]
    return movie_names


# 영화 리뷰 파일 로드
def load_reviews(movie_name):
    review_file = f'src/filmelier/Crawling/crawling/blog_review/{movie_name}_review.txt'
    with open(review_file, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]


# kiwi 로 형태소 분석
def morpheme_kiwi(review, kiwi):
    text_dic = {}
    for line in review:
        kiwi_list = kiwi.tokenize(line)
        for word in kiwi_list:
            if len(word.form) > 1:
                if word.tag == 'NNG':
                    if word.form not in text_dic:
                        text_dic[word.form] = 0
                    text_dic[word.form] += 1
    return text_dic


# 형태소, 빈도수 저장
def save_morpheme(text_dic, save_file):
    words = sorted(text_dic.items(), key=lambda x: x[0])
    with open(save_file, 'w', encoding='utf-8') as file:
        for word, count in words:
            file.write(f"{word}\t{count}\n")


# 카테고리 파일 로드
def load_category(category_file):
    with open(category_file, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]


# 형태소 파일 로드
def load_morpheme(morpheme_file):
    morpheme_words = []
    word_frequencies = {}
    with open(morpheme_file, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                word, freq = line.split()
                morpheme_words.append(word)
                word_frequencies[word] = int(freq)
    return morpheme_words, word_frequencies


# 각 형태소 단어를 가장 유사한 카테고리에 할당
def category_words(model, morpheme_words, word_frequencies, categories):
    results = []
    category_count = defaultdict(int)

    for morph_word in morpheme_words:
        best_category = None
        best_similarity = 0.3

        morph_vector = model.get_word_vector(morph_word)

        for category in categories:
            category_vector = model.get_word_vector(category)
            similarity = 1 - cosine(morph_vector, category_vector)

            if similarity > best_similarity:
                best_similarity = similarity
                best_category = category

        if best_category:
            results.append((morph_word, best_category, best_similarity, word_frequencies[morph_word]))
            category_count[best_category] += 1

    return results, category_count


# 각 카테고리에 할당 한 결과를 csv 파일로 저장
def save_csv(results, sorted_categories, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # 형태소 단어별 결과 작성 (빈도수 포함)
        writer.writerow(['Word', 'Category', 'Similarity', 'Frequency'])
        for word, category, similarity, frequency in results:
            writer.writerow([word, category, similarity, frequency])

        # 카테고리별 단어 수 추가
        writer.writerow([])  # 빈 줄 추가
        writer.writerow(['Category', 'Count'])  # 헤더 작성
        for category, count in sorted_categories:
            writer.writerow([category, count])


# 영화 목록별 리뷰를 처리 하고 csv 파일로 저장
def process_reviews(movie_names, model, kiwi, category_file):
    categories = load_category(category_file)

    for movie_name in movie_names:
        print(f"{movie_name} 로드중")

        review = load_reviews(movie_name)
        if not review:
            print(f"{movie_name}_review.txt 를 찾을 수 없습니다")
            continue

        text_dic = morpheme_kiwi(review, kiwi)
        word_freq_file = f'{movie_name}_review_dic.txt'
        save_morpheme(text_dic, word_freq_file)

        morpheme_words, word_frequencies = load_morpheme(word_freq_file)
        results, category_count = category_words(model, morpheme_words, word_frequencies, categories)
        sorted_categories = sorted(category_count.items(), key=lambda x: x[1], reverse=True)

        csv_file = f'src/filmelier/csvfile/{movie_name}_categorized_words.csv'
        save_csv(results, sorted_categories, csv_file)

        print(f"{movie_name} csv 저장완료")


def main():
    model_path = 'cc.ko.100.bin'
    movie_file = 'src/filmelier/Crawling/crawling/movie_list.txt'
    category_file = 'category.txt'

    model = load_model(model_path)
    kiwi = Kiwi()

    movie_names = load_movies(movie_file)

    process_reviews(movie_names, model, kiwi, category_file)

if __name__ == "__main__":
    main()

