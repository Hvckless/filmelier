import os

import pymysql
#import pandas as pd
from pymysql.cursors import DictCursor

con = pymysql.connect(host='192.168.0.11', user='root', password='3131',
                      db='test_db', charset='utf8mb4', # 한글처리 (charset = 'utf8')
                      autocommit=True, # 결과 DB 반영 (Insert or update)
                      cursorclass=DictCursor # DB조회시 컬럼명을 동시에 보여줌
                     )
cur = con.cursor()

filepath:str = "../../csvfile/"

movielist = []

num_cnt = 0

for filename in os.listdir(filepath):
    movielist.append(filename.split("_categorized_words.csv")[0])


for movie in movielist:
    with open(filepath+movie+"_categorized_words.csv", 'r', encoding="utf-8") as file:
        content = file.read()

    a = movie
    b = content

    sql = "INSERT INTO articles (title, content) VALUES (%s, %s)"
    cur.execute(sql, (a, b))

    rows = cur.fetchall()

    print(f"{num_cnt}개 완료")
    num_cnt += 1


# 제목과 내용을 변수에 저장
  # 여기에 실제 제목을 넣으세요
  # 여기에 실제 내용을 넣으세요

# article 테이블에 데이터 삽입



con.close() # DB 연결 종료
#print(rows)