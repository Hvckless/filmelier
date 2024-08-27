import json
import csv
import time
import requests

# 전역 카운터 변수 설정
Load_count = 0

def from_movie(filename):
    movie_code = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # DictReader를 사용합니다.
        for row in reader:
            movie_cd = row['movieCd']  # movieCd 열의 값을 가져옵니다.
            movie_code.append(movie_cd)
            print(f"영화 코드 읽음: {movie_cd}")  # 로그 출력
    return movie_code

def get_movie(movie_cd):
    global Load_count  # 전역 카운터 변수를 사용합니다.

    url = f"https://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key=494fd51f5e5b4a22cc080457849a3f49&movieCd={movie_cd}"
    for get_info in range(3):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            Load_count += 1
            print(f"json로드: {Load_count}")

            return data
        except requests.HTTPError as http_err:
            print(f"HTTP 오류: {http_err}, 재시도 {get_info + 1}/3")
        except json.JSONDecodeError:
            print("JSON 오류")
        time.sleep(3)
    return None

def filter_movie_data(movie_data):
    movie_info = movie_data.get('movieInfoResult', {}).get('movieInfo', {})
    if not movie_info:
        print("영화 정보가 없습니다.")
        return None

    # 등급 및 장르 가져오기
    audits = movie_info.get('audits', [{}])
    filter_genre = audits[0].get('watchGradeNm', '') if audits else ''
    genres = [genre.get('genreNm') for genre in movie_info.get('genres', [])]

    print(f"등급: {filter_genre}, 장르: {genres}")

    # 등급이 18세 관람가 또는 청소년관람불가인 경우
    if filter_genre in ['18세관람가', '청소년관람불가']:
        # 장르가 멜로/로맨스 또는 성인물(에로)일 경우 필터링
        if any(genre in ['멜로/로맨스', '성인물(에로)', ''] for genre in genres) or not genres:
            print("걸러내는 영화:", movie_info.get('movieNm'))
            return None

    # 필터링 조건에 맞지 않으면 영화 제목 반환
    return {
        'movieNm': movie_info.get('movieNm')
    }

def save_filter(movie, filename):
    with open(filename, "a", newline='', encoding='utf-8') as file:
        fieldnames = ['movieNm']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # 파일이 비어있는 경우 헤더를 작성합니다.
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(movie)
        print(f"CSV에 영화 제목 저장: {movie['movieNm']}")

def main(input_csv, output_csv):
    movie_codes = from_movie(input_csv)

    # 각 영화를 개별적으로 처리합니다.
    for movie_cd in movie_codes:
        movie_data = get_movie(movie_cd)
        if movie_data:
            filter_movie = filter_movie_data(movie_data)
            if filter_movie:
                save_filter(filter_movie, output_csv)
        time.sleep(1)

if __name__ == "__main__":
    input_csv = 'src/filmelier/Crawling/json_save/movie_list3.csv'
    output_csv = 'movie_filterList1.csv'
    main(input_csv, output_csv)


