import os
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Tuple, List

class MovieProcessor:
    def __init__(self):
        self.kinggodworld: Dict[str, Dict[str, List[Tuple[int, float]]]] = {}

    def process_movie(self, movie: str, filepath: str) -> Dict[str, List[Tuple[int, float]]]:
        """하나의 영화를 처리하고 데이터를 반환"""
        try:
            with open(f"{filepath}{movie}_categorized_words.csv", 'r', encoding="utf-8") as file:
                data_list = file.read().split("\n\n")[1].split("\n")
                
                somedict = {}
                for i in range(1, len(data_list)):
                    try:
                        data_list_split = data_list[i].split(",")
                        somedict[data_list_split[0]] = [
                            (int(data_list_split[1]), float(data_list_split[2]))
                        ]
                    except (ValueError, IndexError):
                        continue

                return {movie: somedict}
        except FileNotFoundError:
            print(f"파일 {movie}을(를) 찾을 수 없습니다.")
            return {}

    def use_fs(self):
        filepath = "../../csvfile/"
        movielist = [filename.split("_categorized_words.csv")[0] 
                     for filename in os.listdir(filepath)]

        start_time = time.time()

        # ThreadPoolExecutor로 멀티스레딩 수행
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = executor.map(
                lambda movie: self.process_movie(movie, filepath), movielist
            )

        # 결과를 kinggodworld에 통합
        for result in results:
            self.kinggodworld.update(result)

        print(f"elapsed time: {time.time() - start_time}")

# 실행 예시
processor = MovieProcessor()
processor.use_fs()
