import pandas as pd
from PIL import Image
from io import BytesIO
import base64
import pymysql

con = pymysql.connect(host='localhost', user='root', password='3131', autocommit=True,
                      db='movie_db')

cur = con.cursor()
byo = BytesIO()
img = Image.open('src/filmelier/Crawling/mysql/마션.jfif')
# img.show()

img.save(byo, format='jpeg')
img_str = base64.b64encode(byo.getvalue())
print(img_str)

img_df = pd.DataFrame({'movie_image': [img_str]})
append_img = "insert into movie_info(movie_image) values(%s) "

cur.execute(img_df)
print("이미지 업로드 완료")
con.close()
