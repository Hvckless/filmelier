import fasttext
import csv
from scipy.spatial.distance import cosine
from collections import defaultdict
from kiwipiepy import Kiwi


# FastText 모델 로드
def load_model(model_path):
    """
    fasttext 모델 호출
    :param model_path:
    :return: fasttext 모델 로드
    """
    return fasttext.load_model(model_path)
# 모델 함수 end


# 영화 제목 파일 로드 및 제목 리스트 저장
def load_movies(movie_file):
    """
    영화 제목 파일을 불러오는 함수.
    파일 시스템에서 허용되지 않는 문자를 '_' 로 변환하여 저장
    처리가 완료된 텍스트를 movie_names 에 담고,
    호출시 영화 제목을 반환 한다
    영화 제목 파일은 밑의 main 함수에서 전달 받는다
    :param movie_file: 영화 제목 파일
    :return: 영화 제목 리스트
    """
    with open(movie_file, 'r', encoding='utf-8') as file:
        movie_oldnames = file.read().splitlines()
        # 영화 제목의 특수문자 처리
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
# 영화 제목 로드 함수 end


# 영화 리뷰 파일 로드
def load_reviews(movie_name):
    """
    영화 리뷰 파일을 가져오는 함수.
    한 줄씩 구분하여 저장하고 있다.
    movie_name 은 밑의 process_reviews 함수에서 전달 받는다.
    :param movie_name: 영화 제목 리스트
    :return: 영화 리뷰 텍스트
    """
    # 영화 리뷰 텍스트 파일 경로
    review_file = f'src/filmelier/Crawling/crawling/test_blog/{movie_name}_review.txt'
    with open(review_file, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]
# 영화 리뷰 파일 로드 함수 end

