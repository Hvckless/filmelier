from collections import defaultdict # 키가 없을 경우 기본값을 자동으로 생성하는 특징
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from nltk.tokenize import sent_tokenize
import csv
import torch
import nltk
import re
import os



torch.random.manual_seed(0)
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-128k-instruct",
    device_map="cuda",
    torch_dtype="auto",
    trust_remote_code=True,
)

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct")



# 영화 제목 파일 로드
def loadMovie(movie_file):
    with open(movie_file, 'r', encoding='utf-8') as file:
        movie_oldnames = file.read().splitlines()
        movie_names = [re.sub(r'[\/\\:*?"<>|]', '_', name) for name in movie_oldnames]

    return movie_names


# 영화 리뷰 파일 로드
def loadReviews(movie_name):
    review_file = f'src/filmelier/Crawling/crawling/test_blog/{movie_name}_review.txt'
    with open(review_file, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()] # 공백만 있는 줄은 제외시킴
    
             

# 리뷰 텍스트를 문장별로 잘라서 리스트 반환
def makeSentence(review):
     if not isinstance(review, str):
        return []
     
     else:
        sentence_list = sent_tokenize(review) # sent_tokenize는 리스트를 반환함 
        return sentence_list


# 카테고리 파일 로드
def loadCategory(category_file):
    with open(category_file, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()] # 공백이 아닌 라인만 반환.
    
# Phi3 모델 설정 및 로드
def getSimFormPhi3(morph_word, category):
    messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "Read the passage below and indicate the degree to which the two sentences match using a real number between 0 and 1 Never explain about sentence, just answer with real numbers.\n\nSentence 1 : play overwatch now!\nSentence 2 : game play"},
    {"role": "assistant", "content": "Similarity : 0.7231562"},
    {"role": "user", "content": f"Sentence 1 : {morph_word}\nSentence 2 : {category}"},
    ]

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )

    generation_args = {
        "max_new_tokens": 500,
        "return_full_text": False,
        "temperature": 0.0,
        "do_sample": False,
    }

    output = pipe(messages, **generation_args)
    print(output[0]['generated_text'])
    return output[0]['generated_text']

# 각 형태소 단어를 가장 유사한 카테고리에 할당 -> 각 문장을 가장 유사한 카테고리에 할당. 여기에서 phi3사용해야함
def categoryWords(sentence_list, categories):
    results = []
    category_count = defaultdict(int)
    category_sum = defaultdict(float)

    for sentence in sentence_list:
        best_category = None
        best_similarity = 0.5

        for category in categories:

            # 각 문장과 카테고리의 유사도 출력
            similarity = getSimFormPhi3(sentence, category) 

            if similarity > best_similarity:
                best_similarity = similarity # 가장 높은 유사도를 찾기 위함 
                best_category = category
        
        # 각 문장을 유사도가 가장 높은 카테고리에 할당. 
        if best_category: # best_category가 null 이 아니면 true
            results.append((sentence, best_category, best_similarity))
            category_count[best_category] += 1
            category_sum[best_category] += best_similarity
    
    return results, category_count, category_sum






# 각 카테고리에 할당한 결과를 csv 파일로 저장
def saveCsv(results, sorted_categories, category_sum, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # 형태소 단어별 결과 작성
        writer.writerow(['Word', 'Category', 'Similarity']) # 헤더 작성
        for word, category, similarity in results:
            writer.writerow([word, category, similarity])

        # 카테고리별 단어 수 추가
        writer.writerow([])
        writer.writerow(['Category', 'Count', 'Average'])
        for category, count in sorted_categories:
            average = category_sum[category] / count if count > 0 else 0
            writer.writerow([category, count, average])



# 영화 목록별 리뷰를 최종적으로 처리
def processReviews(movie_names, category_file):
    categories = loadCategory(category_file)

    for movie_name in movie_names:
        print(f"{movie_name} 로드중")
        review = loadReviews(movie_name)
        if not review:
            print(f"{movie_name}_review.txt를 찾을 수 없습니다. ")
            continue

        sentence_list = makeSentence(review) # 문장 끊어오기
        results, category_count, category_sum = categoryWords(sentence_list, categories)
        
        # 카테고리별로 할당된 단어의 개수와 평균 유사도를 기준으로 내림차순으로 정렬
        sorted_categories = sorted(category_count.items(),
                            key=lambda x: (x[1], category_sum[x[0]]/x[1] if x[1] > 0 else 0), reverse=True)

        csv_file =  f'src/filmelier/wordFile/csvfile/{movie_name}_categorized_words.csv'
        saveCsv(results, sorted_categories, category_sum, csv_file)

        print(f"{movie_name} csv 저장완료")



def main():
    nltk.download('punkt')
    movie_file = 'src/filmelier/Crawling/crawling/movie_filterList.txt'
    category_file = 'src/filmelier/Crawling/category/category.txt'
    
    movie_names = loadMovie(movie_file)
    processReviews(movie_names, category_file)


if __name__=="__main__":
    main()

