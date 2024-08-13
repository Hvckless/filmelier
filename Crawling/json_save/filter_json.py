import json
import csv
import time
import requests

Load_count = 0

def from_movie(filename):
    movie_code = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movie_cd = row['movieCd']
            movie_code.append(row['movieCd'])
            print(f"영화코드: {movie_cd}")
    return movie_code


def get_movie(movie_cd):
    global Load_count

    url = f"https://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key=50bed5dbddceec0204ce571b38a12fc9&movieCd={movie_cd}"
    for get_info in range(3):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            Load_count += 1
            print(f"json 로드: {Load_count}")
            return data
        except requests.HTTPError as http_err:
            print(f"HTTP오류: {http_err}, 재시도 {get_info +1}/3")
        except json.JSONDecodeError:
            print("json오류")
        time.sleep(3)
    return None


def filter_movie_data(movie_data):
    movie_info = movie_data.get('movieInfoResult',{}).get('movieInfo', {})
    if not movie_info:
        return None

    filter_genre = movie_info.get('audits', [{}])[0].get('watchGradeNm', '')
    genres = [genre.get('genreNm')for genre in movie_info.get('genres', [])]

    if filter_genre in ['18세관람가', '청소년관람불가'] and '멜로/로맨스' not in genres:
        return {
            'movieNm': movie_info.get('movieNm')
        }
    return None


def save_filter(file_data, filename):
    with open(filename, "w", newline='', encoding='utf-8') as file:
        fieldnames = ['movieNm']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(file_data)
    print(f"csv 파일 저장{filename}")


def main(input_csv, output_csv):
    movie_codes = from_movie(input_csv)
    filter_movies = []
    for movie_cd in movie_codes:
        movie_data = get_movie(movie_cd)
        if movie_data:
            filter_movie = filter_movie_data(movie_data)
            if filter_movie:
                filter_movies.append(filter_movie)
        time.sleep(1)

    print(f"필터링된 영화 수: {len(filter_movies)}")
    save_filter(filter_movies, output_csv)


if __name__ == "__main__":
    input_csv = 'src/movieProject/movie_list3.csv'
    output_csv = 'movie_filterList.csv'
    main(input_csv, output_csv)
