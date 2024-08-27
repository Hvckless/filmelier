def filter_movie_data(movie_data):
    movie_info = movie_data.get('movieInfoResult', {}).get('movieInfo', {})
    if not movie_info:
        return None

    # 등급과 장르를 가져옴
    filter_genre = movie_info.get('audits', [{}])[0].get('watchGradeNm', '')
    genres = [genre.get('genreNm') for genre in movie_info.get('genres', [])]

    # 18세 관람가 또는 청소년 관람불가 등급의 경우
    if filter_genre in ['18세관람가', '청소년관람불가']:
        # 멜로/로맨스 또는 성인물(에로) 장르가 포함된 경우 제외
        if any(genre in ['멜로/로맨스', '성인물(에로)'] for genre in genres):
            return None

    # 그 외의 모든 영화를 반환
    return {
        'movieNm': movie_info.get('movieNm')
    }

# 테스트 데이터 예시
movie_data1 = {
    "movieInfoResult": {
        "movieInfo": {
            "movieCd": "20194403",
            "movieNm": "킹스맨: 퍼스트 에이전트",
            "movieNmEn": "The King's Man",
            "showTm": "130",
            "prdtYear": "2020",
            "openDt": "20211222",
            "prdtStatNm": "개봉",
            "typeNm": "장편",
            "genres": [
                {"genreNm": "액션"}
            ],
            "audits": [
                {
                    "auditNo": "2021-MF03082",
                    "watchGradeNm": "청소년관람불가"
                }
            ]
        }
    }
}

movie_data2 = {
    "movieInfoResult": {
        "movieInfo": {
            "movieCd": "20247217",
            "movieNm": "숙모 삼촌한테는 비밀이야",
            "movieNmEn": "TATANAIDANNA",
            "showTm": "60",
            "prdtYear": "2022",
            "openDt": "20240130",
            "prdtStatNm": "개봉",
            "typeNm": "장편",
            "genres": [
                {"genreNm": "멜로/로맨스"},
                {"genreNm": "드라마"}
            ],
            "audits": [
                {
                    "auditNo": "2024-MF00056",
                    "watchGradeNm": "청소년관람불가"
                }
            ]
        }
    }
}

# 결과 확인
print(filter_movie_data(movie_data1))
print(filter_movie_data(movie_data2))
