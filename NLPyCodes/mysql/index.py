import pymysql
import time
#import pandas as pd
from pymysql.cursors import DictCursor

con = pymysql.connect(host='192.168.0.11', user='root', password='3131',
                      db='test_db', charset='utf8mb4', # 한글처리 (charset = 'utf8')
                      autocommit=True, # 결과 DB 반영 (Insert or update)
                      cursorclass=DictCursor # DB조회시 컬럼명을 동시에 보여줌
                     )
cur = con.cursor()

start_time = time.time()

sql = "select * from articles;" # customers 테이블 전체를 불러옴
cur.execute(sql)
rows = cur.fetchall()
print(len(rows))
print(f"elapsed time : {time.time()-start_time}")

con.close() # DB 연결 종료
