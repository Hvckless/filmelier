import json
import csv
import requests
import time

def get_movie(page, rows):
    url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=494fd51f5e5b4a22cc080457849a3f49&curPage={page}&itemPerPage={rows}"
    for attempt in range(3):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.HTTPError as http_err:
            print(f"HTTP 오류: {http_err}, 재시도 {attempt + 1}/3")
        except json.JSONDecodeError:
            print("JSON 디코딩 오류")
        time.sleep(5)
    return None

def movie_data(movies):
    return [
        {
            'movieCd': movie['movieCd'],
            'movieNm': movie['movieNm']
        }
        for movie in movies
        if movie.get('nationAlt', '') in ['한국', '대만', '인도', '중국', '태국', '미국', '캐나다', '일본', '홍콩', '독일', '러시아', '영국', '이탈리아', '프랑스', '호주']
           and movie.get('openDt', '') >= '20000101'
           and movie.get('typeNm', '') == '장편'
           and movie.get('prdtStatNm', '') == '개봉'
           and movie.get('genreAlt', '') not in ['성인물(에로)', '뮤지컬', '공연', '다큐멘터리', '기타']
    ]

def save_movie(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        fieldnames = ['movieCd', 'movieNm']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"CSV 저장 완료: {filename}")

def main(rows=100):
    all_movie = []
    page = 77

    while True:
        print(f"Fetching page {page}")
        data = get_movie(page, rows)
        if data is None:
            print("API 호출 오류, 작업 종료")
            break

        print(f"Page {page} 응답 데이터:", data)

        movie_list = data.get('movieListResult', {}).get('movieList', [])
        if not movie_list:
            print(f"Page {page}: 더 이상 데이터가 없습니다. 작업을 종료합니다.")
            break

        print(f"Page {page}: {len(movie_list)} movies fetched")
        all_movie.extend(movie_list)
        page += 1
        time.sleep(1)

    filter_data = movie_data(all_movie)
    print("필터링된 데이터 개수:", len(filter_data))
    save_movie(filter_data, 'movie_list3.csv')

if __name__ == "__main__":
    main()

