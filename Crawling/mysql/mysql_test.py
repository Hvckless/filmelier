import pandas as pd
from sqlalchemy import create_engine
from PIL import Image
from io import BytesIO
import base64
import pymysql

con = pymysql.connect(host='localhost', user='root', password='3131', autocommit=True,
                      db='movie_db')

cur = con.cursor()

sql = "INSERT INTO movie_info(movie_name) values ('심해솔')"
cur.execute(sql)

print("{} 개의 레코드가 입력되었습니다".format(cur.rowcount))
con.close()

