from multiprocessing import Pool
import os
import time

class YourClass:
    def __init__(self):
        self.reviewFolderpath = "../../csvfile/"  # 파일 경로 설정
        self.initial = 0

    def testwork(self, movie: str) -> dict:
        # 여기에 실제 작업 내용을 작성합니다.
        # 예를 들어 영화 이름을 키로 하고 임의 결과를 값으로 반환합니다.
        return {movie: f"Processed {movie}"}

    def use_fs(self):
        movielist: list[str] = []  # 영화 리스트

        start_time = time.time()

        # 파일 이름에서 영화 이름 추출
        for filename in os.listdir(self.reviewFolderpath):
            movielist.append(filename.split("_categorized_words.csv")[0])

        # 멀티프로세싱 수행
        with Pool(os.cpu_count()) as pool:
            results = pool.map(self.testwork, movielist)

        # 결과를 {영화 이름: 결과물} 형태의 딕셔너리로 변환
        results_dict = {k: v for result in results for k, v in result.items()}

        # 결과 확인
        print(f"Total results: {len(results_dict)}")
        print(results_dict)

        print(f"Elapsed time: {(time.time() - start_time):.2f} seconds")

# 클래스 사용 예시
your_class = YourClass()
your_class.use_fs()