def exclude_words():
    """
    불용어 파일을 가져오는 함수.
    :return:
    """
    with open('src/filmelier/stopword_filter/save_name1.txt', 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

# kiwi 로 형태소 분석
def morpheme_kiwi(review, kiwi):
    """
    형태소 분석을 하는 함수.
    영화 리뷰 텍스트를 받아 kiwi.tokenize 를 사용해 분류한다.
    kiwi 형태소 분석시 단어가 form 속성에 저장 된다
    따라서 word.form 을 사용하여, 형태소가 존재하면 text_dic 에 담는다.
    word.tag 로 tag 속성이 명사(NNG) 인 형태소만 가져오도록 필터링 한다.
    함수 호출 시 text_dic 을 반환해 형태소 리스트를 받을 수 있다
    :param review:영화 리뷰 목록
    :param kiwi:형태소 분석 모델
    :return: 형태소(kiwi) 텍스트
    """
    text_dic = {}
    exclude_dic = {}
    exclude_word = exclude_words()

    # 불용어 리스트에 없는 단어만 추가
    for line in review:
        kiwi_list = kiwi.tokenize(line)
        for word in kiwi_list:
            if len(word.form) > 1:  # 한 글자 이상의 단어만 분석
                if word.tag == 'NNG':  # 명사(NNG)만 필터링
                    if word.form not in exclude_word:  # 불용어에 없는 단어
                        if word.form not in text_dic:
                            text_dic[word.form] = 0
                        text_dic[word.form] += 1
                    else:  # 불용어에 포함된 단어
                        if word.form not in exclude_dic:
                            exclude_dic[word.form] = 0
                        exclude_dic[word.form] += 1

    return text_dic, exclude_dic  # 형태소 사전과 불용어 사전 반환
# kiwi 형태소 분석 함수 end


# 형태소, 빈도수 저장
def save_morpheme(text_dic, exclude_dic, save_file, exsave_file):
    """
    형태소를 txt 파일로 저장하는 함수.
    형태소 텍스트를 받아서 sorted 로 형태소를 기준으로 정렬 하고 있다.
    정리된 words 를 형태소와 빈도수를 함께 저장한다.
    저장 파일 경로는 밑의 process_reviews 함수에서 전달 받는다.
    :param exclude_dic:
    :param exsave_file:
    :param text_dic: 형태소 텍스트
    :param save_file: 형태소 저장 파일
    :return: 형태소+빈도수 저장
    """
    words = sorted(text_dic.items(), key=lambda x: x[0])
    with open(save_file, 'w', encoding='utf-8') as file:
        for word, count in words:
            file.write(f"{word}\t{count}\n")

    ex_words = sorted(exclude_dic.items(), key=lambda x: x[0])
    with open(exsave_file, 'w', encoding='utf-8') as file:
        for ex_word, ex_count in ex_words:
            file.write(f"{ex_word}\t{ex_count}\n")
# 형태소, 빈도수 저장 함수 end

# 카테고리 파일 로드
def load_category(category_file):
    """
    카테고리 파일을 읽어오는 함수.
    지정한 카테고리가 저장된 파일 로드
    카테고리 파일의 경로는 밑의 main 함수에서 전달받는다
    :param category_file: 카테고리 파일 경로
    :return: 카테고리 텍스트
    """
    with open(category_file, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]
# 카테고리 파일 로드 함수 end


# 형태소 파일 로드
def load_morpheme(morpheme_file):
    """
    형태소 txt 파일을 가져오는 함수.
    형태소 분석 파일을 가져와 담고,
    빈도수는 int 라는 것을 명시 했다.
    호출시 형태소 텍스트 리스트와 형태소 빈도수 리스트를 반환한다.
    :param morpheme_file:형태소 텍스트 파일
    :return: 형태소 텍스트, 형태소 빈도수
    """
    morpheme_words = []
    word_frequencies = {}
    with open(morpheme_file, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                word, freq = line.split()
                morpheme_words.append(word)
                word_frequencies[word] = int(freq)
    return morpheme_words, word_frequencies
# 형태소 파일 로드 함수 end


# 각 형태소 단어를 가장 유사한 카테고리에 할당
def category_words(model, morpheme_words, word_frequencies, categories):
    """
    형태소와 카테고리를 매칭 시키는 함수.
    형태소와 카테고리를 불러 온 뒤,
    fasttext 를 사용해 각 단어의 벡터를 구한다.
    그 다음 카테고리와 각 형태소간의 유사도를 구하고,
    형태소와 가장 유사한 카테고리에 매칭시킨다.
    임계점을 0.3 으로 잡고, 전체 카테고리중 유사도가 가장 높은 하나의 카테고리에만 들어가도록 되어있다.
    또한 각 카테고리별로 count 하여 랭크를 생성 하고, 각 카테고리별 평균 유사도를 구했다.
    results 에는 단어, 카테고리, 유사도, 빈도수 가 들어간다.

    :param model: fasttext 모델
    :param morpheme_words: 형태소 텍스트
    :param word_frequencies: 형태소 빈도
    :param categories: 카테고리 텍스트
    :return: 형태소별 베스트 카테고리 매칭 리스트
    """
    results = []
    category_count = defaultdict(float)
    category_sum = defaultdict(float)
    category_weighted_count = defaultdict(float)

    total_frequency = sum(word_frequencies.values())

    for morph_word in morpheme_words:
        best_category = None
        best_similarity = 0.5

        morph_vector = model.get_word_vector(morph_word)

        # 카테로리별로 코사인거리 계산
        for category in categories:
            category_vector = model.get_word_vector(category)
            # 코사인거리 -1 = 코사인유사도
            similarity = 1 - cosine(morph_vector, category_vector)

            # 코사인 유사도가 기존 값보다 크면 교체
            if similarity > best_similarity:
                best_similarity = similarity
                best_category = category

        # 리스트에 저장
        if best_category:
            # 리스트에 형태소, 카테고리, 유사도, 빈도수 저장
            results.append((morph_word, best_category, best_similarity, word_frequencies[morph_word]))
            # 형태소 빈도수를 전체 빈도수로 나누어 가중치 계산(높을수록 가중치 up)
            frequency_weight = word_frequencies[morph_word] / total_frequency
            # 카테고리에 형태소가 들어온 만큼 count
            category_count[best_category] += 1
            # 카테고리 카운트 * 형태소 빈도 가중치
            category_weighted_count[best_category] += category_count[best_category] * frequency_weight
            # 평균 유사도 * 형태도 빈도 가중치
            category_sum[best_category] += best_similarity * frequency_weight

    return results, category_count, category_weighted_count, category_sum
# 형태소별 카테고리 매칭 함수 end

# 각 카테고리에 할당 한 결과를 csv 파일로 저장
def save_csv(results, sorted_categories, category_weighted_count, category_sum, output_file):
    """
    매칭된 결과를 csv 파일로 저장하는 함수.
    형태소별로 카테고리에 매칭 한 결과를 csv 파일로 저장 한다.
    다만 한 줄에 유사도와 count 를 모두 둘 수 없어서,
    빈 줄을 생성하여 데이터를 두 블럭으로 나누었다.
    위쪽은 단어, 카테고리, 유사도, 빈도수 가 저장된다.
    아래쪽은 카테고리, 빈도수, 카테고리별 평균 유사도가 저장된다.
    저장 경로는 밑의 process_reviews 함수에서 전달 받는다.
    :param results: 형태소별 카테고리 매칭 리스트
    :param sorted_categories: 카테고리 정렬 변수
    :param category_sum: 카테고리별 평균 유사도
    :param output_file: 저장 파일 경로
    :return: csv 파일 저장
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # 형태소 단어별 결과 작성 (빈도수 포함)
        writer.writerow(['Word', 'Category', 'Similarity', 'Frequency'])
        for word, category, similarity, frequency in results:
            writer.writerow([word, category, similarity, frequency])

        # 카테고리별 단어 수 추가
        writer.writerow([])  # 빈 줄 추가
        writer.writerow(['Category', 'Count', 'Weighted Count', 'average'])  # 헤더 작성
        for category, count in sorted_categories:
            weighted_count = category_weighted_count.get(category, 0) # 가중치 반영 카운트
            average = category_sum[category] / count if count > 0 else 0
            writer.writerow([category, count, weighted_count, average])
# 카테고리 csv 파일 저장 함수 end

# 영화 목록별 리뷰을 최종적으로 처리
def process_reviews(movie_names, model, kiwi, category_file):
    """
    위의 함수들을 종합적으로 처리 한다.
    1. load_category 함수에서 카테고리 텍스트를 가져 온다.
    2. 영화 목록 파일에서 제목을 가져와 load_reviews 함수에 전달 하고,
    3. load_reviews 함수에서 영화 이름별 리뷰 텍스트를 받아 온다.
    4. 리뷰 텍스트는 morpheme_kiwi 함수를 호출 하여 형태소 분석을 한다.
    5. save_morpheme 함수를 호출 해 형태소와 빈도수를 저장 한다.
    6. load_morpheme 함수를 호출 해 형태소와 빈도수를 가져 온다.
    7. category_words 함수를 호출 해 형태소를 카테고리에 할당 하고 정렬 한다.
    8. sorted_categories 변수를 사용해 카테고리의 랭크가 같을 시, 평균 유사도로 정렬 하도록 했다.
    8. save_csv 함수를 호출 해 정리 된 파일을 저장 한다.
    :param movie_names: 영화 제목
    :param model: fasttext 모델
    :param kiwi: 형태소 분석 모델
    :param category_file: 카테고리 파일
    :return: 영화 목록별 리뷰 최종 처리
    """
    categories = load_category(category_file)

    for movie_name in movie_names:
        print(f"{movie_name} 로드중")

        review = load_reviews(movie_name)
        if not review:
            print(f"{movie_name}_review.txt 를 찾을 수 없습니다")
            continue

        text_dic, exclude_dic = morpheme_kiwi(review, kiwi)
        # 리뷰 형태소 경로
        word_freq_file = f'src/filmelier/wordFile/ignore/word_dic/{movie_name}_review_dic_filter1.txt'
        word_ex_file = f'src/filmelier/wordFile/ignore/word_dic/{movie_name}_review_dic_ex.txt'
        save_morpheme(text_dic, exclude_dic, word_freq_file, word_ex_file)

        morpheme_words, word_frequencies = load_morpheme(word_freq_file)
        results, category_count, category_sum, category_weighted_count = category_words(model, morpheme_words, word_frequencies, categories)
        # count 순으로 정렬. 동일 할 경우 카테고리의 평균 유사도로 정렬
        sorted_categories = sorted(category_count.items(),
                                   key=lambda x: (x[1] if x[1] > 0 else 0), reverse=True)
        # csv 파일의 경로
        csv_file = f'src/filmelier/wordFile/ignore/csvfile/{movie_name}_categorized_words_filter1.csv'
        save_csv(results, sorted_categories, category_weighted_count, category_sum, csv_file)

        print(f"{movie_name} csv 저장완료")
# 영화 목록별 리뷰 최종 처리 함수 end


# main 함수
def main():
    """
    movie_file 의 경로가 영화 제목 파일이 있는 경로다.
    이 경로만 수정해주면 사용 가능하다.
    :return:
    """
    model_path = 'cc.ko.100.bin'
    # 영화 제목 파일의 경로
    movie_file = 'src/filmelier/Crawling/crawling/movie_list.txt'
    category_file = 'category.txt'

    model = load_model(model_path)
    kiwi = Kiwi()

    movie_names = load_movies(movie_file)

    process_reviews(movie_names, model, kiwi, category_file)
#main 함수 end


if __name__ == "__main__":
    main()

