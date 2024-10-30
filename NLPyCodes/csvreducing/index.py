import csv
import os


reviewFolderpath:str = "../../csvfile/"

# 입력 파일과 출력 파일 경로 설정

for filename in os.listdir(reviewFolderpath):
    input_file = f"{reviewFolderpath}{filename}"
    output_file = f"./output/{filename}"

    # 두 번째 테이블의 유용한 데이터만 저장할 리스트
    filtered_data = []

    # CSV 파일 읽기 및 필요한 데이터 추출
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        # 첫 번째 테이블과 두 번째 테이블의 구분을 위한 플래그
        second_table = False

        for row in reader:
            # 빈 줄 이후 두 번째 테이블 시작
            if not row:
                second_table = True
                continue

            # 두 번째 테이블이 시작된 경우와 헤더 제외
            if second_table and row[0] != "Category":
                filtered_data.append(row)

    # 추출한 데이터를 새로운 파일에 쓰기
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(filtered_data)

    print(f"{filename}처리 완료")
